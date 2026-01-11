# OpenCode Integration - Quick Start Guide

> Get VoiceMode working in OpenCode in 5 minutes

## What You Get

After running the patch installer, you'll have voice commands integrated directly into OpenCode:

- `/voice/converse` - Start voice conversations
- `/voice/status` - Check service status
- `/voice/install` - Install voice services
- `/voice/help` - Get help
- `/voice/config` - Configure settings

## Installation (3 Steps)

### 1. Install OpenCode

```bash
curl -fsSL https://opencode.ai/install | bash
```

Or use your package manager:
```bash
brew install anomalyco/tap/opencode  # macOS/Linux
npm i -g opencode-ai@latest          # Any OS
```

### 2. Run the Patch Installer

```bash
git clone https://github.com/groxaxo/voicemode.git
cd voicemode
chmod +x patch/install-opencode-patch.sh
./patch/install-opencode-patch.sh
```

### 3. Install Voice Services

Start OpenCode and run the install command:

```bash
opencode
```

Inside OpenCode:
```
/voice/install
```

This installs:
- FFmpeg (audio processing)
- VoiceMode CLI
- Whisper.cpp (local speech-to-text)
- Kokoro (local text-to-speech)

## First Conversation

```
/voice/converse
```

That's it! VoiceMode will:
1. Speak "Hello! How can I help you?" through your speakers
2. Listen to your microphone
3. Transcribe your speech to text
4. Return the text to OpenCode for processing

## How It Works

### Traditional MCP Approach
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   OpenCode  │─────>│  MCP Server  │─────>│  VoiceMode  │
└─────────────┘      └──────────────┘      └─────────────┘
   (Client)             (stdio/IPC)          (Python)
```

### OpenCode Patch Approach (This Solution)
```
┌─────────────────────────────────────────────────────┐
│  OpenCode                                           │
│                                                     │
│  /voice/converse ──> voicemode CLI ──> VoiceMode  │
│                                                     │
└─────────────────────────────────────────────────────┘
    Native commands, direct execution
```

**Benefits:**
- ✅ Faster - no MCP server overhead
- ✅ Simpler - one less process to manage
- ✅ Native - behaves like built-in OpenCode feature
- ✅ Reliable - uses proven VoiceMode CLI

## Common Commands

### Voice Conversation
```bash
/voice/converse                          # Start conversation
/voice/converse What should I work on?   # With initial message
```

### Service Management
```bash
/voice/status                            # Check all services
/voice/install                           # Install services
```

### Configuration
```bash
/voice/config                            # View/edit config
/voice/help                              # Full documentation
```

### Using VoiceMode CLI Directly
```bash
voicemode converse                       # Start conversation
voicemode service status                 # Check services
voicemode service start whisper kokoro   # Start services
voicemode config set VOICEMODE_TTS_VOICE nova  # Set voice
```

## Troubleshooting

### Services Not Running

```bash
# Inside OpenCode
/voice/status

# If services are down, start them:
voicemode service start whisper
voicemode service start kokoro
```

### No Microphone Access

**macOS:**
- System Preferences → Privacy & Security → Microphone
- Enable Terminal.app or iTerm

**Linux:**
```bash
arecord -l  # List audio devices
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

### Command Not Found in OpenCode

```bash
# Verify files exist
ls ~/.config/opencode/command/voice/

# If empty, reinstall
cd /path/to/voicemode
./patch/install-opencode-patch.sh
```

## Configuration

### Set Default Voice

```bash
voicemode config set VOICEMODE_TTS_VOICE nova
```

Available voices: `alloy`, `nova`, `shimmer`, `echo`, `fable`, `onyx`

### Use Local Services Only

```bash
voicemode config set VOICEMODE_PREFER_LOCAL true
```

### Use Cloud Services (OpenAI)

```bash
export OPENAI_API_KEY="sk-..."
voicemode config set OPENAI_API_KEY "sk-..."
```

### Save Audio for Debugging

```bash
voicemode config set VOICEMODE_SAVE_AUDIO true
```

Audio files saved to: `~/.voicemode/audio/YYYY/MM/`

## Advanced Usage

### Custom Commands

Create custom voice commands in `~/.config/opencode/command/voice/`:

```markdown
---
description: Quick status check
agent: build
---

Check voice service status:

```bash
voicemode service status
```
```

Save as `~/.config/opencode/command/voice/quick-status.md`

Use in OpenCode: `/voice/quick-status`

### Multiple Whisper Models

```bash
# Install large-v2 model (best accuracy, needs 16GB+ RAM)
voicemode whisper install --model large-v2

# Install small model (good balance)
voicemode whisper install --model small

# List available models
voicemode whisper models
```

### Offline Mode

```bash
# Install local services
voicemode service install whisper
voicemode service install kokoro

# Configure to prefer local
voicemode config set VOICEMODE_PREFER_LOCAL true

# Disable cloud fallback
voicemode config set VOICEMODE_TTS_BASE_URLS "http://localhost:8880/v1"
voicemode config set VOICEMODE_STT_BASE_URLS "http://localhost:2022/v1"
```

## System Requirements

**Minimum:**
- OpenCode installed
- Python 3.10+
- FFmpeg
- 4GB RAM
- Microphone and speakers

**Recommended (for local services):**
- Apple Silicon Mac or Linux with 16GB+ RAM
- GPU (optional, for faster processing)

## Architecture

### Files Created by Patch

```
~/.config/opencode/
├── command/
│   └── voice/
│       ├── converse.md   # /voice/converse
│       ├── install.md    # /voice/install
│       ├── status.md     # /voice/status
│       ├── help.md       # /voice/help
│       └── config.md     # /voice/config
└── bin/
    ├── voice-converse.py # Direct Python wrapper
    └── voice-status.py   # Direct Python wrapper
```

### How Commands Work

1. User types `/voice/converse` in OpenCode
2. OpenCode reads `~/.config/opencode/command/voice/converse.md`
3. Command definition instructs OpenCode to run `voicemode converse`
4. VoiceMode CLI executes the voice interaction
5. Result is returned to OpenCode

**No MCP server needed!** Direct, fast, simple.

## Resources

- **Full Documentation**: [OPENCODE_PATCH.md](OPENCODE_PATCH.md)
- **VoiceMode Docs**: https://voice-mode.readthedocs.io
- **OpenCode Docs**: https://opencode.ai/docs
- **GitHub Issues**: https://github.com/groxaxo/voicemode/issues

## Support

Having issues? Try these steps:

1. Run diagnostics:
   ```bash
   voicemode diag info
   voicemode diag devices
   ```

2. Check logs:
   ```bash
   tail -f ~/.voicemode/logs/events/$(date +%Y-%m-%d).log
   ```

3. Reinstall services:
   ```bash
   voicemode service uninstall whisper
   voicemode service install whisper
   ```

4. Ask for help:
   - GitHub Issues: https://github.com/groxaxo/voicemode/issues
   - Original Project: https://github.com/mbailey/voicemode

## What's Next?

After you're up and running:

1. Try different voices: `/voice/config`
2. Install better Whisper models for improved accuracy
3. Create custom voice commands
4. Explore advanced configuration options

Happy coding with voice! 🎤
