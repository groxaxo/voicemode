# VoiceMode

VoiceMode is an MCP voice interface for Codex, Claude Code, OpenCode, Qwen Code, Gemini CLI, and other MCP-capable agents. This fork is configured for a fast local/LAN voice stack:

- **TTS:** OpenAI-compatible local TTS, either localhost or LAN
- **STT:** Parakeet TDT 0.6B v3, either localhost or LAN
- **Fallback:** none configured for Codex MCP by default
- **MCP tools:** `converse` and `service`

The goal is simple: talk to your coding agent with local speech generation and local transcription by default.

## Current Local Setup

On this LAN the working setup is:

```bash
VOICEMODE_TTS_BASE_URLS=http://100.85.200.51:12437/v1
VOICEMODE_STT_BASE_URLS=http://100.85.200.51:5092/v1
VOICEMODE_TTS_MODELS=neuphonic/neutts-air-q8-gguf
VOICEMODE_TTS_MODEL=neuphonic/neutts-air-q8-gguf
VOICEMODE_TTS_AUDIO_FORMAT=wav
VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3
VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3
VOICEMODE_VOICES=latina-1,mateo,spanish-medium-1,spanish-medium-2,spanish-long-1,spanish-short-1,female-voice,jo,juliette,greta,dave,chatterbox_en_03_medium,alloy
VOICEMODE_DEFAULT_LOCAL_VOICE=latina-1
VOICEMODE_LOCAL_TTS_PORT=12437
VOICEMODE_LOCAL_TTS_DIR=/home/op/neutts
VOICEMODE_LOCAL_STT_PORT=5092
VOICEMODE_PREFER_LOCAL=true
VOICEMODE_ALWAYS_TRY_LOCAL=true
```

Codex is registered to run the installed `voicemode` executable as an MCP server with the same endpoint chain.

## Services

### OpenAI-Compatible LAN TTS

The LAN TTS server provides OpenAI-compatible text-to-speech on port `12437`.

```bash
curl http://100.85.200.51:12437/health
curl http://100.85.200.51:12437/v1/voices
```

Configured Spanish voices include `latina-1`, `mateo`, and `spanish-medium-1`.

### Parakeet TDT STT

Parakeet provides OpenAI-compatible local speech-to-text on port `5092`.

```bash
curl http://100.85.200.51:5092/health
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
  --env VOICEMODE_TTS_BASE_URLS=http://100.85.200.51:12437/v1 \
  --env VOICEMODE_STT_BASE_URLS=http://100.85.200.51:5092/v1 \
  --env VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_STT_MODEL=parakeet-tdt-0.6b-v3 \
  --env VOICEMODE_VOICES=latina-1,mateo,spanish-medium-1,spanish-medium-2,spanish-long-1,spanish-short-1,female-voice,jo,juliette,greta,dave,chatterbox_en_03_medium,alloy \
  --env VOICEMODE_TTS_MODELS=neuphonic/neutts-air-q8-gguf \
  --env VOICEMODE_TTS_MODEL=neuphonic/neutts-air-q8-gguf \
  --env VOICEMODE_TTS_AUDIO_FORMAT=wav \
  --env VOICEMODE_DEFAULT_LOCAL_VOICE=latina-1 \
  --env VOICEMODE_LOCAL_TTS_PORT=12437 \
  --env VOICEMODE_LOCAL_TTS_DIR=/home/op/neutts \
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
