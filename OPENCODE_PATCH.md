# OpenCode Integration Patch

> Integrate VoiceMode directly into OpenCode as a built-in feature

This patch allows you to use VoiceMode voice interaction features as native OpenCode commands, without requiring a separate MCP server. The voice functionality behaves like it's embedded directly into OpenCode.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Available Commands](#available-commands)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

## Overview

### What This Patch Does

The OpenCode Integration Patch transforms VoiceMode from a separate MCP server into native OpenCode commands. After installation, voice features work exactly like built-in OpenCode functionality.

**Key Benefits:**

1. **Native Integration**: Voice commands appear in OpenCode's command palette
2. **Zero Latency**: Direct execution without MCP server overhead
3. **Seamless UX**: Users experience voice as a core feature, not a plugin
4. **No MCP Required**: VoiceMode functions are called directly in-process
5. **Familiar Syntax**: Uses OpenCode's slash command system (`/voice/converse`)

### Architecture

```
┌─────────────────────────────────────────────────┐
│              OpenCode                           │
│  ┌─────────────────────────────────────────┐   │
│  │   User runs: /voice/converse            │   │
│  └────────────────┬────────────────────────┘   │
│                   │                             │
│  ┌────────────────▼────────────────────────┐   │
│  │   Command Definition                    │   │
│  │   ~/.config/opencode/command/voice/     │   │
│  │   converse.md                           │   │
│  └────────────────┬────────────────────────┘   │
│                   │                             │
│  ┌────────────────▼────────────────────────┐   │
│  │   Direct Python Call                    │   │
│  │   voice_mode.tools.converse.converse_impl │
│  └────────────────┬────────────────────────┘   │
│                   │                             │
│  ┌────────────────▼────────────────────────┐   │
│  │   VoiceMode Core                        │   │
│  │   - Microphone capture                  │   │
│  │   - Whisper STT / OpenAI API            │   │
│  │   - Kokoro TTS / OpenAI API             │   │
│  │   - Audio playback                      │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘

No MCP server needed! Direct in-process execution.
```

## Installation

### Prerequisites

1. **OpenCode** installed and working
   ```bash
   curl -fsSL https://opencode.ai/install | bash
   # Or: npm i -g opencode-ai@latest
   # Or: brew install anomalyco/tap/opencode
   ```

2. **UV package manager** (for Python dependencies)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **System dependencies** (audio processing)
   ```bash
   # macOS
   brew install ffmpeg portaudio
   
   # Ubuntu/Debian
   sudo apt install -y ffmpeg gcc libasound2-dev libportaudio2 portaudio19-dev python3-dev
   
   # Fedora/RHEL
   sudo dnf install alsa-lib-devel ffmpeg gcc portaudio portaudio-devel python3-devel
   ```

### Quick Install

```bash
# Clone or navigate to the VoiceMode repository
cd /path/to/voicemode

# Run the patch installer
chmod +x patch/install-opencode-patch.sh
./patch/install-opencode-patch.sh
```

The installer will:
1. ✅ Detect your OpenCode installation
2. ✅ Install VoiceMode Python package
3. ✅ Create OpenCode command definitions
4. ✅ Set up direct-call wrappers
5. ✅ Configure OpenCode to recognize voice commands

### Manual Installation

If you prefer manual installation:

```bash
# 1. Install VoiceMode package
uv pip install -e /path/to/voicemode

# 2. Create command directory
mkdir -p ~/.config/opencode/command/voice

# 3. Copy command definitions
cp /path/to/voicemode/patch/commands/voice/*.md ~/.config/opencode/command/voice/

# 4. Copy wrapper scripts (optional)
mkdir -p ~/.config/opencode/bin
cp /path/to/voicemode/patch/wrappers/*.py ~/.config/opencode/bin/
chmod +x ~/.config/opencode/bin/*.py
```

## Usage

### First-Time Setup

After installing the patch, install voice services:

```bash
# Start OpenCode
opencode

# Inside OpenCode, run:
/voice/install
```

