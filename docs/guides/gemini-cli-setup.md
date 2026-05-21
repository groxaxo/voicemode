# Gemini CLI Setup

This guide shows how to connect VoiceMode to Gemini CLI using MCP.

## Quick Start

Install VoiceMode and configure Gemini CLI in one step:

```bash
uvx voice-mode-install --integrations gemini
```

This writes the VoiceMode server configuration to `~/.gemini/settings.json`.

To only configure Gemini CLI:

```bash
uvx voice-mode-install --integrations gemini --integrations-only
```

Restart Gemini CLI after the installer finishes.

## Manual Setup

Gemini CLI supports MCP management from the command line:

```bash
gemini mcp add voicemode voicemode \
  --scope user \
  --env VOICEMODE_TTS_BASE_URLS=http://100.85.200.51:6655/v1 \
  --env VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1 \
  --env VOICEMODE_TTS_MODELS=omnivoice \
  --env VOICEMODE_TTS_MODEL=omnivoice \
  --env VOICEMODE_TTS_AUDIO_FORMAT=mp3 \
  --env VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_VOICES=shimmer,onyx,echo,alloy,fable,nova,british_man,british_woman,mergy \
  --env VOICEMODE_DEFAULT_LOCAL_VOICE=shimmer \
  --env VOICEMODE_LOCAL_TTS_PORT=6655 \
  --env VOICEMODE_LOCAL_TTS_DIR=$HOME/OmniVoice-benchmark \
  --env VOICEMODE_LOCAL_STT_PORT=5092 \
  --env VOICEMODE_PREFER_LOCAL=true \
  --env VOICEMODE_ALWAYS_TRY_LOCAL=true
```

Or add the same server directly in `~/.gemini/settings.json` under `mcpServers.voicemode`.

## Verify

```bash
gemini mcp list
voicemode status
```

## Troubleshooting

If Gemini CLI can see the server but speech fails, check:

```bash
curl http://100.85.200.51:6655/health
curl http://127.0.0.1:5092/health
```
