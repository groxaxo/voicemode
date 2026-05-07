---
description: Check the status of VoiceMode services
---

# /voicemode:status

Check the status of VoiceMode services.

## Usage

```
/voicemode:status
```

## Description

Shows the current status of VoiceMode plus local OpenAI-compatible endpoints such as Supertonic Express and Parakeet STT.

## Implementation

Use the `mcp__voicemode__service` tool:

```json
{
  "service_name": "whisper",
  "action": "status"
}
```

Check all services:

```bash
# Check Whisper (STT)
mcp__voicemode__service service_name=whisper action=status

# Check Kokoro/Supertonic-compatible TTS on port 8880
mcp__voicemode__service service_name=kokoro action=status

# Check the Supertonic Express HTTP service directly
curl http://127.0.0.1:8880/health
```

## Output

Shows for each service:
- Running status
- Resource usage
- Endpoint availability
