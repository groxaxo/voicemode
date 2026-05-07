---
description: Start an ongoing voice conversation
argument-hint: [message]
---

# /voicemode:converse

Start an ongoing voice conversation with the user using the `voicemode:converse` MCP tool.

## Implementation

Use the `voicemode:converse` tool with the user's message. All parameters have sensible defaults.

## If MCP Connection Fails

If the MCP server isn't connected or the tool isn't available:

1. **Run the install command:**
   ```
   /voicemode:install
   ```
   This installs VoiceMode CLI, FFmpeg, and local voice services.

2. **Or install manually via CLI:**
   ```bash
   uv tool install "git+https://github.com/groxaxo/voicemode.git[adapters]" --force
   voicemode status
   ```

3. **Check service status:**
   ```bash
   curl http://127.0.0.1:8880/health
   voicemode status
   ```

4. **Reconnect MCP server after install:**
   Run `/mcp`, select voicemode, click "Reconnect" (or restart Claude Code)

For complete documentation, load the `voicemode` skill.
