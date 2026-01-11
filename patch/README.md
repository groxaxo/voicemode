# OpenCode Integration Patch

This directory contains files to integrate VoiceMode directly into OpenCode as native commands.

## Quick Start

```bash
# Run the installer
./install-opencode-patch.sh
```

## Directory Structure

```
patch/
├── install-opencode-patch.sh    # Main installer script
├── commands/                     # OpenCode command definitions
│   └── voice/                   # Voice commands
│       ├── converse.md          # /voice/converse command
│       ├── install.md           # /voice/install command
│       └── status.md            # /voice/status command
├── wrappers/                    # Direct Python wrappers
│   ├── voice-converse.py       # Direct converse wrapper
│   └── voice-status.py         # Direct status wrapper
└── README.md                    # This file
```

## What Gets Installed

After running the installer:

1. **Command Definitions**: Copied to `~/.config/opencode/command/voice/`
   - Makes `/voice/converse`, `/voice/status`, `/voice/install` available in OpenCode

2. **Wrapper Scripts**: Copied to `~/.config/opencode/bin/` (optional)
   - Provides direct Python execution without MCP overhead

3. **VoiceMode Package**: Installed via pip/uv if not present
   - Core functionality for voice features

## Usage in OpenCode

```bash
# Start OpenCode
opencode

# Inside OpenCode:
/voice/install    # First time: install voice services
/voice/converse   # Start a voice conversation
/voice/status     # Check service status
```

## How It Works

The patch integrates VoiceMode using OpenCode's command system:

1. **OpenCode Command System**: Uses `.opencode/command/` directory for custom commands
2. **Direct Execution**: Commands call VoiceMode CLI or Python package directly
3. **No MCP Server**: Eliminates the need for a separate MCP server process
4. **Native Experience**: Voice features work like built-in OpenCode functionality

## Requirements

- OpenCode installed (`opencode` command available)
- Python 3.10+ with pip or uv
- System dependencies (FFmpeg, PortAudio)

## Files

### install-opencode-patch.sh

Main installer script that:
- Detects OpenCode installation
- Installs VoiceMode package
- Creates command directories
- Copies command definitions
- Sets up wrapper scripts

### commands/voice/\*.md

OpenCode command definitions in Markdown format with YAML frontmatter:

```markdown
---
description: Command description
agent: build
---

Command implementation...
```

### wrappers/\*.py

Python scripts that call VoiceMode functionality directly:
- `voice-converse.py`: Direct conversation wrapper
- `voice-status.py`: Service status checker

## Customization

### Adding Custom Commands

Create new markdown files in `commands/voice/`:

```bash
cat > commands/voice/my-command.md <<'EOF'
---
description: My custom voice command
agent: build
---

Custom implementation...
EOF
```

Run installer again to deploy.

### Modifying Existing Commands

Edit markdown files in `commands/voice/`, then:

```bash
# Redeploy
./install-opencode-patch.sh
```

## Troubleshooting

### Installer Fails

```bash
# Check OpenCode is installed
which opencode

# Verify Python environment
python3 -c "import voice_mode"
```

### Commands Not Available

```bash
# Verify files were copied
ls ~/.config/opencode/command/voice/

# Check OpenCode config directory
echo $HOME/.config/opencode
```

### Permission Errors

```bash
# Make installer executable
chmod +x install-opencode-patch.sh

# Run with appropriate permissions
./install-opencode-patch.sh
```

## See Also

- [OPENCODE_PATCH.md](../OPENCODE_PATCH.md) - Complete documentation
- [OpenCode Documentation](https://opencode.ai/docs)
- [VoiceMode Documentation](https://voice-mode.readthedocs.io)
