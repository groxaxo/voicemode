#!/usr/bin/env bash
# VoiceMode OpenCode Patch Installer
# Integrates VoiceMode directly into OpenCode as native commands

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  VoiceMode → OpenCode Integration Patch Installer       ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${BLUE}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if OpenCode is installed
check_opencode() {
    print_status "Checking for OpenCode installation..."
    
    if command -v opencode &> /dev/null; then
        OPENCODE_VERSION=$(opencode --version 2>&1 | head -1 || echo "unknown")
        print_success "OpenCode found: $OPENCODE_VERSION"
        return 0
    else
        print_error "OpenCode not found in PATH"
        echo ""
        echo "Please install OpenCode first:"
        echo "  curl -fsSL https://opencode.ai/install | bash"
        echo ""
        echo "Or using a package manager:"
        echo "  npm i -g opencode-ai@latest"
        echo "  brew install anomalyco/tap/opencode"
        echo ""
        return 1
    fi
}

# Detect OpenCode configuration directory
detect_opencode_config() {
    print_status "Detecting OpenCode configuration directory..."
    
    # Check common locations
    if [ -d "$HOME/.config/opencode" ]; then
        OPENCODE_CONFIG_DIR="$HOME/.config/opencode"
    elif [ -d "$HOME/.opencode" ]; then
        OPENCODE_CONFIG_DIR="$HOME/.opencode"
    else
        # Create default location
        OPENCODE_CONFIG_DIR="$HOME/.config/opencode"
        mkdir -p "$OPENCODE_CONFIG_DIR"
        print_warning "Created new config directory: $OPENCODE_CONFIG_DIR"
    fi
    
    print_success "Using config directory: $OPENCODE_CONFIG_DIR"
}

# Install VoiceMode package if not already installed
install_voicemode() {
    print_status "Checking VoiceMode installation..."
    
    if python3 -c "import voice_mode" 2>/dev/null; then
        print_success "VoiceMode package already installed"
    else
        print_status "Installing VoiceMode package..."
        
        # Try uv first, fall back to pip
        if command -v uv &> /dev/null; then
            uv pip install -e "$REPO_ROOT"
        elif command -v pip3 &> /dev/null; then
            pip3 install -e "$REPO_ROOT"
        else
            print_error "Neither uv nor pip3 found. Please install one of them."
            return 1
        fi
        
        print_success "VoiceMode package installed"
    fi
}

# Create command directory structure
setup_command_dirs() {
    print_status "Setting up OpenCode command directories..."
    
    COMMAND_DIR="$OPENCODE_CONFIG_DIR/command/voice"
    mkdir -p "$COMMAND_DIR"
    
    print_success "Created command directory: $COMMAND_DIR"
}

