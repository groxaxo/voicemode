# Example Configuration for Custom OpenAI-Compatible Endpoints

This example shows how to configure VoiceMode to use custom OpenAI-compatible 
voice endpoints instead of (or in addition to) the default services.

## Basic Setup

Add custom endpoints to your `~/.voicemode/voicemode.env` file:

```bash
# Custom TTS endpoint
VOICEMODE_TTS_BASE_URLS=https://my-tts.example.com/v1,https://api.openai.com/v1

# Custom STT endpoint  
VOICEMODE_STT_BASE_URLS=https://my-stt.example.com/v1,https://api.openai.com/v1

# If your endpoint requires authentication
OPENAI_API_KEY=your-api-key
```

## How It Works

VoiceMode automatically discovers capabilities from your endpoints:

1. **Models Discovery** (via `GET /v1/models`)
   - VoiceMode queries this endpoint to find available models
   - Falls back to default models if endpoint doesn't support discovery

2. **Voices Discovery** (via `GET /v1/audio/voices` or `GET /v1/voices`)
   - VoiceMode queries these endpoints to find available voices
   - Falls back to configured voice preferences if discovery not available

3. **Fallback Behavior**
   - If discovery endpoints are not available, uses configured defaults
   - Configured via `VOICEMODE_TTS_MODELS` and `VOICEMODE_VOICES`

## Common Scenarios

### Scenario 1: Full OpenAI-Compatible Service

Your custom endpoint implements all OpenAI APIs including discovery:

```bash
# Just point to your endpoint
VOICEMODE_TTS_BASE_URLS=https://my-service.com/v1
VOICEMODE_STT_BASE_URLS=https://my-service.com/v1

# VoiceMode will automatically discover models and voices
```

### Scenario 2: Minimal OpenAI-Compatible Service

Your endpoint only implements core TTS/STT APIs, not discovery:

```bash
# Configure the endpoint
VOICEMODE_TTS_BASE_URLS=https://minimal-tts.com/v1

# Explicitly configure models and voices since discovery won't work
VOICEMODE_TTS_MODELS=tts-1
VOICEMODE_VOICES=alloy,echo,nova

# VoiceMode will use these configured defaults
```

### Scenario 3: Multiple Endpoints with Fallback

Use multiple endpoints with automatic fallback:

```bash
# Try local service first, then cloud, then OpenAI
VOICEMODE_TTS_BASE_URLS=http://localhost:8880/v1,https://my-tts.com/v1,https://api.openai.com/v1
VOICEMODE_STT_BASE_URLS=http://localhost:2022/v1,https://my-stt.com/v1,https://api.openai.com/v1

# Configure voice preferences (VoiceMode tries them in order)
VOICEMODE_VOICES=af_sky,custom-voice,nova,alloy
```

### Scenario 4: Different Endpoints for TTS vs STT

Use one provider for TTS and another for STT:

```bash
# Use service A for TTS
VOICEMODE_TTS_BASE_URLS=https://tts-provider-a.com/v1

# Use service B for STT
VOICEMODE_STT_BASE_URLS=https://stt-provider-b.com/v1

# Each can have its own API key if needed
OPENAI_API_KEY=shared-key-if-both-use-same-auth
```

## Required Endpoint APIs

For your custom endpoint to work with VoiceMode, it should implement:

### Text-to-Speech (TTS)
- **Required:** `POST /v1/audio/speech`
  - Input: JSON with `model`, `input` (text), `voice`, `response_format`
  - Output: Audio stream

- **Optional:** `GET /v1/models`
  - Returns list of available TTS models

- **Optional:** `GET /v1/audio/voices` or `GET /v1/voices`
  - Returns list of available voices

### Speech-to-Text (STT)
- **Required:** `POST /v1/audio/transcriptions`
  - Input: Multipart form with audio file and `model`
  - Output: JSON with `text` field

- **Optional:** `GET /v1/models`
  - Returns list of available STT models

## Testing Your Endpoint

Use the VoiceMode CLI to test your custom endpoint:

```bash
# Set your custom endpoint
export VOICEMODE_TTS_BASE_URLS=https://your-endpoint.com/v1

# Test TTS
voicemode say "Hello, testing custom endpoint"

# Test STT (record and transcribe)
voicemode transcribe

# Check what providers are detected
voicemode status
```

## Troubleshooting

### Endpoint Not Working?

1. **Check endpoint URL format:**
   - Must end with `/v1`
   - Example: `https://api.example.com/v1`

2. **Check authentication:**
   - Set `OPENAI_API_KEY` if your endpoint requires it
   - VoiceMode sends it in `Authorization: Bearer` header

3. **Check API compatibility:**
   - Endpoint must implement OpenAI TTS/STT API format
   - Test with curl first to verify it works

4. **Check discovery endpoints:**
   - If models/voices aren't detected, manually configure them
   - Use `VOICEMODE_TTS_MODELS` and `VOICEMODE_VOICES`

5. **Enable debug logging:**
   ```bash
   export VOICEMODE_DEBUG=true
   # Check logs at ~/.voicemode/logs/
   ```

## Example: Local Development Server

If you're developing your own OpenAI-compatible endpoint:

```bash
# Start your local server on port 8000
# (implement POST /v1/audio/speech and POST /v1/audio/transcriptions)

# Configure VoiceMode to use it
export VOICEMODE_TTS_BASE_URLS=http://localhost:8000/v1
export VOICEMODE_STT_BASE_URLS=http://localhost:8000/v1

# Set defaults since your dev server might not have discovery yet
export VOICEMODE_TTS_MODELS=tts-1
export VOICEMODE_VOICES=test-voice

# Test it
voicemode say "Testing local development endpoint"
```

## Additional Resources

- [OpenAI TTS API Reference](https://platform.openai.com/docs/api-reference/audio/createSpeech)
- [OpenAI STT API Reference](https://platform.openai.com/docs/api-reference/audio/createTranscription)
- [VoiceMode Configuration Guide](configuration.md)
