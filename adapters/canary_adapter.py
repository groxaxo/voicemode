#!/usr/bin/env python3
"""
Canary STT Adapter - OpenAI-compatible wrapper for onnx-asr (Canary 180M Flash).

Exposes OpenAI-compatible /v1/audio/transcriptions endpoint.
Auto-detects Spanish vs English based on text content.
"""

import os
import io
import re
import logging
import tempfile
from typing import Optional
from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("canary-adapter")

ADAPTER_HOST = os.getenv("CANARY_ADAPTER_HOST", "0.0.0.0")
ADAPTER_PORT = int(os.getenv("CANARY_ADAPTER_PORT", "5092"))
DEFAULT_LANGUAGE = os.getenv("CANARY_DEFAULT_LANGUAGE", "en")

SPANISH_CHARS = re.compile(r"[áéíóúüñ¿¡ÁÉÍÓÚÜÑ]", re.IGNORECASE)
SPANISH_WORDS = {
    "hola",
    "gracias",
    "buenos",
    "buenas",
    "como",
    "estas",
    "muy",
    "bien",
    "por",
    "favor",
    "señor",
    "señora",
    "niño",
    "niña",
    "mañana",
    "tarde",
    "noche",
    "agua",
    "comida",
    "casa",
    "trabajo",
    "dinero",
    "tiempo",
    "amigo",
    "amiga",
    "familia",
    "madre",
    "padre",
    "hermano",
    "hermana",
}

asr_model = None


def detect_spanish(text: str) -> bool:
    if SPANISH_CHARS.search(text):
        return True
    words = set(text.lower().split())
    if words & SPANISH_WORDS:
        return True
    return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    global asr_model
    import onnx_asr

    logger.info(f"Canary STT Adapter starting on {ADAPTER_HOST}:{ADAPTER_PORT}")
    logger.info("Loading Canary 180M Flash model...")

    asr_model = onnx_asr.load_model("istupakov/canary-180m-flash-onnx")
    logger.info("Model loaded successfully!")

    yield

    logger.info("Canary STT Adapter shutting down")


app = FastAPI(title="Canary STT Adapter", lifespan=lifespan)


class TranscriptionResponse(BaseModel):
    text: str


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int = 1704067200
    owned_by: str = "nvidia-canary"


class ModelsResponse(BaseModel):
    object: str = "list"
    data: list


@app.get("/v1/models")
async def list_models():
    return ModelsResponse(
        data=[
            ModelInfo(id="canary-180m-flash"),
            ModelInfo(id="whisper-1"),
        ]
    )


@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...),
    model: str = Form(default="canary-180m-flash"),
    language: Optional[str] = Form(default=None),
    response_format: str = Form(default="json"),
    prompt: Optional[str] = Form(default=None),
):
    global asr_model

    logger.info(f"Transcription request: model={model}, language={language}")

    try:
        audio_data = await file.read()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name

        try:
            detect_lang = language or DEFAULT_LANGUAGE
            result = asr_model.recognize(tmp_path, language=detect_lang)

            if isinstance(result, dict):
                text = result.get("text", str(result))
            else:
                text = str(result)

            if not language and detect_spanish(text):
                logger.info("Spanish detected, re-transcribing...")
                result_es = asr_model.recognize(tmp_path, language="es")
                if isinstance(result_es, dict):
                    text = result_es.get("text", str(result_es))
                else:
                    text = str(result_es)
                language = "es"

            logger.info(f"Transcribed ({language or detect_lang}): {text[:100]}...")

            if response_format == "text":
                return text

            return {
                "text": text,
                "language": language or detect_lang,
                "duration": None,
                "words": None,
            }

        finally:
            os.unlink(tmp_path)

    except Exception as e:
        logger.error(f"Transcription error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/audio/translations")
async def translate(
    file: UploadFile = File(...),
    model: str = Form(default="canary-180m-flash"),
    response_format: str = Form(default="json"),
):
    global model_obj

    logger.info(f"Translation request: model={model}")

    try:
        audio_data = await file.read()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name

        try:
            result = asr_model.recognize(tmp_path, language="es", target_language="en")

            if isinstance(result, dict):
                text = result.get("text", str(result))
            else:
                text = str(result)

            logger.info(f"Translated to English: {text[:100]}...")

            if response_format == "text":
                return text

            return {"text": text, "language": "en", "duration": None, "words": None}

        finally:
            os.unlink(tmp_path)

    except Exception as e:
        logger.error(f"Translation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "canary-stt-adapter",
        "model": "canary-180m-flash",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=ADAPTER_HOST, port=ADAPTER_PORT)
