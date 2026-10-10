import base64
import os
import tempfile
from html import escape
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import APIError, OpenAI
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
MAX_AUDIO_BYTES = 10 * 1024 * 1024
VOICE_NAME = "en-US-Andrew:DragonHDLatestNeural"
SPEECH_LANGUAGE = "pl-PL"


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=8_000)


history_adapter = TypeAdapter(list[ChatMessage])
app = FastAPI(title="Polish Voice Chat")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def required_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise HTTPException(
            status_code=503,
            detail=f"Missing required environment variable: {name}",
        )
    return value


def speech_endpoint() -> str:
    endpoint_url = required_setting("AZURE_SPEECH_ENDPOINT")
    parsed = urlparse(endpoint_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(
            status_code=503,
            detail="AZURE_SPEECH_ENDPOINT must be a valid HTTP or HTTPS URL.",
        )
    return f"{parsed.scheme}://{parsed.netloc}"


def create_speech_config() -> speechsdk.SpeechConfig:
    return speechsdk.SpeechConfig(
        subscription=required_setting("AZURE_SPEECH_KEY"),
        endpoint=speech_endpoint(),
    )


def openai_base_url() -> str:
    endpoint = required_setting("AZURE_OPENAI_ENDPOINT").rstrip("/")
    parsed = urlparse(endpoint)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(
            status_code=503,
            detail="AZURE_OPENAI_ENDPOINT must be a valid HTTP or HTTPS URL.",
        )
    if endpoint.endswith("/openai/v1"):
        return f"{endpoint}/"
    return f"{endpoint}/openai/v1/"


def transcribe_wav(audio_bytes: bytes) -> str:
    speech_config = create_speech_config()
    speech_config.speech_recognition_language = SPEECH_LANGUAGE

    audio_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_file:
            audio_file.write(audio_bytes)
            audio_path = audio_file.name

        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )
        result = recognizer.recognize_once_async().get()
    finally:
        if audio_path:
            Path(audio_path).unlink(missing_ok=True)

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        transcript = result.text.strip()
        if transcript:
            return transcript
        raise HTTPException(status_code=422, detail="No speech was recognized.")

    if result.reason == speechsdk.ResultReason.Canceled:
        details = result.cancellation_details
        message = f"Speech recognition was canceled: {details.reason}"
        if details.reason == speechsdk.CancellationReason.Error:
            message = f"{message}. {details.error_details}"
        raise HTTPException(status_code=502, detail=message)

    raise HTTPException(status_code=422, detail="No speech was recognized.")


def generate_reply(transcript: str, history: list[ChatMessage]) -> str:
    api_key = required_setting("AZURE_OPENAI_API_KEY")
    deployment = required_setting("AZURE_OPENAI_DEPLOYMENT")
    client = OpenAI(
        api_key=api_key,
        base_url=openai_base_url(),
        timeout=30.0,
    )

    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś pomocnym asystentem głosowym. Odpowiadaj naturalnie i zwięźle "
                "po polsku, chyba że użytkownik wyraźnie poprosi o inny język."
            ),
        },
        *[message.model_dump() for message in history[-10:]],
        {"role": "user", "content": transcript},
    ]

    try:
        completion = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_completion_tokens=800,
        )
    except APIError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"The chat model request failed: {exc}",
        ) from exc

    reply = completion.choices[0].message.content
    if not reply:
        raise HTTPException(status_code=502, detail="The chat model returned no text.")
    return reply.strip()


def synthesize_reply(text: str) -> bytes:
    speech_config = create_speech_config()
    speech_config.speech_synthesis_language = SPEECH_LANGUAGE
    speech_config.speech_synthesis_voice_name = VOICE_NAME
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None,
    )
    ssml = (
        "<speak version='1.0' "
        "xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='pl-PL'>"
        f"<voice name='{VOICE_NAME}'>"
        f"<lang xml:lang='pl-PL'>{escape(text)}</lang>"
        "</voice></speak>"
    )
    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return bytes(result.audio_data)

    details = result.cancellation_details
    message = f"Speech synthesis was canceled: {details.reason}"
    if details.reason == speechsdk.CancellationReason.Error:
        message = f"{message}. {details.error_details}"
    raise HTTPException(status_code=502, detail=message)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    history: str = Form("[]"),
) -> dict[str, str]:
    try:
        parsed_history = history_adapter.validate_json(history)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail="Invalid chat history.") from exc

    audio_bytes = await audio.read(MAX_AUDIO_BYTES + 1)
    if len(audio_bytes) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio must be 10 MB or smaller.")
    if not audio_bytes.startswith(b"RIFF") or audio_bytes[8:12] != b"WAVE":
        raise HTTPException(status_code=415, detail="Audio must be a WAV file.")

    transcript = transcribe_wav(audio_bytes)
    reply = generate_reply(transcript, parsed_history)
    reply_audio = synthesize_reply(reply)
    return {
        "transcript": transcript,
        "reply": reply,
        "audio": base64.b64encode(reply_audio).decode("ascii"),
    }
