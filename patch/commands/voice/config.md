---
description: Configure VoiceMode settings
agent: build
---

# VoiceMode Configuration

View and modify VoiceMode configuration settings.

## Quick Commands

```bash
# View all settings
voicemode config list

# Edit configuration file
voicemode config edit

# Set a specific value
voicemode config set KEY value

# Get a specific value
voicemode config get KEY
```

## Configuration File

Location: `~/.voicemode/voicemode.env`

This file contains all VoiceMode settings in environment variable format.

## Common Settings

### TTS (Text-to-Speech)

```bash
# Voice selection
voicemode config set VOICEMODE_TTS_VOICE alloy
# Options: alloy, nova, shimmer, echo, fable, onyx

# TTS provider endpoints
voicemode config set VOICEMODE_TTS_BASE_URLS "http://localhost:8880/v1,https://api.openai.com/v1"

# TTS speed (0.25 to 4.0)
voicemode config set VOICEMODE_TTS_SPEED 1.0

# TTS model
voicemode config set VOICEMODE_TTS_MODEL tts-1
# Options: tts-1, tts-1-hd
```

### STT (Speech-to-Text)

```bash
# STT provider endpoints
voicemode config set VOICEMODE_STT_BASE_URLS "http://localhost:2022/v1,https://api.openai.com/v1"

# STT model
voicemode config set VOICEMODE_STT_MODEL whisper-1

# Audio format for STT
voicemode config set VOICEMODE_STT_AUDIO_FORMAT mp3
# Options: mp3, wav, flac, webm, opus
```

### Service Preferences

```bash
# Prefer local services over cloud
voicemode config set VOICEMODE_PREFER_LOCAL true

# OpenAI API key (for cloud services)
voicemode config set OPENAI_API_KEY "sk-..."
```

### Audio Settings

```bash
# Sample rate (Hz)
voicemode config set VOICEMODE_SAMPLE_RATE 16000

# Number of audio channels
voicemode config set VOICEMODE_CHANNELS 1

# Save audio files for debugging
voicemode config set VOICEMODE_SAVE_AUDIO true

# Audio save directory
voicemode config set VOICEMODE_AUDIO_DIR "$HOME/.voicemode/audio"
```

### Recording Settings

```bash
# Default listen duration (seconds)
voicemode config set VOICEMODE_DEFAULT_LISTEN_DURATION 60

# Minimum recording duration (seconds)
voicemode config set VOICEMODE_MIN_RECORDING_DURATION 0.5

# Disable silence detection
voicemode config set VOICEMODE_DISABLE_SILENCE_DETECTION false

# VAD aggressiveness (0-3, higher = more aggressive)
voicemode config set VOICEMODE_VAD_AGGRESSIVENESS 2

# Silence threshold (milliseconds)
voicemode config set VOICEMODE_SILENCE_THRESHOLD_MS 900
```

### Debug & Logging

```bash
# Enable debug mode
voicemode config set VOICEMODE_DEBUG true

# Enable VAD debug output
voicemode config set VOICEMODE_VAD_DEBUG true

# Event logging
voicemode config set VOICEMODE_EVENT_LOG_ENABLED true

# Event log directory
voicemode config set VOICEMODE_EVENT_LOG_DIR "$HOME/.voicemode/logs/events"

# Conversation logging
voicemode config set VOICEMODE_SAVE_TRANSCRIPTIONS true
```

### Advanced Settings

```bash
# Skip TTS (speak mode only)
voicemode config set VOICEMODE_SKIP_TTS false

# Audio feedback enabled
voicemode config set VOICEMODE_AUDIO_FEEDBACK_ENABLED true

# Metrics level (0=none, 1=basic, 2=detailed)
voicemode config set VOICEMODE_METRICS_LEVEL 1

# HTTP timeout (seconds)
voicemode config set VOICEMODE_HTTP_TIMEOUT 30
```

## Configuration Examples

### Local-Only Setup

```bash
voicemode config set VOICEMODE_PREFER_LOCAL true
voicemode config set VOICEMODE_TTS_BASE_URLS "http://localhost:8880/v1"
voicemode config set VOICEMODE_STT_BASE_URLS "http://localhost:2022/v1"
```

### Cloud-Only Setup

```bash
voicemode config set OPENAI_API_KEY "sk-..."
voicemode config set VOICEMODE_PREFER_LOCAL false
voicemode config set VOICEMODE_TTS_BASE_URLS "https://api.openai.com/v1"
voicemode config set VOICEMODE_STT_BASE_URLS "https://api.openai.com/v1"
```

### Hybrid Setup (Local with Cloud Fallback)

```bash
voicemode config set OPENAI_API_KEY "sk-..."
voicemode config set VOICEMODE_PREFER_LOCAL true
voicemode config set VOICEMODE_TTS_BASE_URLS "http://localhost:8880/v1,https://api.openai.com/v1"
voicemode config set VOICEMODE_STT_BASE_URLS "http://localhost:2022/v1,https://api.openai.com/v1"
```

### Debug Setup

```bash
voicemode config set VOICEMODE_DEBUG true
voicemode config set VOICEMODE_VAD_DEBUG true
voicemode config set VOICEMODE_SAVE_AUDIO true
voicemode config set VOICEMODE_EVENT_LOG_ENABLED true
```

## View Current Configuration

```bash
# List all settings
voicemode config list

# Get specific value
voicemode config get VOICEMODE_TTS_VOICE

# Show effective configuration (with defaults)
voicemode config show
```

## Edit Configuration File

```bash
# Open in default editor
voicemode config edit

# Open in specific editor
EDITOR=nano voicemode config edit
EDITOR=vim voicemode config edit
```

## Reset Configuration

```bash
# Reset specific setting to default
voicemode config unset VOICEMODE_TTS_VOICE

# Reset all settings (backup first!)
cp ~/.voicemode/voicemode.env ~/.voicemode/voicemode.env.backup
rm ~/.voicemode/voicemode.env
```

## Environment Variables

You can also set configuration via environment variables:

```bash
# In your shell profile (~/.bashrc, ~/.zshrc, etc.)
export VOICEMODE_TTS_VOICE=nova
export VOICEMODE_PREFER_LOCAL=true
export OPENAI_API_KEY=sk-...
```

**Note**: Environment variables take precedence over config file settings.

## Per-Project Configuration

Create a `.voicemode.env` file in your project directory:

```bash
# Project-specific settings
VOICEMODE_TTS_VOICE=alloy
VOICEMODE_PREFER_LOCAL=true
```

VoiceMode will use project settings when run from that directory.

## Configuration Priority

Settings are loaded in this order (later overrides earlier):

1. Built-in defaults
2. User config file (`~/.voicemode/voicemode.env`)
3. Project config file (`.voicemode.env`)
4. Environment variables
5. Command-line arguments

## Troubleshooting

### Config File Not Found

```bash
# Create config directory
mkdir -p ~/.voicemode

# Create empty config file
touch ~/.voicemode/voicemode.env
```

### Invalid Settings

```bash
# View config with validation
voicemode config validate

# Check logs for errors
voicemode service logs whisper
```

### Reset to Defaults

```bash
# Backup current config
cp ~/.voicemode/voicemode.env ~/.voicemode/voicemode.env.backup

# Remove config file (will use defaults)
rm ~/.voicemode/voicemode.env

# Verify defaults
voicemode config list
```

## See Also

- `/voice/help` - General help and documentation
- `/voice/status` - Check service status
- Documentation: https://voice-mode.readthedocs.io/guides/configuration/
