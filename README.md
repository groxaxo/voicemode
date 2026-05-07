# VoiceMode

VoiceMode is an MCP voice interface for Codex, Claude Code, OpenCode, and other MCP-capable agents. This fork is configured for a fast local voice stack:

- **TTS:** Supertonic Express on `http://127.0.0.1:8880/v1`
- **STT:** Parakeet TDT 0.6B v3 on `http://127.0.0.1:5092/v1`
- **Fallback:** OpenAI-compatible cloud endpoints when local services are unavailable
- **MCP tools:** `converse` and `service`

The goal is simple: talk to your coding agent with local speech generation and local transcription by default.

## Current Local Setup

On this machine the working setup is:

```bash
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1,https://api.openai.com/v1
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1,https://api.openai.com/v1
VOICEMODE_TTS_MODELS=tts-1,tts-1-hd,gpt-4o-mini-tts
VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3,whisper-1
VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3
VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy
VOICEMODE_DEFAULT_LOCAL_VOICE=F1
VOICEMODE_PREFER_LOCAL=true
VOICEMODE_ALWAYS_TRY_LOCAL=true
```

Codex is registered to run the installed `voicemode` executable as an MCP server with the same endpoint chain.

## Services

### Supertonic Express TTS

Supertonic Express provides OpenAI-compatible local text-to-speech on port `8880`.

```bash
curl http://127.0.0.1:8880/health
curl http://127.0.0.1:8880/v1/audio/voices
```

Configured voices are `F1`-`F5` and `M1`-`M5`, with OpenAI voices available as fallback.

### Parakeet TDT STT

Parakeet provides OpenAI-compatible local speech-to-text on port `5092`.

```bash
systemctl --user status parakeet-tdt.service
curl http://127.0.0.1:5092/health
```

Manual start:

```bash
conda activate parakeet-onnx
cd /home/op/parakeet-tdt-0.6b-v3-fastapi-openai
python app.py
```

The active model is `parakeet-tdt-0.6b-v3`. VoiceMode sends this model to the local endpoint and uses `whisper-1` for OpenAI fallback.

## Install

Install this fork with the local adapter entry points:

```bash
uv tool install "git+https://github.com/groxaxo/voicemode.git[adapters,canary]" --force
```

Register with Codex:

```bash
codex mcp add voicemode \
  --env VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1,https://api.openai.com/v1 \
  --env VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1,https://api.openai.com/v1 \
  --env VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3,whisper-1 \
  --env VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy \
  --env VOICEMODE_TTS_MODELS=tts-1,tts-1-hd,gpt-4o-mini-tts \
  --env VOICEMODE_DEFAULT_LOCAL_VOICE=F1 \
  --env VOICEMODE_LOCAL_TTS_PORT=8880 \
  --env VOICEMODE_LOCAL_TTS_DIR=/home/op/supertonic-express \
  --env VOICEMODE_PREFER_LOCAL=true \
  --env VOICEMODE_ALWAYS_TRY_LOCAL=true \
  -- voicemode
```

Check it:

```bash
voicemode status
codex mcp get voicemode
```

## Use

From an MCP client, call the `converse` tool. VoiceMode records your speech, transcribes through the local STT chain, sends the text to the agent, then speaks the response through the local TTS chain.

Useful commands:

```bash
voicemode status
voicemode config edit
systemctl --user restart parakeet-tdt.service
```

## Fork Additions

This fork adds and configures:

- OpenAI-compatible Inworld TTS adapter entry point: `voicemode-inworld-adapter`
- OpenAI-compatible Canary adapter entry point: `voicemode-canary-adapter`
- Supertonic Express local TTS configuration and docs
- Parakeet TDT local STT defaults, status reporting, prompts, and docs
- Codex/OpenCode-oriented MCP configuration examples

## Upstream VoiceMode

VoiceMode upstream remains the general-purpose project for voice conversations with Claude Code and other MCP agents:

- Website: [getvoicemode.com](https://getvoicemode.com)
- Upstream GitHub: [github.com/mbailey/voicemode](https://github.com/mbailey/voicemode)
- Documentation: [voice-mode.readthedocs.io](https://voice-mode.readthedocs.io)
- PyPI: [pypi.org/project/voice-mode](https://pypi.org/project/voice-mode/)

## Development

Run focused checks:

```bash
uv run --extra test python -m pytest tests/test_provider_discovery.py tests/test_provider_selection.py tests/test_service_health_checks.py -q
```

Build package:

```bash
uv build
```

## License

MIT - A [Failmode](https://failmode.com) Project

---
mcp-name: com.failmode/voicemode
