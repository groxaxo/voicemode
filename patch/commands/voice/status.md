---
description: Check VoiceMode service status
agent: build
---

# VoiceMode Service Status

Check the status of VoiceMode voice services including Whisper (STT), Kokoro (TTS), and other components.

## Usage

```
/voice/status
```

## Implementation

```bash
voicemode service status
```

## What It Shows

The status command displays:

### Service Status
- **Running State**: Whether each service is active
- **PID**: Process ID if running
- **Port**: Network port the service is listening on
- **Uptime**: How long the service has been running

### Available Services

| Service | Port | Purpose |
|---------|------|---------|
| whisper | 2022 | Local speech-to-text (Whisper.cpp) |
| kokoro | 8880 | Local text-to-speech (Kokoro) |
| livekit | 7880 | Real-time audio rooms (optional) |

### Health Checks

Each service undergoes health checks:
- ✅ **Healthy**: Service running and responding
- ⚠️ **Degraded**: Service running but slow/errors
- ❌ **Down**: Service not running or unreachable

## Example Output

```
VoiceMode Services Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Whisper (STT)
  Status: ✅ Running
  Port:   2022
  PID:    12345
  Uptime: 2h 15m
  Health: Healthy

Kokoro (TTS)
  Status: ✅ Running
  Port:   8880
  PID:    12346
  Uptime: 2h 15m
  Health: Healthy

LiveKit
  Status: ⚠️  Not installed
  Info:   Optional service
```

## Detailed Service Status

Check a specific service:

```bash
# Whisper status
voicemode service status whisper

# Kokoro status
voicemode service status kokoro

# View service logs
voicemode service logs whisper
voicemode service logs kokoro
```

## Starting/Stopping Services

If services aren't running:

```bash
# Start all services
voicemode service start whisper
voicemode service start kokoro

# Stop services
voicemode service stop whisper
voicemode service stop kokoro

# Restart services
voicemode service restart whisper
```

## Service Management

### Enable Auto-Start

Configure services to start on system boot:

```bash
# macOS (launchd)
voicemode service enable whisper
voicemode service enable kokoro

# Linux (systemd)
systemctl --user enable voicemode-whisper
systemctl --user enable voicemode-kokoro
```

### Disable Auto-Start

```bash
# macOS
voicemode service disable whisper

# Linux
systemctl --user disable voicemode-whisper
```

## Troubleshooting

### Service Won't Start

1. **Check logs**:
   ```bash
   voicemode service logs whisper --lines 50
   ```

2. **Verify installation**:
   ```bash
   voicemode deps
   ```

3. **Check port conflicts**:
   ```bash
   # macOS/Linux
   lsof -i :2022  # Whisper
   lsof -i :8880  # Kokoro
   ```

4. **Reinstall service**:
   ```bash
   voicemode service uninstall whisper
   voicemode service install whisper
   ```

### Service Crashes

Check the service logs for errors:

```bash
voicemode service logs whisper --lines 100
```

Common issues:
- **Port already in use**: Another service using the port
- **Missing models**: Model files not downloaded
- **Permission errors**: Insufficient file/directory permissions

### Services Missing

If services show as "Not installed":

```bash
# Install missing services
voicemode service install whisper
voicemode service install kokoro
```

## Alternative: Cloud Services

If you don't want to run local services, use OpenAI's API:

```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Configure VoiceMode
voicemode config set OPENAI_API_KEY "sk-..."
voicemode config set VOICEMODE_PREFER_LOCAL false
```

## Diagnostics

For comprehensive system information:

```bash
# System info
voicemode diag info

# Audio devices
voicemode diag devices

# Dependency check
voicemode deps
```

## See Also

- `/voice/install` - Install voice services
- `/voice/converse` - Start voice conversation
- Documentation: https://voice-mode.readthedocs.io/troubleshooting/
