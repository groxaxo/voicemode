# Custom OpenAI-Compatible Endpoints

VoiceMode accepts comma-separated endpoint chains for TTS and STT.

```bash
VOICEMODE_TTS_BASE_URLS=http://100.85.200.51:6655/v1
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1
VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3
```

Endpoints are tried in order. Local endpoints use a dummy key when no OpenAI key is needed.

Common local endpoints:

| Service | URL | Purpose |
| --- | --- | --- |
| Supertonic Express | `http://100.85.200.51:6655/v1` | TTS |
| Parakeet TDT | `http://127.0.0.1:5092/v1` | STT |

Supertonic default voices include `shimmer, onyx, echo, alloy...` and can be set with:

```bash
VOICEMODE_VOICES=shimmer,onyx,echo,alloy,fable,nova,british_man,british_woman,mergy
``` 
