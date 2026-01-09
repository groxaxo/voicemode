"""Tests for custom OpenAI-compatible endpoint discovery."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone

from voice_mode.provider_discovery import ProviderRegistry, EndpointInfo, detect_provider_type
from voice_mode.providers import get_tts_client_and_voice, get_stt_client


class TestCustomEndpointDiscovery:
    """Test discovery of custom OpenAI-compatible endpoints."""
    
    @pytest.mark.asyncio
    async def test_custom_tts_endpoint_discovery(self):
        """Test that a custom TTS endpoint is properly discovered."""
        registry = ProviderRegistry()
        
        # Mock the OpenAI client for discovery
        mock_client = AsyncMock()
        mock_models_response = Mock()
        mock_models_response.data = [
            Mock(id="tts-1"),
            Mock(id="my-custom-model")
        ]
        mock_client.models.list.return_value = mock_models_response
        
        # Mock httpx for voice discovery
        with patch('voice_mode.provider_discovery.httpx.AsyncClient') as mock_httpx:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "voices": ["custom-voice-1", "custom-voice-2", "alloy"]
            }
            mock_httpx_instance = AsyncMock()
            mock_httpx_instance.__aenter__.return_value.get.return_value = mock_response
            mock_httpx.return_value = mock_httpx_instance
            
            with patch('voice_mode.provider_discovery.AsyncOpenAI', return_value=mock_client):
                # Discover custom endpoint
                await registry._discover_endpoint("tts", "https://custom-tts.example.com/v1")
        
        # Verify endpoint was registered
        endpoint_info = registry.registry["tts"].get("https://custom-tts.example.com/v1")
        assert endpoint_info is not None
        assert "tts-1" in endpoint_info.models
        assert "my-custom-model" in endpoint_info.models
        assert "custom-voice-1" in endpoint_info.voices
        assert endpoint_info.provider_type == "openai-compatible"
    
    @pytest.mark.asyncio
    async def test_custom_stt_endpoint_discovery(self):
        """Test that a custom STT endpoint is properly discovered."""
        registry = ProviderRegistry()
        
        # Mock the OpenAI client for discovery
        mock_client = AsyncMock()
        mock_models_response = Mock()
        mock_models_response.data = [
            Mock(id="whisper-1"),
            Mock(id="whisper-large-v3")
        ]
        mock_client.models.list.return_value = mock_models_response
        
        with patch('voice_mode.provider_discovery.AsyncOpenAI', return_value=mock_client):
            # Discover custom endpoint
            await registry._discover_endpoint("stt", "https://custom-stt.example.com/v1")
        
        # Verify endpoint was registered
        endpoint_info = registry.registry["stt"].get("https://custom-stt.example.com/v1")
        assert endpoint_info is not None
        assert "whisper-1" in endpoint_info.models
        assert "whisper-large-v3" in endpoint_info.models
        assert endpoint_info.provider_type == "openai-compatible"
    
    @pytest.mark.asyncio
    async def test_endpoint_without_discovery_uses_defaults(self):
        """Test that endpoints without model/voice discovery endpoints use defaults."""
        registry = ProviderRegistry()
        
        # Mock the OpenAI client that fails model listing
        mock_client = AsyncMock()
        mock_client.models.list.side_effect = Exception("Not implemented")
        
        # Mock httpx that fails voice discovery
        with patch('voice_mode.provider_discovery.httpx.AsyncClient') as mock_httpx:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_httpx_instance = AsyncMock()
            mock_httpx_instance.__aenter__.return_value.get.return_value = mock_response
            mock_httpx.return_value = mock_httpx_instance
            
            with patch('voice_mode.provider_discovery.AsyncOpenAI', return_value=mock_client):
                # Discover endpoint - should use defaults
                await registry._discover_endpoint("tts", "https://minimal-tts.example.com/v1")
        
        # Verify endpoint uses defaults
        endpoint_info = registry.registry["tts"].get("https://minimal-tts.example.com/v1")
        assert endpoint_info is not None
        # Should have default model
        assert "tts-1" in endpoint_info.models
        # Voices might be empty since discovery failed
        # That's OK - system will use configured preferences
    
    def test_custom_endpoint_type_detection(self):
        """Test that custom endpoints are detected as openai-compatible."""
        # Various custom endpoint URLs
        custom_endpoints = [
            "https://my-tts-service.example.com/v1",
            "https://tts.mydomain.com/v1",
            "http://192.168.1.100:8080/v1",
            "https://api.custom-ai.com/v1",
        ]
        
        for endpoint in custom_endpoints:
            provider_type = detect_provider_type(endpoint)
            assert provider_type == "openai-compatible", \
                f"Expected {endpoint} to be detected as openai-compatible, got {provider_type}"
    
    @pytest.mark.asyncio
    async def test_multiple_custom_endpoints_priority(self):
        """Test that multiple custom endpoints are tried in order."""
        # Create a registry with multiple custom endpoints
        registry = ProviderRegistry()
        registry._initialized = True
        
        # First endpoint has a specific voice
        registry.registry["tts"]["https://tts1.example.com/v1"] = EndpointInfo(
            base_url="https://tts1.example.com/v1",
            models=["tts-1"],
            voices=["custom-voice"],
            provider_type="openai-compatible"
        )
        
        # Second endpoint has different voices
        registry.registry["tts"]["https://tts2.example.com/v1"] = EndpointInfo(
            base_url="https://tts2.example.com/v1",
            models=["tts-1"],
            voices=["alloy", "echo"],
            provider_type="openai-compatible"
        )
        
        # Test voice selection picks the right endpoint
        with patch('voice_mode.providers.provider_registry', registry):
            with patch('voice_mode.providers.TTS_BASE_URLS', [
                'https://tts1.example.com/v1',
                'https://tts2.example.com/v1'
            ]):
                with patch('voice_mode.providers.TTS_VOICES', ['alloy']):
                    with patch('voice_mode.providers.TTS_MODELS', ['tts-1']):
                        with patch('voice_mode.providers.get_voice_preferences', return_value=['alloy']):
                            client, voice, model, endpoint = await get_tts_client_and_voice(voice="alloy")
                            
                            # Should select second endpoint which has 'alloy'
                            assert voice == "alloy"
                            assert endpoint.base_url == "https://tts2.example.com/v1"
