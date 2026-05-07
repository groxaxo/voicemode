#!/usr/bin/env python3
"""
Inworld TTS Adapter - OpenAI-compatible wrapper for Inworld TTS API.

Exposes OpenAI-compatible /v1/audio/speech endpoint that proxies to Inworld TTS.
"""

import os
import io
import json
import base64
import logging
from typing import Optional, List
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("inworld-adapter")

INWORLD_API_URL = "https://api.inworld.ai/tts/v1/voice:stream"
INWORLD_API_KEY = os.getenv("INWORLD_API_KEY", "")

INWORLD_MODEL = os.getenv("INWORLD_MODEL", "inworld-tts-1.5-max")
DEFAULT_VOICE = os.getenv("INWORLD_DEFAULT_VOICE", "Blake")
DEFAULT_AUDIO_FORMAT = os.getenv("INWORLD_AUDIO_FORMAT", "MP3")

INWORLD_VOICES = [
    "Blake",
    "Sarah",
    "Ethan",
    "Luna",
    "Marcus",
    "Zoe",
    "James",
    "Emma",
    "David",
    "Sophie",
]

CONTENT_TYPE_MAP = {
    "MP3": "audio/mpeg",
    "WAV": "audio/wav",
    "OGG": "audio/ogg",
    "RAW": "audio/raw",
}


class SpeechRequest(BaseModel):
    model: str = "inworld-tts-1"
    input: str
    voice: str = DEFAULT_VOICE
    response_format: str = "mp3"
    speed: float = 1.0


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int = 1704067200
    owned_by: str = "inworld"


class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]


audio_buffer = io.BytesIO()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Inworld TTS Adapter starting on port {ADAPTER_PORT}")
    logger.info(f"Default voice: {DEFAULT_VOICE}")
    logger.info(f"Model: {INWORLD_MODEL}")
    yield
    logger.info("Inworld TTS Adapter shutting down")


app = FastAPI(title="Inworld TTS Adapter", lifespan=lifespan)

ADAPTER_HOST = os.getenv("INWORLD_ADAPTER_HOST", "0.0.0.0")
ADAPTER_PORT = int(os.getenv("INWORLD_ADAPTER_PORT", "8888"))


@app.get("/v1/models")
async def list_models():
    return ModelsResponse(
        data=[
            ModelInfo(id="inworld-tts-1"),
            ModelInfo(id="inworld-tts-1.5-max"),
        ]
    )


@app.get("/v1/voices")
async def list_voices():
    return {"voices": INWORLD_VOICES}


@app.post("/v1/audio/speech")
async def create_speech(request: SpeechRequest):
    if not INWORLD_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="INWORLD_API_KEY is required for the Inworld TTS adapter",
        )

    voice = request.voice if request.voice in INWORLD_VOICES else DEFAULT_VOICE

    audio_format = request.response_format.upper()
    if audio_format not in CONTENT_TYPE_MAP:
        audio_format = DEFAULT_AUDIO_FORMAT

    payload = {
        "text": request.input,
        "voice_id": voice,
        "audio_config": {
            "audio_encoding": audio_format,
            "speaking_rate": request.speed,
        },
        "temperature": 1.0,
        "model_id": INWORLD_MODEL,
    }

    headers = {
        "Authorization": f"Basic {INWORLD_API_KEY}",
        "Content-Type": "application/json",
    }

    logger.info(f"Proxying TTS request: voice={voice}, len={len(request.input)} chars")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                INWORLD_API_URL,
                json=payload,
                headers=headers,
            )

            if response.status_code != 200:
                logger.error(
                    f"Inworld API error: {response.status_code} - {response.text[:500]}"
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Inworld API error: {response.text[:200]}",
                )

            try:
                text = response.text
                audio_parts = []
                for line in text.strip().split("\n"):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            if "result" in data and "audioContent" in data["result"]:
                                audio_parts.append(data["result"]["audioContent"])
                        except json.JSONDecodeError:
                            continue

                if audio_parts:
                    combined_b64 = "".join(audio_parts)
                    audio_bytes = base64.b64decode(combined_b64)
                    content_type = CONTENT_TYPE_MAP.get(audio_format, "audio/mpeg")
                    logger.info(f"Decoded {len(audio_bytes)} bytes of audio")
                    return Response(
                        content=audio_bytes,
                        media_type=content_type,
                        headers={
                            "Content-Disposition": f'attachment; filename="speech.{audio_format.lower()}"'
                        },
                    )
            except Exception as e:
                logger.warning(f"Could not decode JSON response: {e}")

            content_type = CONTENT_TYPE_MAP.get(audio_format, "audio/mpeg")

            return Response(
                content=response.content,
                media_type=content_type,
                headers={
                    "Content-Disposition": f'attachment; filename="speech.{audio_format.lower()}"'
                },
            )

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Inworld API timeout")
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(
            status_code=502, detail=f"Inworld API connection error: {str(e)}"
        )


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "inworld-tts-adapter"}


def main():
    import uvicorn

    uvicorn.run(app, host=ADAPTER_HOST, port=ADAPTER_PORT)


if __name__ == "__main__":
    main()
