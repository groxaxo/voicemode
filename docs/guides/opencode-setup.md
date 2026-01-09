# OpenCode Integration Guide

This guide shows you how to integrate Real-OpenVoice with OpenCode, an open-source AI coding agent that supports multiple LLM providers through the Model Context Protocol (MCP).

## What is OpenCode?

[OpenCode](https://github.com/opencode-ai/opencode) is a powerful AI coding assistant that:

- Works with multiple LLM providers (OpenAI, Anthropic Claude, Google Gemini, and more)
- Supports the Model Context Protocol (MCP) for extensibility
- Provides a terminal UI for interactive coding sessions
- Can be integrated into your development workflow
- Is fully open-source and community-driven

## Prerequisites

Before you begin, make sure you have:

1. **OpenCode installed** - See installation options below
2. **UV package manager** - For installing Real-OpenVoice
3. **At least one AI provider API key** - OpenAI, Anthropic, or Google
4. **A microphone and speakers** - For voice interaction

## Installation

### Step 1: Install OpenCode

Choose one of the following installation methods:

#### Quick Install Script (Recommended)

```bash
curl -fsSL https://opencode.ai/install | bash
```

#### Homebrew (macOS/Linux)

```bash
brew install opencode-ai/tap/opencode
```

#### npm

```bash
npm install -g opencode-ai
```

#### Arch Linux

```bash
yay -S opencode-ai-bin
# or
paru -S opencode-ai-bin
```

#### From Source (requires Go 1.24+)

```bash
git clone https://github.com/opencode-ai/opencode.git
cd opencode
go build -o opencode
sudo mv opencode /usr/local/bin/
```

### Step 2: Install UV Package Manager

If you don't have UV installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc on macOS
```

### Step 3: Install Real-OpenVoice

#### Option A: Quick Install

```bash
uvx voice-mode-install
```

This runs the installer which sets up:
- Voice mode CLI
- System dependencies check
- Optional local voice services (Whisper, Kokoro)

#### Option B: From Repository

```bash
git clone https://github.com/groxaxo/voicemode.git
cd voicemode
uv tool install -e .
```

## Configuration

### Step 1: Set Up AI Provider API Keys

OpenCode needs at least one LLM provider configured. Export the appropriate API key:

#### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

#### Anthropic Claude

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### Google Gemini

```bash
export GEMINI_API_KEY="..."
```

**Make it permanent:** Add the export to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
```

### Step 2: Configure OpenCode with MCP

Create or edit the OpenCode configuration file:

**File location:** `~/.opencode.json` (global) or `.opencode.json` (project-specific)

#### Basic Configuration

```json
{
  "providers": {
    "openai": {
      "apiKey": "sk-..."
    },
    "anthropic": {
      "apiKey": "sk-ant-..."
    }
  },
  "agents": {
    "primary": {
      "model": "claude-3.7-sonnet"
    }
  },
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

#### Advanced Configuration with Local Services

For privacy-focused setup with local Whisper and Kokoro:

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-..."
    }
  },
  "agents": {
    "primary": {
      "model": "claude-3.7-sonnet"
    }
  },
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "VOICEMODE_TTS_BASE_URLS": "http://localhost:8080/v1,https://api.openai.com/v1",
        "VOICEMODE_STT_BASE_URLS": "http://localhost:8081/v1,https://api.openai.com/v1",
        "VOICEMODE_TTS_VOICE": "af_sarah",
        "VOICEMODE_STT_MODEL": "whisper-1",
        "VOICEMODE_SAVE_AUDIO": "true"
      }
    }
  }
}
```

### Step 3: Install Voice Services (Optional)

For local, offline voice processing:

#### Install Whisper.cpp (Speech-to-Text)

```bash
voicemode service install whisper
```

This installs and starts Whisper.cpp as a local service on port 8081.

#### Install Kokoro (Text-to-Speech)

```bash
voicemode service install kokoro
```

This installs and starts Kokoro TTS service on port 8080.

**Verify services are running:**

```bash
voicemode service status
```

See the [Whisper Setup Guide](whisper-setup.md) and [Kokoro Setup Guide](kokoro-setup.md) for more details.

## Using Voice with OpenCode

### Starting OpenCode

Launch the OpenCode terminal UI:

```bash
opencode
```

### Accessing Voice Tools

Once OpenCode is running with the MCP server configured, you can access voice tools:

#### Method 1: MCP Tool Invocation

If OpenCode exposes MCP tools directly in its interface, you can use commands like:

- `/voicemode:converse` - Start a voice conversation
- `/voicemode:status` - Check voice service status  
- `/voicemode:install` - Install voice services

#### Method 2: Via Commands

In the OpenCode interface, you may be able to invoke MCP tools through natural language:

```
"Start a voice conversation"
"Check voice mode status"
```

OpenCode will recognize these and invoke the appropriate MCP tools.

### Voice Conversation Workflow

1. **Start OpenCode**: `opencode`
2. **Invoke voice mode**: Use the appropriate method for your setup
3. **Speak naturally**: Real-OpenVoice will transcribe your speech
4. **Hear responses**: OpenCode's responses are synthesized to speech
5. **End conversation**: Press Ctrl+C or say "exit"

## How It Works

### MCP Integration Architecture

```
┌─────────────┐
│  OpenCode   │
│   (Client)  │
└──────┬──────┘
       │ MCP Protocol
       │ (stdio/JSON-RPC)
       ▼
┌─────────────────┐
│ Real-OpenVoice  │
│  (MCP Server)   │
└─────┬───────────┘
      │
      ├─────────────┐
      │             │
      ▼             ▼
┌─────────┐   ┌──────────┐
│   TTS   │   │   STT    │
│ Service │   │ Service  │
└─────────┘   └──────────┘
```

1. **OpenCode** acts as the MCP client
2. **Real-OpenVoice** runs as an MCP server providing voice tools
3. **Voice Services** (TTS/STT) can be local or cloud-based
4. All communication uses the standardized MCP protocol

### Provider Flexibility

Real-OpenVoice works with any OpenAI-compatible voice API:

**Text-to-Speech (TTS):**
- OpenAI TTS API
- Local Kokoro service
- Any compatible endpoint

**Speech-to-Text (STT):**
- OpenAI Whisper API
- Local Whisper.cpp service
- Any compatible endpoint

The system automatically tries endpoints in order, falling back as needed.

## Configuration Options

### Environment Variables

You can configure Real-OpenVoice through environment variables in the MCP server config:

```json
{
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "VOICEMODE_TTS_BASE_URLS": "url1,url2",
        "VOICEMODE_STT_BASE_URLS": "url1,url2",
        "VOICEMODE_TTS_VOICE": "alloy",
        "VOICEMODE_TTS_MODEL": "tts-1",
        "VOICEMODE_STT_MODEL": "whisper-1",
        "VOICEMODE_SAVE_AUDIO": "true",
        "VOICEMODE_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Voice Preferences

Create a `.voicemode` file in your project directory:

```yaml
tts:
  voice: "af_sarah"  # or "alloy", "echo", "fable", etc.
  model: "tts-1"
  
stt:
  model: "whisper-1"
  language: "en"

audio:
  save: true
  format: "mp3"
```

See the [Configuration Guide](configuration.md) for all options.

## Troubleshooting

### OpenCode Can't Find MCP Server

**Problem:** Voice tools not available in OpenCode

**Solutions:**
1. Verify `~/.opencode.json` exists and has correct syntax
2. Check the `mcpServers` section is properly formatted
3. Ensure UV is in your PATH: `which uvx`
4. Try running manually: `uvx --refresh voice-mode`

### Voice Tools Not Working

**Problem:** MCP server starts but voice doesn't work

**Solutions:**
1. Check API keys are set correctly
2. Verify microphone permissions for terminal/OpenCode
3. Test audio devices: `voicemode config test-audio`
4. Check service status: `voicemode service status`

### Audio Device Errors

**Problem:** "No microphone found" or "Can't access audio device"

**Solutions:**
1. **macOS:** Grant microphone permission to Terminal/iTerm in System Preferences
2. **Linux:** Check ALSA/PulseAudio configuration
3. **WSL2:** Install PulseAudio packages (see main README)
4. Verify device exists: `voicemode config list-devices`

### API Rate Limits

**Problem:** Too many API calls when using cloud services

**Solutions:**
1. Install local services: `voicemode service install whisper kokoro`
2. Configure local endpoints first in base URLs
3. Adjust silence detection timeout
4. Use `VOICEMODE_SAVE_AUDIO=false` to reduce logging overhead

### Service Won't Start

**Problem:** Whisper or Kokoro service fails to start

**Solutions:**
1. Check if port is already in use: `lsof -i :8080` (macOS/Linux)
2. Review service logs: `voicemode service logs whisper`
3. Reinstall service: `voicemode service uninstall whisper && voicemode service install whisper`
4. Check system dependencies: `voicemode service check-deps`

## Performance Tips

### Reduce Latency

1. **Use local services** - Whisper.cpp and Kokoro are faster than API calls
2. **Adjust VAD sensitivity** - Tune silence detection for your environment
3. **Choose faster models** - `tts-1` is faster than `tts-1-hd`

### Optimize for Privacy

1. **Install all local services** - No data sent to cloud
2. **Disable audio saving** - Set `VOICEMODE_SAVE_AUDIO=false`
3. **Use local models only** - Don't configure fallback API endpoints

### Balance Cost and Quality

1. **Local STT, cloud TTS** - Whisper local, OpenAI TTS for better voices
2. **Cloud STT, local TTS** - Accurate transcription, private synthesis
3. **Set budget limits** - Monitor API usage in provider dashboard

## Advanced Usage

### Multiple Projects

Use project-specific configs:

```bash
cd ~/my-project
cat > .opencode.json << 'EOF'
{
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "VOICEMODE_TTS_VOICE": "shimmer"
      }
    }
  }
}
EOF
```

### Custom Voice Endpoints

Point to your own voice services:

```json
{
  "mcpServers": {
    "voicemode": {
      "command": "uvx",
      "args": ["--refresh", "voice-mode"],
      "env": {
        "VOICEMODE_TTS_BASE_URLS": "https://my-tts.example.com/v1",
        "VOICEMODE_STT_BASE_URLS": "https://my-stt.example.com/v1"
      }
    }
  }
}
```

See [Custom Endpoints Guide](custom-endpoints.md) for details.

### Integration with CI/CD

Use voice mode in automated workflows:

```yaml
# .github/workflows/opencode.yml
name: OpenCode Voice Agent
on: [issue_comment]
jobs:
  voice:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup OpenCode
        run: |
          curl -fsSL https://opencode.ai/install | bash
          uvx voice-mode-install
      - name: Configure
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cat > ~/.opencode.json << EOF
          {
            "mcpServers": {
              "voicemode": {
                "command": "uvx",
                "args": ["voice-mode"]
              }
            }
          }
          EOF
      - name: Run OpenCode
        run: opencode
```

## Next Steps

- **Explore voice options**: [Selecting Voices](selecting-voices.md)
- **Configure pronunciation**: [Pronunciation Guide](pronunciation.md)
- **Set up local services**: [Whisper Setup](whisper-setup.md) and [Kokoro Setup](kokoro-setup.md)
- **Advanced config**: [Configuration Reference](configuration.md)

## Resources

- **OpenCode Documentation**: [opencode.ai/docs](https://opencode.ai/docs)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **OpenCode GitHub**: [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)
- **Real-OpenVoice**: [github.com/groxaxo/voicemode](https://github.com/groxaxo/voicemode)
- **Original VoiceMode**: [github.com/mbailey/voicemode](https://github.com/mbailey/voicemode)

## Contributing

Found an issue or have suggestions for the OpenCode integration?

- **File an issue**: [github.com/groxaxo/voicemode/issues](https://github.com/groxaxo/voicemode/issues)
- **Original project**: Consider contributing to [mbailey/voicemode](https://github.com/mbailey/voicemode) as well
- **OpenCode issues**: [github.com/opencode-ai/opencode/issues](https://github.com/opencode-ai/opencode/issues)
