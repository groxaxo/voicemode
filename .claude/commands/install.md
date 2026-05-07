---
description: Install VoiceMode, FFmpeg, and local voice services
allowed-tools: Bash(uvx:*), Bash(voicemode:*), Bash(brew:*), Bash(uname:*), Bash(which:*)
---

# /voicemode:install

Install VoiceMode and all dependencies needed for voice conversations.

## Quick Install (Non-Interactive)

For this fork with OpenCode/Codex and Supertonic Express:

```bash
uv tool install "git+https://github.com/groxaxo/voicemode.git[adapters]" --force
voicemode status
```

## What Gets Installed

| Component | Size | Purpose |
|-----------|------|---------|
| FFmpeg | ~50MB | Audio processing (via Homebrew) |
| VoiceMode CLI | ~10MB | Command-line tools |
| Supertonic Express | existing local service | Text-to-speech on `:8880` |
| OpenAI or Parakeet | API or local endpoint | Speech-to-text |

## Implementation

1. **Check architecture:** `uname -m` (arm64 = Apple Silicon, recommended for local services)

2. **Check what's already installed:**
   ```bash
   which voicemode  # VoiceMode CLI
   which ffmpeg     # Audio processing
   ```

3. **Install missing components:**
   ```bash
   uv tool install "git+https://github.com/groxaxo/voicemode.git[adapters]" --force
   voicemode status
   ```

4. **Verify services are running:**
   ```bash
   curl http://127.0.0.1:8880/health
   voicemode status
   ```

5. **Reconnect MCP server:**
   After installation, the VoiceMode MCP server needs to reconnect:
   - Run `/mcp` and select voicemode, then click "Reconnect", OR
   - Restart Claude Code

## Whisper Model Selection

For Apple Silicon Macs with 16GB+ RAM, the large-v2 model is recommended:

| Model | Download | RAM Usage | Accuracy |
|-------|----------|-----------|----------|
| base | ~150MB | ~300MB | Good (default) |
| small | ~460MB | ~1GB | Better |
| large-v2 | ~3GB | ~5GB | Best (recommended for 16GB+ RAM) |
| large-v3-turbo | ~1.5GB | ~3GB | Fast & accurate |

To install the recommended model:
```bash
voicemode whisper install --model large-v2
```

## Prerequisites

This install process assumes:
- **UV** - Python package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Homebrew** - macOS package manager (install: `brew.sh`)

The VoiceMode installer will install Homebrew if missing on macOS.

For local ASR on this machine, use the Parakeet TDT service in `/home/op/parakeet-tdt-0.6b-v3-fastapi-openai` on port `5092`.
