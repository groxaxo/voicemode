---
description: VoiceMode help and documentation
agent: plan
---

# VoiceMode Help

Quick reference for using VoiceMode voice features in OpenCode.

## Available Commands

### Voice Interaction
- `/voice/converse` - Start a voice conversation
- `/voice/converse [message]` - Start conversation with initial message

### Service Management
- `/voice/status` - Check voice service status
- `/voice/install` - Install VoiceMode and voice services

### Configuration
- `/voice/config` - View and edit VoiceMode configuration
- `/voice/help` - This help message

## Quick Start

**First time setup:**
```
/voice/install
```

**Start talking:**
```
/voice/converse
```

**Check if services are running:**
```
/voice/status
```

## Common Tasks

### Voice Conversation Basics

```bash
# Simple conversation
/voice/converse

# Conversation with specific message
/voice/converse What can you help me with?
```

The command will:
1. Speak your message through speakers
2. Listen via microphone
3. Transcribe your speech to text
4. Return transcription to OpenCode

### Service Troubleshooting

If voice features aren't working:

```bash
# 1. Check service status
voicemode service status

# 2. Start services if not running
voicemode service start whisper
voicemode service start kokoro

# 3. View logs if errors occur
voicemode service logs whisper
voicemode service logs kokoro

# 4. Restart services
voicemode service restart whisper kokoro
```

### Configuration

View current settings:
```bash
voicemode config list
```

Common settings:
```bash
# Set preferred TTS voice
voicemode config set VOICEMODE_TTS_VOICE alloy

# Prefer local services over cloud
voicemode config set VOICEMODE_PREFER_LOCAL true

# Save audio for debugging
voicemode config set VOICEMODE_SAVE_AUDIO true
```

Edit config file directly:
```bash
voicemode config edit
```

## Service Architecture

VoiceMode uses two main services:

1. **Whisper (STT)** - Speech-to-Text
   - Port: 2022
   - Purpose: Transcribe microphone input
   - Options: Local (Whisper.cpp) or Cloud (OpenAI API)

2. **Kokoro (TTS)** - Text-to-Speech
   - Port: 8880
   - Purpose: Synthesize voice responses
   - Options: Local (Kokoro) or Cloud (OpenAI API)

## Privacy Options

### Full Local Processing

```bash
# Install local services
voicemode service install whisper
voicemode service install kokoro

# Configure to prefer local
voicemode config set VOICEMODE_PREFER_LOCAL true
```

Benefits:
- ✅ No data sent to cloud
- ✅ Works offline
- ✅ Faster after first load
- ✅ No API costs

### Cloud Processing

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-..."
voicemode config set OPENAI_API_KEY "sk-..."

# Disable local preference
voicemode config set VOICEMODE_PREFER_LOCAL false
```

Benefits:
- ✅ No local installation needed
- ✅ Always up-to-date models
- ✅ Lower resource usage

## Diagnostics

### System Information

```bash
# Full system diagnostic
voicemode diag info

# Audio device information
voicemode diag devices

# Check dependencies
voicemode deps
```

### Logs

VoiceMode logs are stored in `~/.voicemode/logs/`:

```bash
# Event logs
tail -f ~/.voicemode/logs/events/$(date +%Y-%m-%d).log

# Conversation logs
tail -f ~/.voicemode/logs/conversations/$(date +%Y-%m-%d).jsonl
```

### Debug Mode

```bash
# Enable debug output
export VOICEMODE_DEBUG=true

# Save all audio
export VOICEMODE_SAVE_AUDIO=true

# Run with verbose logging
voicemode --verbose converse
```

## Advanced Features

### Voice Selection

Available TTS voices (OpenAI-compatible):

- `alloy` - Neutral, balanced
- `nova` - Warm, friendly
- `shimmer` - Clear, professional
- `echo` - Calm, measured
- `fable` - Expressive, dynamic
- `onyx` - Deep, authoritative

Set default voice:
```bash
voicemode config set VOICEMODE_TTS_VOICE nova
```

### Custom Voice Providers

VoiceMode works with any OpenAI-compatible endpoint:

```bash
# Add custom TTS endpoint
voicemode config set VOICEMODE_TTS_BASE_URLS "http://custom:8080/v1,https://api.openai.com/v1"

# Add custom STT endpoint
voicemode config set VOICEMODE_STT_BASE_URLS "http://custom:8081/v1,https://api.openai.com/v1"
```

### Recording Duration

Control how long VoiceMode listens:

```bash
# Listen for 30 seconds max
voicemode converse --duration 30

# Default is 60 seconds
```

### Silence Detection

VoiceMode automatically stops recording when you stop speaking:

```bash
# Disable silence detection (record full duration)
voicemode config set VOICEMODE_DISABLE_SILENCE_DETECTION true

# Adjust sensitivity (0-3, higher = more aggressive)
voicemode config set VOICEMODE_VAD_AGGRESSIVENESS 2
```

## Troubleshooting

### No Microphone Access

**macOS:**
- Open System Preferences → Privacy & Security → Microphone
- Enable access for Terminal.app or iTerm

**Linux:**
```bash
# Check audio devices
arecord -l

# Test recording
arecord -d 3 test.wav && aplay test.wav
```

**WSL2:**
```bash
# Install PulseAudio
sudo apt install pulseaudio pulseaudio-utils

# Configure WSL audio forwarding
# See: https://voice-mode.readthedocs.io/troubleshooting/wsl2/
```

### FFmpeg Not Found

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora/RHEL
sudo dnf install ffmpeg
```

### Services Won't Start

```bash
# Check logs
voicemode service logs whisper

# Verify installation
voicemode deps

# Reinstall service
voicemode service uninstall whisper
voicemode service install whisper
```

### Import Errors

```bash
# Verify VoiceMode is installed
python3 -c "import voice_mode; print('OK')"

# If not, reinstall
uvx voice-mode-install --yes
```

## Resources

- **Full Documentation**: https://voice-mode.readthedocs.io
- **OpenCode Patch Guide**: See OPENCODE_PATCH.md in repository
- **Troubleshooting**: https://voice-mode.readthedocs.io/troubleshooting/
- **Configuration Reference**: https://voice-mode.readthedocs.io/guides/configuration/

## Support

- **GitHub Issues**: https://github.com/groxaxo/voicemode/issues
- **Original Project**: https://github.com/mbailey/voicemode
- **OpenCode Docs**: https://opencode.ai/docs

## Tips

1. **First run is slow**: Model downloads take 2-5 minutes, then instant
2. **Speak clearly**: Position microphone ~6-12 inches away
3. **Quiet environment**: Background noise affects transcription quality
4. **Use headphones**: Prevents feedback loop with TTS
5. **Check status first**: Run `/voice/status` before starting conversations
