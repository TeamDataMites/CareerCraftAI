import os

from pyht import Client, TTSOptions, Format
from dotenv import load_dotenv

load_dotenv()

client = Client(
    user_id=os.getenv('PLAY_HT_ID'),
    api_key=os.getenv('PLAY_HT_API_KEY')
)

options = TTSOptions(
    # this voice id can be one of our prebuilt voices or your own voice clone id, refer to the`listVoices()` method for a list of supported voices.
    voice="s3://voice-cloning-zero-shot/1afba232-fae0-4b69-9675-7f1aac69349f/delilahsaad/manifest.json",

    # you can pass any value between 8000 and 48000, 24000 is default
    sample_rate=44_100,

    # the generated audio encoding, supports 'raw' | 'mp3' | 'wav' | 'ogg' | 'flac' | 'mulaw'
    format=Format.FORMAT_MP3,

    # playback rate of generated speech
    speed=1,
)