This installs:
- FFmpeg (audio processing)
- VoiceMode CLI
- Whisper.cpp (local speech-to-text)
- Kokoro (local text-to-speech)

### Starting a Voice Conversation

```bash
# Inside OpenCode
/voice/converse

# Or with an initial message
/voice/converse Hello, what can you help me with today?
```

The command will:
1. Speak your message (or "Hello! How can I help you?" if none provided)
2. Listen for your response via microphone
3. Transcribe your speech to text
4. Return the transcribed text to OpenCode for processing

### Checking Service Status

```bash
/voice/status
```

Shows:
- Whisper (STT) status and health
- Kokoro (TTS) status and health
- Service ports and PIDs
- Health check results

## How It Works

### Command Flow

1. **User types**: `/voice/converse Hello!`

2. **OpenCode reads**: `~/.config/opencode/command/voice/converse.md`

3. **Command executes**: The markdown file contains instructions to run:
   ```bash
   voicemode converse "Hello!"
   ```

4. **VoiceMode runs**:
   - Loads configuration
   - Initializes TTS/STT services
   - Speaks "Hello!" via speakers
   - Listens via microphone
   - Transcribes speech to text
   - Returns transcribed text

5. **OpenCode receives**: User's transcribed response and continues conversation

### Direct vs MCP Execution

**Traditional MCP Approach:**
```
OpenCode → MCP Client → stdio → MCP Server → Python Function → Result → stdio → MCP Client → OpenCode
```

**OpenCode Patch Approach:**
```
OpenCode → Command Definition → Python Function → Result → OpenCode
```

The patch eliminates multiple layers of indirection, providing:
- Faster execution
- Lower latency
- Simpler architecture
- Better error handling
- Native OpenCode experience

## Available Commands

### `/voice/converse`

Start an interactive voice conversation.

**Parameters:**
- `message` (optional): Initial message to speak

**Examples:**
```
/voice/converse
/voice/converse Tell me about this codebase
/voice/converse What should I work on next?
```

**Options:**
```bash
# Speak without waiting for response
voicemode converse "Processing your request..." --no-wait

# Use specific voice
voicemode converse "Hello" --voice nova

# Set recording duration
voicemode converse "Speak now" --duration 30
```

### `/voice/status`

Check the status of voice services.

**Example:**
```
/voice/status
```

**Output:**
```
VoiceMode Services Status
━━━━━━━━━━━━━━━━━━━━━━

Whisper (STT)
  Status: ✅ Running
  Port:   2022
  Health: Healthy

Kokoro (TTS)
  Status: ✅ Running
  Port:   8880
  Health: Healthy
```

### `/voice/install`

Install VoiceMode and voice services.

**Example:**
```
/voice/install
```

Installs:
- System dependencies (FFmpeg, etc.)
- VoiceMode CLI
- Local voice services (Whisper, Kokoro)

## Configuration

### VoiceMode Configuration

Edit configuration:
```bash
voicemode config edit
```

Configuration file: `~/.voicemode/voicemode.env`

**Key Settings:**

```bash
# TTS Voice (OpenAI compatible)
VOICEMODE_TTS_VOICE=alloy  # or: nova, shimmer, echo, fable, onyx

# Prefer local services over cloud
VOICEMODE_PREFER_LOCAL=true

# Save audio for debugging
VOICEMODE_SAVE_AUDIO=true

# STT/TTS provider URLs
VOICEMODE_TTS_BASE_URLS=http://localhost:8880/v1,https://api.openai.com/v1
VOICEMODE_STT_BASE_URLS=http://localhost:2022/v1,https://api.openai.com/v1

# OpenAI API key (for cloud services)
OPENAI_API_KEY=sk-...
```

### OpenCode Configuration

OpenCode config: `~/.config/opencode/config.json`

**Voice Command Configuration:**

```json
{
  "command": {
    "voice": {
      "description": "Voice interaction commands",
      "converse": {
        "agent": "build",
        "model": "anthropic/claude-3-5-sonnet-20241022"
      }
    }
  }
}
```

