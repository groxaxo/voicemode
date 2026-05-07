# Supertonic Express TTS

VoiceMode uses Supertonic Express as the default local OpenAI-compatible text-to-speech endpoint.

On this machine the service is expected at:

```bash
http://127.0.0.1:8880/v1
```

Configure VoiceMode:

```bash
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy
VOICEMODE_TTS_MODELS=tts-1,tts-1-hd
VOICEMODE_TTS_AUDIO_FORMAT=mp3
VOICEMODE_LOCAL_TTS_PORT=8880
VOICEMODE_LOCAL_TTS_DIR=/home/op/supertonic-express
VOICEMODE_DEFAULT_LOCAL_VOICE=F1
```

Verify:

```bash
curl http://127.0.0.1:8880/health
curl http://127.0.0.1:8880/v1/audio/voices
```

VoiceMode sends standard OpenAI `/v1/audio/speech` requests, so Supertonic works as the local TTS provider. For a complete local stack, pair it with Parakeet TDT at `http://127.0.0.1:5092/v1`.
