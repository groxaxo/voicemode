# Codex Setup

This guide shows how to connect VoiceMode to Codex using MCP.

## Quick Start

Install VoiceMode and configure the Codex integration in one step:

```bash
uvx voice-mode-install --integrations codex
```

This installs or upgrades VoiceMode, then writes the VoiceMode MCP configuration to `~/.codex/config.toml`.

To only write the Codex integration without reinstalling VoiceMode:

```bash
uvx voice-mode-install --integrations codex --integrations-only
```

Restart Codex after the installer finishes.

## What The Installer Adds

The installer creates or updates a managed block in `~/.codex/config.toml` for:

- `mcp_servers.voicemode`
- local TTS on `http://100.85.200.51:6655/v1`
- local STT on `http://127.0.0.1:5092/v1`
- OmniVoice/Parakeet voices and model

## Manual Setup

If you want to configure Codex yourself, add VoiceMode with:

```bash
codex mcp add voicemode \
  --env VOICEMODE_TTS_BASE_URLS=http://100.85.200.51:6655/v1 \
  --env VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1 \
  --env VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_VOICES=shimmer,onyx,echo,alloy,fable,nova,british_man,british_woman,mergy \
  --env VOICEMODE_TTS_MODELS=omnivoice \
  --env VOICEMODE_TTS_MODEL=omnivoice \
  --env VOICEMODE_TTS_AUDIO_FORMAT=mp3 \
  --env VOICEMODE_DEFAULT_LOCAL_VOICE=shimmer \
  --env VOICEMODE_LOCAL_TTS_PORT=6655 \
  --env VOICEMODE_LOCAL_TTS_DIR=$HOME/OmniVoice-benchmark \
  --env VOICEMODE_LOCAL_STT_PORT=5092 \
  --env VOICEMODE_PREFER_LOCAL=true \
  --env VOICEMODE_ALWAYS_TRY_LOCAL=true \
  -- voicemode
```

Verify it:

```bash
codex mcp list
codex mcp get voicemode
```

## Troubleshooting

Check the local voice stack first:

```bash
voicemode status
curl http://100.85.200.51:6655/health
curl http://127.0.0.1:5092/health
```

If Codex still does not show VoiceMode, restart Codex so it reloads `~/.codex/config.toml`.
