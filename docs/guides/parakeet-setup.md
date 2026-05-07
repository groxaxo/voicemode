# Parakeet STT

VoiceMode uses Parakeet TDT as the default local speech-to-text endpoint. Parakeet is expected to expose an OpenAI-compatible transcription API, so it works like Whisper from VoiceMode's perspective.

Default endpoint:

```bash
http://127.0.0.1:5092/v1
```

Configure VoiceMode:

```bash
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1
VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3
VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3
VOICEMODE_LOCAL_STT_PORT=5092
VOICEMODE_LOCAL_STT_DIR=/home/op/parakeet
```

Verify:

```bash
curl http://127.0.0.1:5092/health
```

Manual transcription check:

```bash
curl -s http://127.0.0.1:5092/v1/audio/transcriptions \
  -F model=parakeet-tdt-0.6b-v3 \
  -F file=@recording.wav
```

For a complete local stack, run Parakeet with Supertonic Express:

```bash
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1
VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3
VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy
```