# Install wrapper scripts
install_wrappers() {
    print_status "Installing VoiceMode wrapper scripts..."
    
    WRAPPER_DIR="$OPENCODE_CONFIG_DIR/bin"
    mkdir -p "$WRAPPER_DIR"
    
    # Copy wrapper scripts
    if [ -d "$SCRIPT_DIR/wrappers" ]; then
        cp -r "$SCRIPT_DIR/wrappers/"* "$WRAPPER_DIR/" 2>/dev/null || true
        chmod +x "$WRAPPER_DIR"/*.py 2>/dev/null || true
        print_success "Installed wrapper scripts to $WRAPPER_DIR"
    else
        print_warning "Wrapper scripts not found, will be created on-demand..."
    fi
}

# Install OpenCode command definitions
install_commands() {
    print_status "Installing OpenCode voice commands..."
    
    COMMAND_DIR="$OPENCODE_CONFIG_DIR/command/voice"
    
    # Copy command definitions
    if [ -d "$SCRIPT_DIR/commands/voice" ] && [ "$(ls -A "$SCRIPT_DIR/commands/voice" 2>/dev/null)" ]; then
        cp -r "$SCRIPT_DIR/commands/voice/"* "$COMMAND_DIR/"
        print_success "Installed voice commands:"
        for cmd_file in "$COMMAND_DIR"/*.md; do
            if [ -f "$cmd_file" ]; then
                cmd_name=$(basename "$cmd_file" .md)
                echo "    /voice/$cmd_name"
            fi
        done
    else
        print_warning "Command definitions not found, creating basic commands..."
        create_basic_commands
    fi
}

# Create basic command definitions if not present
create_basic_commands() {
    COMMAND_DIR="$OPENCODE_CONFIG_DIR/command/voice"
    
    # Create converse command
    cat > "$COMMAND_DIR/converse.md" <<'EOF'
---
description: Start a voice conversation
agent: build
---

Start a voice conversation using VoiceMode.

Use the voice-mode package directly to have a conversation with the user:

```python
from voice_mode.tools.converse import converse_tool
result = converse_tool(message="$ARGUMENTS" if "$ARGUMENTS" else "Hello! How can I help you?")
```

If this fails, guide the user to install VoiceMode first:
```bash
uvx voice-mode-install --yes
```
EOF
    
    # Create status command
    cat > "$COMMAND_DIR/status.md" <<'EOF'
---
description: Check VoiceMode service status
agent: build
---

Check the status of VoiceMode services (Whisper STT, Kokoro TTS).

```bash
voicemode service status
```

This shows:
- Service running state
- Port availability
- Health check results
EOF
    
    # Create install command
    cat > "$COMMAND_DIR/install.md" <<'EOF'
---
description: Install VoiceMode services
agent: build
allowed-tools: Bash(uvx:*), Bash(voicemode:*)
---

Install VoiceMode and local voice services.

```bash
# Install VoiceMode CLI and dependencies
uvx voice-mode-install --yes

# Install local services (recommended for Apple Silicon)
voicemode service install whisper
voicemode service install kokoro
```

What gets installed:
- FFmpeg (~50MB) - Audio processing
- VoiceMode CLI (~10MB) - Command-line tools
- Whisper.cpp (~150MB) - Local speech-to-text
- Kokoro (~350MB) - Local text-to-speech
EOF
    
    print_success "Created basic voice commands"
}

# Create or update OpenCode configuration
update_opencode_config() {
    print_status "Updating OpenCode configuration..."
    
    CONFIG_FILE="$OPENCODE_CONFIG_DIR/config.json"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        # Create new config
        cat > "$CONFIG_FILE" <<'EOF'
{
  "command": {
    "voice": {
      "description": "Voice interaction commands"
    }
  }
}
EOF
        print_success "Created OpenCode configuration"
    else
        print_success "OpenCode configuration already exists"
    fi
}

# Main installation flow
main() {
    echo ""
    
    # Pre-flight checks
    if ! check_opencode; then
        exit 1
    fi
    
    echo ""
    detect_opencode_config
    
    echo ""
    install_voicemode || exit 1
    
    echo ""
    setup_command_dirs
    
    echo ""
    install_wrappers
    
    echo ""
    install_commands
    
    echo ""
    update_opencode_config
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  VoiceMode Patch Installed Successfully! ✓              ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Voice commands are now available in OpenCode:"
    echo ""
    echo "  ${BLUE}/voice/converse${NC}  - Start a voice conversation"
    echo "  ${BLUE}/voice/status${NC}    - Check voice service status"
    echo "  ${BLUE}/voice/install${NC}   - Install voice services"
    echo ""
    echo "To use voice features, first install services:"
    echo "  ${YELLOW}opencode${NC}"
    echo "  ${YELLOW}/voice/install${NC}"
    echo ""
    echo "Then start a conversation:"
    echo "  ${YELLOW}/voice/converse${NC}"
    echo ""
    echo "For more information, see: ${BLUE}$REPO_ROOT/OPENCODE_PATCH.md${NC}"
    echo ""
}

# Run main installation
main "$@"
