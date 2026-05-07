# OpenCode Setup

This guide shows how to connect VoiceMode to OpenCode using MCP.

## Quick Start

Install VoiceMode and configure OpenCode in one step:

```bash
uvx voice-mode-install --integrations opencode
```

This installs or upgrades VoiceMode, then writes the VoiceMode MCP configuration to `~/.config/opencode/opencode.json`.

To only configure OpenCode:

```bash
uvx voice-mode-install --integrations opencode --integrations-only
```

Restart OpenCode after the installer finishes.

## What The Installer Writes

The installer adds this shape under `mcp.voicemode`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "voicemode": {
      "type": "local",
      "enabled": true,
      "command": ["voicemode"],
      "environment": {
        "VOICEMODE_TTS_BASE_URLS": "http://127.0.0.1:8880/v1",
        "VOICEMODE_STT_BASE_URLS": "http://127.0.0.1:5092/v1"
      }
    }
  }
}
```

The actual installer writes the full local stack configuration, including model lists, preferred voice, and local-first behavior.

## Manual Setup

Create or edit `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "voicemode": {
      "type": "local",
      "enabled": true,
      "command": ["voicemode"],
      "environment": {
        "VOICEMODE_TTS_BASE_URLS": "http://127.0.0.1:8880/v1",
        "VOICEMODE_STT_BASE_URLS": "http://127.0.0.1:5092/v1",
        "VOICEMODE_TTS_MODELS": "tts-1,tts-1-hd,gpt-4o-mini-tts",
        "VOICEMODE_STT_MODELS": "parakeet-tdt-0.6b-v3",
        "VOICEMODE_STT_MODEL": "parakeet-tdt-0.6b-v3",
        "VOICEMODE_VOICES": "F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy",
        "VOICEMODE_DEFAULT_LOCAL_VOICE": "F1",
        "VOICEMODE_LOCAL_TTS_PORT": "8880",
        "VOICEMODE_LOCAL_TTS_DIR": "/home/your-user/supertonic-express",
        "VOICEMODE_LOCAL_STT_PORT": "5092",
        "VOICEMODE_PREFER_LOCAL": "true",
        "VOICEMODE_ALWAYS_TRY_LOCAL": "true"
      }
    }
  }
}
```

Replace `/home/your-user/supertonic-express` with your actual home directory if needed.

## Verify

```bash
opencode mcp list
voicemode status
```

## Troubleshooting

Check the local services first:

```bash
curl http://127.0.0.1:8880/health
curl http://127.0.0.1:5092/health
```

If OpenCode still does not see VoiceMode, verify that `~/.config/opencode/opencode.json` is valid JSON and restart OpenCode.
