# Non-English Language Support

## Overview

VoiceMode's default local stack uses Supertonic Express for TTS and Parakeet for STT. Keep provider selection automatic unless you have verified that a specific endpoint and voice support the language you need.

## Local Voices

Supertonic Express local voices:

- `F1`, `F2`, `F3`, `F4`, `F5`
- `M1`, `M2`, `M3`, `M4`, `M5`

Example:

```python
converse("Bonjour!", voice="F1", tts_provider="supertonic-express")
```

## OpenAI Voices

OpenAI voices work for many languages but may retain an American English accent:

- `nova` - Female
- `shimmer` - Female
- `alloy` - Neutral
- `echo` - Male
- `fable` - Male
- `onyx` - Male

## STT Language Handling

Parakeet is exposed through the standard OpenAI-compatible `/v1/audio/transcriptions` endpoint. Keep `VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3` unless your Parakeet service advertises a different model.

## Important Notes

1. Let VoiceMode auto-select providers for normal use.
2. Specify `voice` only when you know that voice exists on the selected TTS endpoint.
3. Never use `coral` voice.
4. Use `VOICEMODE_STT_PROMPT` for vocabulary biasing when Parakeet misrecognizes project-specific words.

## See Also

- `voicemode-parameters` - Full parameter reference
- `voicemode-quickstart` - Basic usage examples