## Troubleshooting

### Command Not Found

**Problem:** `/voice/converse` says command not found

**Solution:**
```bash
# Verify command files exist
ls ~/.config/opencode/command/voice/

# If empty, reinstall
cd /path/to/voicemode
./patch/install-opencode-patch.sh
```

### VoiceMode Package Not Installed

**Problem:** Error: VoiceMode package not installed

**Solution:**
```bash
# Install from repository
cd /path/to/voicemode
uv pip install -e .

# Or install from PyPI
uv pip install voice-mode
```

### Services Not Running

**Problem:** `/voice/status` shows services not running

**Solution:**
```bash
# Start services
voicemode service start whisper
voicemode service start kokoro

# Enable auto-start
voicemode service enable whisper
voicemode service enable kokoro
```

### Microphone Access Denied

**Problem:** No microphone input

**Solution:**
- **macOS:** Grant microphone access to Terminal.app/iTerm in System Preferences → Privacy & Security → Microphone
- **Linux:** Check PulseAudio/ALSA configuration
- **WSL2:** Configure audio forwarding from Windows

### FFmpeg Not Found

**Problem:** FFmpeg not installed

**Solution:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora/RHEL
sudo dnf install ffmpeg
```

### Import Errors

**Problem:** Python import errors when running commands

**Solution:**
```bash
# Verify VoiceMode is importable
python3 -c "import voice_mode; print('OK')"

# If not, reinstall
uv pip install -e /path/to/voicemode
```

### Debugging

Enable debug output:

```bash
# Set debug mode
export VOICEMODE_DEBUG=true

# Run with verbose logging
voicemode --verbose converse
```

Check logs:
```bash
# Event logs
tail -f ~/.voicemode/logs/events/$(date +%Y-%m-%d).log

# Conversation logs
tail -f ~/.voicemode/logs/conversations/$(date +%Y-%m-%d).jsonl
```

## Uninstallation

### Remove Patch

```bash
# Remove OpenCode commands
rm -rf ~/.config/opencode/command/voice/

# Remove wrapper scripts
rm -rf ~/.config/opencode/bin/voice-*.py

# Remove VoiceMode configuration (optional)
rm -rf ~/.voicemode/
```

### Uninstall VoiceMode Package

```bash
uv pip uninstall voice-mode
```

### Uninstall Voice Services

```bash
# Stop and remove services
voicemode service stop whisper
voicemode service stop kokoro
voicemode service uninstall whisper
voicemode service uninstall kokoro
```

## Advanced Topics

### Custom Voice Commands

Create custom voice commands by adding markdown files to `~/.config/opencode/command/voice/`:

**Example:** `~/.config/opencode/command/voice/quick-check.md`

```markdown
---
description: Quick voice status check
agent: build
---

Check voice service status quickly:

```bash
voicemode service status
```
```

Usage: `/voice/quick-check`

### Integration with CI/CD

For automated testing with voice features:

```bash
# Skip TTS for CI environments
export VOICEMODE_SKIP_TTS=true

# Use mocked audio input
export VOICEMODE_MOCK_AUDIO=true
```

### Multiple OpenCode Installations

If you have multiple OpenCode installations, patch each one:

```bash
# Patch system-wide installation
sudo ./patch/install-opencode-patch.sh

# Patch user installation
./patch/install-opencode-patch.sh
```

## Support

- **Documentation**: https://voice-mode.readthedocs.io
- **Issues**: https://github.com/groxaxo/voicemode/issues
- **Original Project**: https://github.com/mbailey/voicemode

## License

MIT - Same as VoiceMode project

## Acknowledgments

- **OpenCode Team**: For creating an excellent open-source AI coding agent
- **Mike Bailey**: For the original VoiceMode project
- **Community**: For testing and feedback

---

**Note**: This patch integrates VoiceMode functionality directly into OpenCode. It is not an official OpenCode feature and is maintained separately. For official OpenCode support, visit https://opencode.ai/docs
