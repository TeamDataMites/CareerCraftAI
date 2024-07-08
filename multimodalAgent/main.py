import asyncio
import logging
import os

from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import JobContext, JobRequest, WorkerOptions, cli, tts, tokenize
from livekit.agents.llm import (
    ChatContext,
    ChatMessage,
    ChatRole,
    ChatImage,
)
from livekit.agents.voice_assistant import VoiceAssistant, AssistantContext
from livekit.plugins import deepgram, openai, silero, google, cartesia
from prompt import SYSTEM_PROMPT
from tools import AssistantFunctions


load_dotenv()
os.environ['DEEPGRAM_API_KEY'] = os.getenv('DEEPGRAM_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['LIVEKIT_URL'] = os.getenv('LIVEKIT_URL')
os.environ['LIVEKIT_API_KEY'] = os.getenv('LIVEKIT_API_KEY')
os.environ['LIVEKIT_API_SECRET'] = os.getenv('LIVEKIT_API_SECRET')
os.environ['CARTESIA_API_KEY'] = os.getenv("CARTESIA_API_KEY")

openai_tts = tts.StreamAdapter(
    tts=openai.TTS(model='tts-1-hd'),
    sentence_tokenizer=tokenize.basic.SentenceTokenizer()
)


async def get_video_track(room: rtc.Room):
    """Get the first video track from the room. We'll use this track to process images."""

    video_track = asyncio.Future[rtc.RemoteVideoTrack]()

    for _, participant in room.participants.items():
        for _, track_publication in participant.tracks.items():
            if track_publication.track is not None and isinstance(
                    track_publication.track, rtc.RemoteVideoTrack
            ):
                video_track.set_result(track_publication.track)
                print(f"Using video track {track_publication.track.sid}")
                break

    return await video_track


async def entrypoint(ctx: JobContext):
    chat_ctx = ChatContext(
        messages=[
            ChatMessage(
                role=ChatRole.SYSTEM,
                text=SYSTEM_PROMPT,
            )
        ]
    )

    gpt = openai.LLM(model="gpt-4o")

    assistant = VoiceAssistant(
        vad=silero.VAD(),  # Voice Activity Detection
        stt=deepgram.STT(),  # Speech-to-Text
        llm=gpt,  # Language Model
        # tts = openai_tts,  # Text-to-Speech (Optional) for long sessions use this
        tts=cartesia.TTS(model='sonic-english', voice='79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e', sample_rate=44100), # cartesia has a limit of 10 mins in free tier use openai for long sessions
        chat_ctx=chat_ctx,  # Chat history context
        fnc_ctx=AssistantFunctions(),
        transcription_speed=5.0
    )

    latest_image: rtc.VideoFrame | None = None

    chat = rtc.ChatManager(ctx.room)

    async def _answer(text: str | dict, use_image: bool = False, action: str = 'reply'):
        """
        Answer the user's message with the given text and optionally the latest
        image captured from the video track.
        :param text:
        :param use_image:
        :return:
        """
        args = {}
        if use_image and latest_image:
            args["images"] = [ChatImage(image=latest_image)]
            if action.strip() == 'reply':
                chat_ctx.messages.append(ChatMessage(role=ChatRole.USER, text=text, **args))

        if action.strip() == 'search':
            chat_ctx.messages.append(ChatMessage(role=ChatRole.ASSISTANT, text=text['search_results']))

        stream = await gpt.chat(chat_ctx)
        await assistant.say(stream, allow_interruptions=True)

        await assistant.say(stream)

    @chat.on("message_received")
    def on_message_received(msg: rtc.ChatMessage):
        """This event triggers whenever we get a new message from the user."""

        if msg.message:
            asyncio.create_task(_answer(msg.message, use_image=False))

    @assistant.on("function_calls_finished")
    def on_function_calls_finished(context: AssistantContext):
        """This event triggers when an assistant's function call completes."""

        user_msg = context.get_metadata("user_msg")
        search_msg = context.get_metadata("user_search")
        if user_msg:
            asyncio.create_task(_answer(user_msg, use_image=True))
        if search_msg:
            asyncio.create_task(_answer(search_msg, use_image=False, action='search'))

    assistant.start(ctx.room)

    await asyncio.sleep(3)

    await assistant.say("Hello I am Elio, how may i assist you?", allow_interruptions=True)

    while ctx.room.connection_state == rtc.ConnectionState.CONN_CONNECTED:
        video_track = await get_video_track(ctx.room)

        async for event in rtc.VideoStream(video_track):
            # We'll continually grab the latest image from the video track
            # and store it in a variable.
            latest_image = event.frame


async def request_fnc(req: JobRequest) -> None:
    logging.info("received request %s", req)
    await req.accept(entrypoint)


if __name__ == "__main__":
    # Initialize the worker with the request function
    cli.run_app(WorkerOptions(request_fnc))
