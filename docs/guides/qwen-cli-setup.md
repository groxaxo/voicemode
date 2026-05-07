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
  -e VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1,https://api.openai.com/v1 \
  -e VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1,https://api.openai.com/v1 \
  -e VOICEMODE_TTS_MODELS=tts-1,tts-1-hd,gpt-4o-mini-tts \
  -e VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3,whisper-1 \
  -e VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  -e VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy \
  -e VOICEMODE_DEFAULT_LOCAL_VOICE=F1 \
  -e VOICEMODE_LOCAL_TTS_PORT=8880 \
  -e VOICEMODE_LOCAL_TTS_DIR=$HOME/supertonic-express \
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
curl http://127.0.0.1:8880/health
curl http://127.0.0.1:5092/health
```
