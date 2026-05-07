# VoiceMode

VoiceMode is an MCP voice interface for Codex, Claude Code, OpenCode, Qwen Code, Gemini CLI, and other MCP-capable agents. This fork is configured for a fast local voice stack:

- **TTS:** Supertonic Express on `http://127.0.0.1:8880/v1`
- **STT:** Parakeet TDT 0.6B v3 on `http://127.0.0.1:5092/v1`
- **Fallback:** none configured for Codex MCP by default
- **MCP tools:** `converse` and `service`

The goal is simple: talk to your coding agent with local speech generation and local transcription by default.

## Current Local Setup

On this machine the working setup is:

```bash
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1
VOICEMODE_TTS_MODELS=tts-1,tts-1-hd,gpt-4o-mini-tts
VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3
VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3
VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy
VOICEMODE_DEFAULT_LOCAL_VOICE=F1
VOICEMODE_LOCAL_STT_PORT=5092
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

Configured local voices are `F1`-`F5` and `M1`-`M5`.

### Parakeet TDT STT

Parakeet provides OpenAI-compatible local speech-to-text on port `5092`.

```bash
curl http://127.0.0.1:5092/health
```

The active model sent by VoiceMode is `parakeet-tdt-0.6b-v3`.

## Install

Install this fork with the local adapter entry points:

```bash
uv tool install "git+https://github.com/groxaxo/voicemode.git[adapters,canary]" --force
```

Or let the installer set up VoiceMode and one or more agent integrations for you:

```bash
uvx voice-mode-install --integrations codex,opencode,qwen,gemini
```

Run `uvx voice-mode-install` interactively to detect installed CLIs and choose from preselected targets. Use `--no-integrations` when you only want to install VoiceMode.

Register with Codex:

```bash
codex mcp add voicemode \
  --env VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1 \
  --env VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1 \
  --env VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_VOICES=F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy \
  --env VOICEMODE_TTS_MODELS=tts-1,tts-1-hd,gpt-4o-mini-tts \
  --env VOICEMODE_DEFAULT_LOCAL_VOICE=F1 \
  --env VOICEMODE_LOCAL_TTS_PORT=8880 \
  --env VOICEMODE_LOCAL_TTS_DIR=/home/op/supertonic-express \
  --env VOICEMODE_LOCAL_STT_PORT=5092 \
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
```

## Fork Additions

This fork adds and configures:

- OpenAI-compatible Inworld TTS adapter entry point: `voicemode-inworld-adapter`
- OpenAI-compatible Canary adapter entry point: `voicemode-canary-adapter`
- Supertonic Express local TTS configuration and docs
- Parakeet TDT local STT defaults, status reporting, prompts, and docs
- Codex/OpenCode/Qwen/Gemini-oriented MCP configuration examples

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
