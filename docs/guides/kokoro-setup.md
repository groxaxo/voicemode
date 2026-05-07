# Legacy Kokoro TTS

Kokoro support is retained for existing installations, but it is no longer the default local TTS path.

New local installs should use [Supertonic Express TTS](supertonic-setup.md):

```bash
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy
VOICEMODE_DEFAULT_LOCAL_VOICE=F1
VOICEMODE_LOCAL_TTS_DIR=/home/op/supertonic-express
```

The legacy Kokoro commands still exist for compatibility:

```bash
voicemode kokoro install
voicemode kokoro start
voicemode kokoro status
voicemode kokoro logs --follow
```

Only use this page if you are maintaining a pre-existing Kokoro deployment or explicitly want the legacy TTS service.

Legacy endpoint:

```bash
http://127.0.0.1:8880/v1
```

Legacy environment variables:

```bash
VOICEMODE_KOKORO_PORT=8880
VOICEMODE_KOKORO_MODELS_DIR=~/Models/kokoro
VOICEMODE_KOKORO_CACHE_DIR=~/.voicemode/cache/kokoro
VOICEMODE_KOKORO_DEFAULT_VOICE=af_sky
```
