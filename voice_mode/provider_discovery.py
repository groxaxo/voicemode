"""
Provider discovery and registry management for voice-mode.

This module handles automatic discovery of TTS/STT endpoints, including:
- Health checks
- Model discovery
- Voice discovery
- Dynamic registry management
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

import httpx
from openai import AsyncOpenAI

from . import config
from .config import TTS_BASE_URLS, STT_BASE_URLS, OPENAI_API_KEY

logger = logging.getLogger("voicemode")


def detect_provider_type(base_url: str) -> str:
    """Detect provider type from base URL.
    
    This is a best-effort heuristic for logging and diagnostics.
    The system should work with any OpenAI-compatible endpoint regardless of type.
    """
    if not base_url:
        return "unknown"
    
    # Known cloud providers
    if "openai.com" in base_url:
        return "openai"
    
    # Known local services by port (common defaults)
    if ":8880" in base_url or ":8880/" in base_url:
        return "kokoro"
    elif ":2022" in base_url or ":2022/" in base_url:
        return "whisper"
    
    # Generic categorization
    if "127.0.0.1" in base_url or "localhost" in base_url:
        return "local"
    
    # Any other OpenAI-compatible endpoint
    return "openai-compatible"


def is_local_provider(base_url: str) -> bool:
    """Check if a provider URL is for a local service."""
    if not base_url:
        return False
    provider_type = detect_provider_type(base_url)
    return provider_type in ["kokoro", "whisper", "local"] or \
           "127.0.0.1" in base_url or \
           "localhost" in base_url


@dataclass
class EndpointInfo:
    """Information about a discovered endpoint."""
    base_url: str
    models: List[str]
    voices: List[str]  # Only for TTS
    provider_type: Optional[str] = None  # e.g., "openai", "kokoro", "whisper"
    last_check: Optional[str] = None  # ISO format timestamp of last attempt
    last_error: Optional[str] = None  # Last error if any


class ProviderRegistry:
    """Manages discovery and selection of voice service providers."""
    
    def __init__(self):
        self.registry: Dict[str, Dict[str, EndpointInfo]] = {
            "tts": {},
            "stt": {}
        }
        self._discovery_lock = asyncio.Lock()
        self._initialized = False
    
    async def initialize(self):
        """Initialize the registry with configured endpoints."""
        if self._initialized:
            return

        async with self._discovery_lock:
            if self._initialized:  # Double-check after acquiring lock
                return

            logger.info("Initializing provider registry...")

            # Discover TTS endpoints dynamically
            await self._discover_endpoints("tts", TTS_BASE_URLS)
            
            # Discover STT endpoints dynamically
            await self._discover_endpoints("stt", STT_BASE_URLS)

            self._initialized = True
            logger.info(f"Provider registry initialized with {len(self.registry['tts'])} TTS and {len(self.registry['stt'])} STT endpoints")
    
    async def _discover_endpoints(self, service_type: str, base_urls: List[str]):
        """Discover all endpoints for a service type."""
        tasks = []
        for url in base_urls:
            if url not in self.registry[service_type]:
                tasks.append(self._discover_endpoint(service_type, url))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for url, result in zip(base_urls, results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to discover {service_type} endpoint {url}: {result}")
                    self.registry[service_type][url] = EndpointInfo(
                        base_url=url,
                        models=[],
                        voices=[],
                        provider_type=detect_provider_type(url),
                        last_check=datetime.now(timezone.utc).isoformat(),
                        last_error=str(result)
                    )
    
    async def _discover_endpoint(self, service_type: str, base_url: str) -> None:
        """Discover capabilities of a single endpoint."""
        logger.debug(f"Discovering {service_type} endpoint: {base_url}")
        start_time = time.time()
        
        try:
            # Create OpenAI client for the endpoint
            client = AsyncOpenAI(
                api_key=OPENAI_API_KEY or "dummy-key-for-local",
                base_url=base_url,
                timeout=10.0
            )
            
            # Try to list models
            models = []
            try:
                model_response = await client.models.list()
                models = [model.id for model in model_response.data]
                logger.debug(f"Found models at {base_url}: {models}")
            except Exception as e:
                logger.debug(f"Could not list models at {base_url}: {e}")
                # Not all endpoints support /v1/models, that's OK
                # Use defaults based on service type
                if service_type == "stt":
                    # Try a minimal transcription request to check if endpoint is alive
                    try:
                        # For local endpoints, check if it responds to basic requests
                        if "127.0.0.1" in base_url or "localhost" in base_url:
                            # Local endpoints don't need auth, just check connectivity
                            async with httpx.AsyncClient(timeout=5.0) as http_client:
                                response = await http_client.get(base_url.rstrip('/v1'))
                                if response.status_code == 200:
                                    logger.debug(f"Local STT endpoint {base_url} is responding")
                                    models = ["whisper-1"]  # Default model name
                                else:
                                    raise Exception(f"STT endpoint returned status {response.status_code}")
                        else:
                            # For cloud endpoints, models.list failure likely means auth issue
                            # We'll still mark it as configured since the endpoint exists
                            models = ["whisper-1"]  # Standard whisper model name
                            logger.debug(f"Using default STT model for {base_url}")
                    except Exception as health_error:
                        logger.debug(f"STT health check failed for {base_url}: {health_error}")
                        raise health_error
                elif service_type == "tts":
                    # For TTS endpoints without model listing, use common defaults
                    if "openai.com" in base_url:
                        models = ["tts-1", "tts-1-hd", "gpt-4o-mini-tts"]
                    else:
                        # Generic OpenAI-compatible TTS endpoint
                        models = ["tts-1"]
                    logger.debug(f"Using default TTS models for {base_url}: {models}")
            
            # Ensure endpoints have at least one model
            if not models:
                if service_type == "stt":
                    models = ["whisper-1"]
                else:
                    models = ["tts-1"]
                logger.debug(f"No models discovered, using default: {models}")
            
            # For TTS, discover voices
            voices = []
            if service_type == "tts":
                voices = await self._discover_voices(base_url, client)
                logger.debug(f"Found voices at {base_url}: {voices}")
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000
            
            # Store endpoint info
            self.registry[service_type][base_url] = EndpointInfo(
                base_url=base_url,
                models=models,
                voices=voices,
                provider_type=detect_provider_type(base_url),
                last_check=datetime.now(timezone.utc).isoformat(),
                last_error=None
            )
            
            logger.info(f"Successfully discovered {service_type} endpoint {base_url} with {len(models)} models and {len(voices)} voices")
            
        except Exception as e:
            logger.warning(f"Endpoint {base_url} discovery failed: {e}")
            self.registry[service_type][base_url] = EndpointInfo(
                base_url=base_url,
                models=[],
                voices=[],
                provider_type=detect_provider_type(base_url),
                last_check=datetime.now(timezone.utc).isoformat(),
                last_error=str(e)
            )
    
    async def _discover_voices(self, base_url: str, client: AsyncOpenAI) -> List[str]:
        """Discover available voices for a TTS endpoint.
        
        Tries multiple discovery methods in order:
        1. /v1/audio/voices endpoint (custom extension)
        2. /v1/voices endpoint (alternative location)
        3. Known OpenAI voices if it's an OpenAI endpoint
        4. Empty list as fallback (system will use configured defaults)
        """
        # Try standard OpenAI-compatible voices endpoint extensions
        for voices_path in ["/audio/voices", "/voices"]:
            try:
                # Use httpx directly for the voices endpoint
                async with httpx.AsyncClient(timeout=5.0) as http_client:
                    url = f"{base_url.rstrip('/v1')}/v1{voices_path}"
                    logger.debug(f"Trying to fetch voices from {url}")
                    response = await http_client.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, dict) and "voices" in data:
                            voices = [v["id"] if isinstance(v, dict) else v for v in data["voices"]]
                            logger.info(f"Discovered {len(voices)} voices from {url}")
                            return voices
                        elif isinstance(data, list):
                            voices = [v["id"] if isinstance(v, dict) else v for v in data]
                            logger.info(f"Discovered {len(voices)} voices from {url}")
                            return voices
            except Exception as e:
                logger.debug(f"Could not fetch voices from {base_url}{voices_path}: {e}")
        
        # If it's OpenAI, use known voices (they don't expose a voices endpoint)
        if "openai.com" in base_url:
            logger.debug("Using known OpenAI voices")
            return ["alloy", "echo", "fable", "nova", "onyx", "shimmer"]
        
        # If we can't determine voices but the endpoint is healthy, return empty list
        # The system will use configured defaults instead
        logger.debug(f"No voices discovered for {base_url}, will use configured defaults")
        return []
    
    
    def get_endpoints(self, service_type: str) -> List[EndpointInfo]:
        """Get all endpoints for a service type in priority order."""
        endpoints = []

        # Return endpoints in the order they were configured
        base_urls = TTS_BASE_URLS if service_type == "tts" else STT_BASE_URLS

        for url in base_urls:
            info = self.registry[service_type].get(url)
            if info:
                endpoints.append(info)

        return endpoints

    def get_healthy_endpoints(self, service_type: str) -> List[EndpointInfo]:
        """Deprecated: Use get_endpoints instead. Returns all endpoints."""
        return self.get_endpoints(service_type)
    
    def find_endpoint_with_voice(self, voice: str) -> Optional[EndpointInfo]:
        """Find the first TTS endpoint that supports a specific voice."""
        for endpoint in self.get_endpoints("tts"):
            if voice in endpoint.voices:
                return endpoint
        return None

    def find_endpoint_with_model(self, service_type: str, model: str) -> Optional[EndpointInfo]:
        """Find the first endpoint that supports a specific model."""
        for endpoint in self.get_endpoints(service_type):
            if model in endpoint.models:
                return endpoint
        return None
    
    def get_registry_for_llm(self) -> Dict[str, Any]:
        """Get registry data formatted for LLM inspection."""
        return {
            "tts": {
                url: {
                    "models": info.models,
                    "voices": info.voices,
                    "provider_type": info.provider_type,
                    "last_check": info.last_check,
                    "last_error": info.last_error
                }
                for url, info in self.registry["tts"].items()
            },
            "stt": {
                url: {
                    "models": info.models,
                    "provider_type": info.provider_type,
                    "last_check": info.last_check,
                    "last_error": info.last_error
                }
                for url, info in self.registry["stt"].items()
            }
        }
    
    async def mark_failed(self, service_type: str, base_url: str, error: str):
        """Record that an endpoint failed.

        This updates the last_error and last_check fields for diagnostics,
        but doesn't prevent the endpoint from being tried again.
        """
        if base_url in self.registry[service_type]:
            # Update error and last check time for diagnostics
            self.registry[service_type][base_url].last_error = error
            self.registry[service_type][base_url].last_check = datetime.now(timezone.utc).isoformat()
            logger.info(f"{service_type} endpoint {base_url} failed: {error}")


# Global registry instance
provider_registry = ProviderRegistry()
