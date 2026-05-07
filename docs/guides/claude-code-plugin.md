# Claude Code Plugin

VoiceMode provides an official plugin for Claude Code that enables voice conversations directly within the CLI.

## What the Plugin Provides

The VoiceMode plugin includes:

- **MCP Server** - Full voice capabilities via the `voicemode-mcp` server
- **Slash Commands** - Quick access to common operations
- **Skill File** - Documentation and usage patterns for Claude
- **Hooks** - Sound feedback during tool execution

## Installation

### From the Plugin Marketplace

The plugin is published to the Claude Code plugin marketplace:

```bash
# Add the marketplace
claude plugin marketplace add https://github.com/mbailey/claude-plugins

# Install the plugin
claude plugin install voicemode@mbailey
```

## Prerequisites

The plugin requires VoiceMode services to be installed and running. After installing the plugin, use the install command:

```bash
/voicemode:install
```

This runs the VoiceMode installer which sets up:

- **Parakeet TDT** - Local speech-to-text endpoint at `http://127.0.0.1:5092/v1`
- **Supertonic Express** - Local text-to-speech endpoint at `http://127.0.0.1:8880/v1`
- **FFmpeg** - Audio processing (via Homebrew on macOS)

Or install VoiceMode directly using uv:

```bash
uv tool install voice-mode
voice-mode-install --integrations claude
```

## Slash Commands

| Command | Description |
|---------|-------------|
| `/voicemode:install` | Install VoiceMode and dependencies |
| `/voicemode:converse` | Start a voice conversation |
| `/voicemode:status` | Check service status |
| `/voicemode:start` | Start voice services |
| `/voicemode:stop` | Stop voice services |

### Starting a Conversation

```bash
# Start with a greeting
/voicemode:converse Hello, how can I help you today?

# Just start listening
/voicemode:converse
```

### Checking Status

```bash
/voicemode:status
```

Shows whether Parakeet (STT) and Supertonic Express (TTS) services are reachable and healthy.

## MCP Tools

Once installed, Claude has access to these MCP tools:

- `mcp__voicemode__converse` - Speak and listen for responses
- `mcp__voicemode__service` - Manage voice services

### Converse Tool Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `message` | (required) | Text for Claude to speak |
| `wait_for_response` | true | Listen for user response after speaking |
| `listen_duration_max` | 120 | Maximum recording time (seconds) |
| `voice` | auto | TTS voice name |
| `vad_aggressiveness` | 3 | Voice detection strictness (0-3) |

## Hooks and Soundfonts

The plugin includes a hook receiver that plays sounds during tool execution:

- Sounds play when tools start and complete
- Provides audio feedback during long operations
- Uses configurable soundfonts
- Toggle with `voicemode soundfonts on/off`

Hooks are automatically configured when the plugin is installed.

See the [Soundfonts Guide](soundfonts.md) for customization, sound lookup order, and troubleshooting.

## Troubleshooting

### Services Not Starting

Check individual service status:

```bash
voicemode status
curl http://127.0.0.1:5092/health
curl http://127.0.0.1:8880/health
```

View logs:

```bash
voicemode logs --tail 50
```

### No Audio Output

1. Ensure your system audio is working
2. Check that Supertonic Express is running
3. Verify FFmpeg is installed: `which ffmpeg`

### Speech Not Recognized

1. Ensure Parakeet is running
2. Check microphone permissions for Terminal/Claude Code
3. Try speaking more clearly or adjusting VAD aggressiveness

## Configuration

VoiceMode respects configuration from `~/.voicemode/voicemode.env`:

```bash
# Default local TTS voice
VOICEMODE_TTS_VOICE=F1

# Local STT endpoint and model
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1
VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3

# Local TTS endpoint
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
```

Edit configuration:

```bash
voicemode config edit
```

## Resources

- [GitHub Repository](https://github.com/mbailey/voicemode)
- [Plugin Source](https://github.com/mbailey/voicemode)

## Development

For local development, add the plugin from your local clone:

```bash
# Add plugin from local path
claude plugin marketplace add /path/to/voicemode

# Install the plugin
claude plugin install voicemode@mbailey
```
