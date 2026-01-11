---
description: Start a voice conversation with VoiceMode
agent: build
argument-hint: [message]
---

# Voice Conversation

Start an interactive voice conversation using VoiceMode. This command provides natural speech-to-text and text-to-speech capabilities directly within OpenCode.

## Usage

```
/voice/converse
/voice/converse Hello, what can you help me with?
```

## Implementation

Use the VoiceMode CLI to start a conversation:

```bash
# Start a voice conversation
voicemode converse
```

Or pass an initial message:

```bash
voicemode converse "$ARGUMENTS"
```

## How It Works

This command integrates VoiceMode directly into OpenCode without requiring a separate MCP server. It:

1. Uses your microphone to capture speech
2. Transcribes speech to text using Whisper (local) or OpenAI API
3. Processes your request
4. Responds with synthesized speech using Kokoro (local) or OpenAI TTS

## First-Time Setup

If VoiceMode isn't installed yet, run:

```
/voice/install
```

This will install:
- VoiceMode CLI and dependencies
- FFmpeg for audio processing
- Optional: Whisper.cpp for local speech-to-text
- Optional: Kokoro for local text-to-speech

## Service Requirements

Before using voice features, ensure services are running:

```bash
# Check service status
voicemode service status

# Start services if needed
voicemode service start whisper
voicemode service start kokoro
```

## Configuration

You can customize voice settings:

```bash
# Set preferred TTS voice
voicemode config set VOICEMODE_TTS_VOICE alloy

# Use local services preferentially
voicemode config set VOICEMODE_PREFER_LOCAL true

# Enable audio saving for debugging
voicemode config set VOICEMODE_SAVE_AUDIO true
```

## Privacy Options

VoiceMode works entirely locally when configured:

1. **Local STT**: Whisper.cpp runs on your machine
2. **Local TTS**: Kokoro synthesizes speech locally
3. **No cloud**: No data sent to external services

Alternatively, use OpenAI's API for cloud-based processing.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No microphone access | Check terminal permissions |
| Services not running | Run `voicemode service start whisper kokoro` |
| FFmpeg not found | Install with `brew install ffmpeg` (macOS) or package manager |
| OpenAI API errors | Set `OPENAI_API_KEY` or use local services |

For detailed troubleshooting, run:

```bash
voicemode diag info
voicemode diag devices
```

## See Also

- `/voice/status` - Check voice service status
- `/voice/install` - Install voice services
- Documentation: https://voice-mode.readthedocs.io
