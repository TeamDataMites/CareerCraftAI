import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.chat.podcast.prompt import SYSTEM_PROMPT

from utils.chat.podcast.audio import client, options

import time
import random
import logging
from grpc import RpcError
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def response(user_input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content

def split_text(text, max_length=1000):
    """Split text into chunks of maximum length."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def tts_with_retry(client, text, voice_engine, options):
    try:
        return list(client.tts(text=text, voice_engine=voice_engine, options=options))
    except RpcError as e:
        logger.error(f"gRPC error occurred: {e}")
        raise


def tts_to_file(client, content_chunks, output_file, voice_engine, options):
    """Convert text to speech and write to file with error handling and retries."""
    with open(output_file, 'wb') as f:
        for i, chunk in enumerate(content_chunks):
            logger.info(f"Processing chunk {i + 1} of {len(content_chunks)}")
            try:
                audio_chunks = tts_with_retry(client, chunk, voice_engine, options)
                for audio_chunk in audio_chunks:
                    if not audio_chunk:
                        break
                    f.write(audio_chunk)
            except Exception as e:
                logger.error(f"Failed to process chunk {i + 1}: {e}")

            # Add a small delay between chunks to avoid overwhelming the server
            time.sleep(random.uniform(0.5, 1.5))
