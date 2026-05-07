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
  --env VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1 \
  --env VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1 \
  --env VOICEMODE_TTS_MODELS=tts-1,tts-1-hd \
  --env VOICEMODE_TTS_AUDIO_FORMAT=mp3 \
  --env VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy \
  --env VOICEMODE_DEFAULT_LOCAL_VOICE=F1 \
  --env VOICEMODE_LOCAL_TTS_PORT=8880 \
  --env VOICEMODE_LOCAL_TTS_DIR=$HOME/supertonic-express \
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
curl http://127.0.0.1:8880/health
curl http://127.0.0.1:5092/health
```
