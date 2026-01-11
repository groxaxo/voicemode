# Real-OpenVoice

> Voice interaction for AI coding assistants - OpenCode, Claude Code, and more.

## Acknowledgment

This project is a fork of [VoiceMode](https://github.com/mbailey/voicemode) by Mike Bailey. We are grateful for his original work in creating this excellent voice interaction system for AI assistants. This fork focuses on expanding compatibility to work seamlessly with OpenCode and other open-source AI coding tools while maintaining full backward compatibility with Claude Code.

[![PyPI Downloads](https://static.pepy.tech/badge/voice-mode)](https://pepy.tech/project/voice-mode)
[![PyPI Downloads](https://static.pepy.tech/badge/voice-mode/month)](https://pepy.tech/project/voice-mode)
[![PyPI Downloads](https://static.pepy.tech/badge/voice-mode/week)](https://pepy.tech/project/voice-mode)

Real-OpenVoice enables natural voice conversations with AI coding assistants. Voice isn't about replacing typing - it's about being available when typing isn't.

**Perfect for:**

- Walking to your next meeting
- Cooking while debugging
- Giving your eyes a break after hours of screen time
- Holding a coffee (or a dog)
- Any moment when your hands or eyes are busy

## See It In Action

[![VoiceMode Demo](https://img.youtube.com/vi/cYdwOD_-dQc/maxresdefault.jpg)](https://www.youtube.com/watch?v=cYdwOD_-dQc)

*Demo video from the original VoiceMode project by Mike Bailey*

## Quick Start

**Requirements:** Computer with microphone and speakers

### Option 1: OpenCode (Recommended)

[OpenCode](https://github.com/opencode-ai/opencode) is an open-source AI coding agent that works with multiple LLM providers and supports MCP (Model Context Protocol). Real-OpenVoice integrates seamlessly with OpenCode to provide voice interaction.

#### Option A: Native Integration Patch (Best Experience)

**NEW!** Install VoiceMode as native OpenCode commands - no MCP server needed!

```bash
# Clone this repository
git clone https://github.com/groxaxo/voicemode.git
cd voicemode

# Run the OpenCode integration patch
chmod +x patch/install-opencode-patch.sh
./patch/install-opencode-patch.sh
```

This integrates VoiceMode directly into OpenCode:
- ✅ Voice commands work like built-in features (`/voice/converse`, `/voice/status`)
- ✅ Zero latency - no MCP server overhead
- ✅ Seamless user experience
- ✅ Works exactly like official OpenCode functionality

**See [OPENCODE_PATCH.md](OPENCODE_PATCH.md) for complete documentation.**

#### Option B: Traditional MCP Server

Use VoiceMode as an MCP server (original approach):

**Installation Steps**

**1. Install OpenCode**

Choose your preferred installation method:

```bash
# Quick install script (Recommended)
curl -fsSL https://opencode.ai/install | bash

# Or using Homebrew (macOS/Linux)
brew install opencode-ai/tap/opencode

# Or using npm
npm install -g opencode-ai

# Or using Arch Linux
yay -S opencode-ai-bin
```

**2. Install UV Package Manager** (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**3. Install Real-OpenVoice**

```bash
# Run the installer (sets up dependencies and local voice services)
uvx voice-mode-install

# Or install from this repository
git clone https://github.com/groxaxo/voicemode.git
cd voicemode
uv tool install -e .
```

**4. Configure OpenCode with MCP**

Add Real-OpenVoice as an MCP server to OpenCode. Create or edit your OpenCode configuration file:

**Location:** `~/.opencode.json` or `.opencode.json` in your project directory

```json
{
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key-here"
      }
    }
  }
}
```

**5. Set Up Your AI Provider**

OpenCode supports multiple providers. Configure at least one:

```bash
# For OpenAI
export OPENAI_API_KEY="your-openai-key"

# For Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-key"

# For Google Gemini
export GEMINI_API_KEY="your-gemini-key"
```

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to make them permanent.

**6. Install Voice Services** (Optional but Recommended)

For local, privacy-focused voice processing:

```bash
# Start OpenCode
opencode

# In the OpenCode interface, you can now access voice tools
# Install local voice services for offline use
/voicemode:install

# Or use the MCP tool directly if available
```

Alternatively, install voice services separately:

```bash
# Install Whisper.cpp (local speech-to-text)
voicemode service install whisper

# Install Kokoro (local text-to-speech)
voicemode service install kokoro
```

**7. Start Using Voice**

Launch OpenCode and enable voice interaction:

```bash
# Start OpenCode terminal UI
opencode

# In OpenCode, trigger voice conversation
# (The exact command may vary based on your OpenCode configuration)
```

If OpenCode exposes MCP tools directly, you can use:
- `/voicemode:converse` - Start a voice conversation
- `/voicemode:status` - Check voice service status

#### OpenCode Configuration Options

**Basic Configuration** (`~/.opencode.json`):

```json
{
  "providers": {
    "openai": {"apiKey": "YOUR_OPENAI_API_KEY"},
    "anthropic": {"apiKey": "YOUR_ANTHROPIC_API_KEY"}
  },
  "agents": {
    "primary": {"model": "claude-3.7-sonnet"}
  },
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key",
        "VOICEMODE_TTS_VOICE": "alloy",
        "VOICEMODE_STT_MODEL": "whisper-1"
      }
    }
  }
}
```

**Advanced Configuration with Local Services**:

```json
{
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "VOICEMODE_TTS_BASE_URLS": "http://localhost:8080/v1,https://api.openai.com/v1",
        "VOICEMODE_STT_BASE_URLS": "http://localhost:8081/v1,https://api.openai.com/v1",
        "VOICEMODE_TTS_VOICE": "af_sarah",
        "VOICEMODE_SAVE_AUDIO": "true"
      }
    }
  }
}
```

#### How OpenCode Integration Works

Real-OpenVoice integrates with OpenCode through the Model Context Protocol (MCP):

1. **MCP Server**: Real-OpenVoice runs as an MCP server that OpenCode connects to
2. **Voice Tools**: OpenCode can invoke voice tools like `converse`, `install`, and `status`
3. **Provider Flexibility**: Works with any OpenAI-compatible voice API (OpenAI, local Whisper, local Kokoro)
4. **Seamless Experience**: Voice input/output works just like typing in OpenCode

**See the [complete OpenCode Integration Guide](docs/guides/opencode-setup.md) for detailed setup instructions, troubleshooting, and advanced configuration.**

#### Troubleshooting OpenCode Integration

| Problem | Solution |
|---------|----------|
| OpenCode can't find MCP server | Verify `~/.opencode.json` path and JSON syntax |
| Voice tools not available | Run `uvx --refresh voice-mode` to update the package |
| Audio device errors | Check microphone permissions for OpenCode/terminal |
| API key errors | Verify environment variables in OpenCode config |

### Option 2: Claude Code Plugin

For users of Claude Code, the plugin method is also fully supported:

```bash
# Add the plugin marketplace (using original VoiceMode marketplace)
claude plugin marketplace add https://github.com/mbailey/claude-plugins

# Install VoiceMode plugin
claude plugin install voicemode@mbailey

# Install dependencies (CLI, Local Voice Services)
/voicemode:install

# Start talking!
/voicemode:converse
```

### Option 3: MCP Server (Universal)

Add Real-OpenVoice as an MCP server for maximum compatibility with any MCP-compatible AI assistant:

```bash
# Install UV package manager (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the installer (sets up dependencies and local voice services)
uvx voice-mode-install

# Add to Claude Code
claude mcp add --scope user voicemode -- uvx --refresh voice-mode

# Optional: Add OpenAI API key as fallback for local services
export OPENAI_API_KEY=your-openai-key

# Start a conversation
claude converse
```

For manual setup, see the [Getting Started Guide](docs/tutorials/getting-started.md).

## Features

- **Universal AI Assistant Support** - Works with OpenCode, Claude Code, and any MCP-compatible AI assistant
- **Natural conversations** - speak naturally, hear responses immediately
- **Works offline** - optional local voice services (Whisper STT, Kokoro TTS)
- **Low latency** - fast enough to feel like a real conversation
- **Smart silence detection** - stops recording when you stop speaking
- **Privacy options** - run entirely locally or use cloud services
- **Multiple LLM providers** - OpenAI, Anthropic, Google, and more through OpenCode

## Compatibility

**AI Assistants:** 
- OpenCode (recommended - open-source, multi-provider support)
- Claude Code (full compatibility with original VoiceMode)
- Any MCP-compatible AI assistant

**Platforms:** Linux, macOS, Windows (WSL), NixOS
**Python:** 3.10-3.14

## Configuration

VoiceMode works out of the box. For customization:

```bash
# Set OpenAI API key (if using cloud services)
export OPENAI_API_KEY="your-key"

# Or configure via file
voicemode config edit
```

See the [Configuration Guide](docs/guides/configuration.md) for all options.

## Voice Services

VoiceMode works with **any OpenAI-compatible voice API endpoint**:

### Cloud Services
- **OpenAI TTS/Whisper** - Official OpenAI API (requires API key)
- **Any OpenAI-compatible endpoint** - Custom TTS/STT services

### Local Services
For privacy or offline use, install local speech services:

- **[Whisper.cpp](docs/guides/whisper-setup.md)** - Local speech-to-text
- **[Kokoro](docs/guides/kokoro-setup.md)** - Local text-to-speech with multiple voices

All services use the OpenAI API format, so VoiceMode switches seamlessly between them.

**Setup Guide:** [Using Custom OpenAI-Compatible Endpoints](docs/guides/custom-endpoints.md)

Configure endpoints via `VOICEMODE_TTS_BASE_URLS` and `VOICEMODE_STT_BASE_URLS`.


## Installation Details

<details>
<summary><strong>System Dependencies by Platform</strong></summary>

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y ffmpeg gcc libasound2-dev libasound2-plugins libportaudio2 portaudio19-dev pulseaudio pulseaudio-utils python3-dev
```

**WSL2 users**: The pulseaudio packages above are required for microphone access.

#### Fedora/RHEL

```bash
sudo dnf install alsa-lib-devel ffmpeg gcc portaudio portaudio-devel python3-devel
```

#### macOS

```bash
brew install ffmpeg node portaudio
```

#### NixOS

```bash
# Use development shell
nix develop github:mbailey/voicemode

# Or install system-wide
nix profile install github:mbailey/voicemode
```

</details>

<details>
<summary><strong>Alternative Installation Methods</strong></summary>

#### From source

```bash
git clone https://github.com/mbailey/voicemode.git
cd voicemode
uv tool install -e .
```

#### NixOS system-wide

```nix
# In /etc/nixos/configuration.nix
environment.systemPackages = [
  (builtins.getFlake "github:mbailey/voicemode").packages.${pkgs.system}.default
];
```

</details>

## Troubleshooting


| Problem | Solution |
|---------|----------|
| No microphone access | Check terminal/app permissions. WSL2 needs pulseaudio packages. |
| UV not found | Run `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| OpenAI API error | Verify `OPENAI_API_KEY` is set correctly |
| No audio output | Check system audio settings and available devices |


### Save Audio for Debugging

```bash
export VOICEMODE_SAVE_AUDIO=true
# Files saved to ~/.voicemode/audio/YYYY/MM/
```

## Documentation

- [Getting Started](docs/tutorials/getting-started.md) - Full setup guide
- **[OpenCode Integration](docs/guides/opencode-setup.md)** - Complete guide for OpenCode setup
- [Configuration](docs/guides/configuration.md) - All environment variables
- [Whisper Setup](docs/guides/whisper-setup.md) - Local speech-to-text
- [Kokoro Setup](docs/guides/kokoro-setup.md) - Local text-to-speech
- [Development Setup](docs/tutorials/development-setup.md) - Contributing guide

Full documentation: [voice-mode.readthedocs.io](https://voice-mode.readthedocs.io)

## Links

- **Original Project**: [VoiceMode by Mike Bailey](https://github.com/mbailey/voicemode) - Thank you for creating this amazing tool!
- **This Fork**: [github.com/groxaxo/voicemode](https://github.com/groxaxo/voicemode)
- **PyPI**: [pypi.org/project/voice-mode](https://pypi.org/project/voice-mode/)
- **OpenCode**: [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)

## Credits & Attribution

**Original Author:** Mike Bailey ([@mbailey](https://github.com/mbailey))
- Original Repository: [mbailey/voicemode](https://github.com/mbailey/voicemode)
- Website: [getvoicemode.com](https://getvoicemode.com)
- YouTube: [@getvoicemode](https://youtube.com/@getvoicemode)
- Twitter/X: [@getvoicemode](https://twitter.com/getvoicemode)

**This Fork Maintained By:** groxaxo
- Focus: Enhanced OpenCode compatibility and open-source AI assistant support

## License

MIT - Originally created by Mike Bailey for [Failmode](https://failmode.com)

This fork maintains the same MIT license to honor the original project's open-source spirit.

---
mcp-name: com.failmode/voicemode
