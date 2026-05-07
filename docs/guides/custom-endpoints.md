# Custom OpenAI-Compatible Endpoints

VoiceMode accepts comma-separated endpoint chains for TTS and STT.

```bash
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1
VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3
```

Endpoints are tried in order. Local endpoints use a dummy key when no OpenAI key is needed.

Common local endpoints:

| Service | URL | Purpose |
| --- | --- | --- |
| Supertonic Express | `http://127.0.0.1:8880/v1` | TTS |
| Parakeet TDT | `http://127.0.0.1:5092/v1` | STT |

Supertonic voices are `F1`-`F5` and `M1`-`M5`. Set them with:

```bash
VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy
```
