# Getting Started with VoiceMode

VoiceMode brings voice conversations to AI coding assistants. It works as both an MCP server for Claude Code and as a standalone CLI tool.

## What is VoiceMode?

VoiceMode provides:

- **MCP Server**: Adds voice tools to Claude Code - no installation needed
- **CLI Tool**: Use VoiceMode's tools directly from your terminal
- **Local Services**: Optional privacy-focused speech processing

## Quick Start: Using with Claude Code

The fastest way to get started is using VoiceMode with Claude Code.

### Installation

Install UV package manager (if not already installed), then run the VoiceMode installer:

```bash
# Install UV package manager (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install VoiceMode and configure services
uvx voice-mode-install

# Install VoiceMode and configure Codex automatically
uvx voice-mode-install --integrations codex

# Install VoiceMode without configuring agent CLI integrations
uvx voice-mode-install --no-integrations
```

The installer will:

- Install missing system dependencies (FFmpeg, PortAudio, etc.)
- Set up your environment for VoiceMode
- Configure local voice endpoints for Supertonic Express TTS and Parakeet STT
- Optionally configure Codex, OpenCode, Qwen CLI, or Gemini CLI MCP settings

For Claude Code, add VoiceMode separately:

```bash
claude mcp add --scope user voicemode -- uvx --refresh voice-mode
```

**Alternative UV installation methods:**
- **macOS**: `brew install uv`
- **With pip**: `pip install uv`

Learn more: [UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

### 2. Configure Your API Key

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Or add it to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.)

### 3. Verify Installation

```bash
# Check that VoiceMode is connected
claude mcp list
```

You should see `voicemode` in the list of connected servers.

### 4. Configure Permissions (Optional)

By default, Claude Code prompts for permission each time VoiceMode tools are used. To enable automatic approval, add to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__voicemode__converse",
      "mcp__voicemode__service"
    ]
  }
}
```

This allows voice conversations and service management without prompts. For more permission options, see the [Permissions Guide](../guides/permissions.md).

### 5. Start Using Voice

In Claude Code, simply type:
```
converse
```

Speak when you hear the chime, and Claude will respond with voice!

## Alternative: Using as a CLI Tool

If you want to use VoiceMode from the command line:

### Installation

```bash
# Install with pip
uv tool install voice-mode

# Or install from source in editable mode
git clone https://github.com/mbailey/voicemode
cd voicemode
uv tool install -e .
```

### Basic Usage

```bash
# Set your API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Start a voice conversation
voicemode converse
```

## Local Services

This fork defaults to local OpenAI-compatible endpoints instead of OpenAI cloud fallback:

- **TTS:** Supertonic Express at `http://127.0.0.1:8880/v1`
- **STT:** Parakeet TDT at `http://127.0.0.1:5092/v1`

```bash
# Check status of all services
voicemode status
```

### Waiting for Services

Wait for both local endpoints to be ready:

```bash
# Wait for Parakeet (port 5092)
while ! nc -z localhost 5092 2>/dev/null; do sleep 2; done
echo "Parakeet ready"

# Wait for Supertonic Express (port 8880)
while ! nc -z localhost 8880 2>/dev/null; do sleep 2; done
echo "Supertonic Express ready"
```

Learn more: [Custom Endpoints](../guides/custom-endpoints.md) | [Supertonic Express Setup](../guides/supertonic-setup.md)

## Configuration

VoiceMode works out of the box with sensible defaults. To customize:

### Select Your Voice

```bash
# Supertonic Express voices
export VOICEMODE_VOICES="F1,F2,M1"
```

Configured local voices: F1-F5 and M1-M5.

### Project-Specific Settings

Create `.voicemode.env` in your project:

```bash
export VOICEMODE_VOICES="af_nova,nova"
export VOICEMODE_TTS_SPEED=1.2
```

Learn more: [Configuration Guide](../guides/configuration.md)

## Troubleshooting

### Voice Not Working in Claude?

1. **Check MCP connection**:
   ```bash
   claude mcp list
   ```
   
2. **Verify OPENAI_API_KEY** is set in your MCP configuration

3. Add to your MCP config:
   ```json
   "env": {
     "OPENAI_API_KEY": "sk-...",
   }
   ```

### No Audio Input?

```bash
# List audio devices
voicemode diag devices

# Test TTS and STT
voicemode converse
```

### Service Issues?

```bash
# Check service status
voicemode status

# Check if service is responding
curl http://127.0.0.1:5092/health
curl http://127.0.0.1:8880/health
```

## Running VoiceMode as a Service (Advanced)

For remote access or persistent operation, run VoiceMode as a background service:

```bash
# Start the VoiceMode HTTP server
voicemode service start voicemode

# Enable auto-start at boot/login
voicemode service enable voicemode

# Check all services
voicemode service status
```

The HTTP server enables remote access from other machines on your network or via secure tunnels.

For security best practices when running remotely, see the [Configuration Guide](../guides/configuration.md#http-server-security).

## Next Steps

- **[Configuration Guide](../guides/configuration.md)** - Customize VoiceMode
- **[Development Setup](development-setup.md)** - Contribute to VoiceMode
- **[Custom Endpoints](../guides/custom-endpoints.md)** - Configure local TTS/STT endpoints
- **[CLI Reference](../reference/cli.md)** - All available commands

## Getting Help

- **GitHub Issues**: [github.com/mbailey/voicemode/issues](https://github.com/mbailey/voicemode/issues)
- **Discord**: Join our community for support

Welcome to voice-enabled AI coding! 🎙️
