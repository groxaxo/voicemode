---
description: Install VoiceMode and voice services
agent: build
allowed-tools: Bash(uvx:*), Bash(voicemode:*), Bash(brew:*), Bash(apt:*), Bash(dnf:*)
---

# Install VoiceMode Services

Install VoiceMode and all dependencies needed for voice conversations in OpenCode.

## Quick Install

For a fast, fully automated installation:

```bash
# Install VoiceMode CLI and dependencies
uvx voice-mode-install --yes

# Install local services (recommended for Apple Silicon)
voicemode service install whisper
voicemode service install kokoro
```

## What Gets Installed

| Component | Size | Purpose |
|-----------|------|---------|
| FFmpeg | ~50MB | Audio processing |
| VoiceMode CLI | ~10MB | Command-line tools and Python package |
| Whisper.cpp | ~150MB | Local speech-to-text (optional) |
| Kokoro | ~350MB | Local text-to-speech (optional) |

## Installation Steps

### 1. Install System Dependencies

**macOS:**
```bash
brew install ffmpeg portaudio
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y ffmpeg gcc libasound2-dev libportaudio2 portaudio19-dev python3-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install alsa-lib-devel ffmpeg gcc portaudio portaudio-devel python3-devel
```

### 2. Install UV Package Manager

If not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install VoiceMode

```bash
uvx voice-mode-install --yes
```

This installer:
- Checks system requirements
- Installs FFmpeg if needed (macOS via Homebrew)
- Installs VoiceMode CLI
- Configures audio devices
- Sets up local voice services

### 4. Install Local Voice Services (Optional but Recommended)

For privacy and offline use:

```bash
# Install Whisper.cpp for speech-to-text
voicemode service install whisper

# Install Kokoro for text-to-speech
voicemode service install kokoro
```

### 5. Verify Installation

```bash
# Check all services
voicemode service status

# Test voice functionality
voicemode converse "Test message"
```

## Whisper Model Selection

For Apple Silicon Macs with 16GB+ RAM, use the large-v2 model for best accuracy:

| Model | Download | RAM Usage | Accuracy |
|-------|----------|-----------|----------|
| base | ~150MB | ~300MB | Good (default) |
| small | ~460MB | ~1GB | Better |
| large-v2 | ~3GB | ~5GB | Best (recommended for 16GB+ RAM) |
| large-v3-turbo | ~1.5GB | ~3GB | Fast & accurate |

To install a specific model:

```bash
voicemode whisper install --model large-v2
```

## Cloud Services (Alternative)

If you prefer cloud-based services over local:

1. **Get an OpenAI API key**: https://platform.openai.com/api-keys

2. **Set the API key**:
```bash
export OPENAI_API_KEY="sk-..."
# Or add to your shell profile (~/.bashrc, ~/.zshrc)
```

3. **Configure VoiceMode**:
```bash
voicemode config set OPENAI_API_KEY "sk-..."
```

## Troubleshooting

### UV not found

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env  # Or restart your terminal
```

### FFmpeg not found

**macOS:**
```bash
brew install ffmpeg
```

**Linux:** See system dependency commands above

### Permission errors

Make sure you have:
- Microphone access permissions for your terminal
- Write access to `~/.voicemode/` directory

### Audio device issues

List available devices:
```bash
voicemode diag devices
```

## Platform-Specific Notes

### macOS
- Requires Homebrew for FFmpeg
- Apple Silicon recommended for local services
- Grant microphone access to Terminal.app or iTerm

### Linux (WSL2)
- Install PulseAudio packages
- Configure audio forwarding from Windows
- See: https://voice-mode.readthedocs.io/troubleshooting/wsl2/

### NixOS
```bash
nix develop github:mbailey/voicemode
# Or
nix profile install github:mbailey/voicemode
```

## Next Steps

After installation:

1. Check service status: `/voice/status`
2. Start a conversation: `/voice/converse`
3. Configure preferences: `voicemode config edit`

## See Also

- `/voice/status` - Check service status
- `/voice/converse` - Start voice conversation
- Documentation: https://voice-mode.readthedocs.io
