# Service Management Commands

VoiceMode defaults to external OpenAI-compatible local services:

```bash
# Default local STT
curl http://127.0.0.1:5092/health

# Default local TTS
curl http://127.0.0.1:8880/health

# VoiceMode provider summary
voicemode status
```

## Legacy Managed Services

The CLI still includes managed service commands for existing Whisper.cpp and Kokoro deployments. They are not part of the default local install path.

```bash
# Legacy STT service
voicemode whisper status
voicemode whisper start
voicemode whisper stop
voicemode whisper restart
voicemode whisper logs --follow

# Legacy TTS service
voicemode kokoro status
voicemode kokoro start
voicemode kokoro stop
voicemode kokoro restart
voicemode kokoro logs --follow
```

Use these only when maintaining a legacy deployment. New local installs should configure Parakeet at `http://127.0.0.1:5092/v1` and Supertonic Express at `http://127.0.0.1:8880/v1`.
