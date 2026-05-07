# Legacy Whisper STT

Whisper.cpp support is retained for existing installations, but it is no longer the default local STT path.

New local installs should use [Parakeet STT](parakeet-setup.md):

```bash
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1
VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3
VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3
```

The legacy Whisper commands still exist for compatibility:

```bash
voicemode whisper install
voicemode whisper start
voicemode whisper status
voicemode whisper logs --follow
```

Only use this page if you are maintaining a pre-existing Whisper.cpp deployment or explicitly want the legacy STT service.

Legacy endpoint:

```bash
http://127.0.0.1:2022/v1
```

Legacy environment variables:

```bash
VOICEMODE_WHISPER_MODEL=large-v2
VOICEMODE_WHISPER_PORT=2022
VOICEMODE_WHISPER_LANGUAGE=auto
VOICEMODE_WHISPER_MODEL_PATH=~/.voicemode/models/whisper
```
