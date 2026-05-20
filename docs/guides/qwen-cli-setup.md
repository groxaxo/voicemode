# Qwen CLI Setup

This guide shows how to connect VoiceMode to Qwen Code using MCP.

## Quick Start

Install VoiceMode and configure Qwen Code in one step:

```bash
uvx voice-mode-install --integrations qwen
```

This writes the VoiceMode server configuration to `~/.qwen/settings.json`.

To only configure Qwen Code:

```bash
uvx voice-mode-install --integrations qwen --integrations-only
```

Restart Qwen Code after the installer finishes.

## Manual Setup

Qwen Code also supports adding MCP servers from the CLI:

```bash
qwen mcp add voicemode voicemode \
  -s user \
  -t stdio \
  -e VOICEMODE_TTS_BASE_URLS=http://100.85.200.51:6655/v1 \
  -e VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1 \
  -e VOICEMODE_TTS_MODELS=omnivoice \
  -e VOICEMODE_TTS_MODEL=omnivoice \
  -e VOICEMODE_TTS_AUDIO_FORMAT=mp3 \
  -e VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3 \
  -e VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  -e VOICEMODE_VOICES=shimmer,onyx,echo,alloy,fable,nova,british_man,british_woman,mergy \
  -e VOICEMODE_DEFAULT_LOCAL_VOICE=shimmer \
  -e VOICEMODE_LOCAL_TTS_PORT=6655 \
  -e VOICEMODE_LOCAL_TTS_DIR=$HOME/OmniVoice-benchmark \
  -e VOICEMODE_LOCAL_STT_PORT=5092 \
  -e VOICEMODE_PREFER_LOCAL=true \
  -e VOICEMODE_ALWAYS_TRY_LOCAL=true
```

Or write the same settings directly to `~/.qwen/settings.json` under `mcpServers.voicemode`.

## Verify

```bash
qwen mcp list
voicemode status
```

## Troubleshooting

If the server appears but voice is not working, verify the local endpoints:

```bash
curl http://100.85.200.51:6655/health
curl http://127.0.0.1:5092/health
```
