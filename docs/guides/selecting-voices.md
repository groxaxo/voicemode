# Selecting Voices

Voice Mode supports multiple TTS providers with different voices. This guide helps you choose and configure voices for the best experience.

## Available Voices


### Supertonic Express Voices (Local TTS)
- **F1** - Female voice 1
- **F2** - Female voice 2
- **F3** - Female voice 3
- **F4** - Female voice 4
- **F5** - Female voice 5
- **M1** - Male voice 1
- **M2** - Male voice 2
- **M3** - Male voice 3
- **M4** - Male voice 4
- **M5** - Male voice 5

### OpenAI Voices
- **alloy** - Balanced, neutral voice (default)
- **nova** - Warm, expressive female voice
- **shimmer** - Bright, energetic female voice
- **fable** - Calm, storytelling voice
- **echo** - Clear, professional voice
- **onyx** - Deep, authoritative male voice

## Voice Selection Strategy

Voice Mode uses a **voice-first selection algorithm**:

1. **Try each preferred voice** in order from `VOICEMODE_VOICES`
2. **Find first healthy endpoint** that supports that voice
3. **Use that voice and endpoint** for TTS

This ensures you get your preferred voice when possible, regardless of which provider supports it.

## Configuring Voice Preferences

### Quick Setup
Add to your `.voicemode.env`:
```bash
# Try Supertonic first, fallback to OpenAI
VOICEMODE_VOICES=F1,F2,M1,nova,alloy
```

### Voice-First Examples

**Prefer expressive female voices:**
```bash
VOICEMODE_VOICES=F1,shimmer,nova
```

**Prefer male voices:**
```bash
VOICEMODE_VOICES=M1,M2,onyx,echo
```

**Local-first setup:**
```bash
VOICEMODE_VOICES=F1,M1,nova
```

**Cloud-first setup:**
```bash
VOICEMODE_VOICES=nova,shimmer,F1
```

## Provider Considerations

### OpenAI (Cloud)
- **Pros**: Reliable, consistent quality, no setup
- **Cons**: Requires API key, costs money, internet dependent
- **Best for**: Quick setup, reliable fallback

### Supertonic Express (Local)
- **Pros**: Free, private, works offline
- **Cons**: Requires setup, resource intensive
- **Best for**: Privacy, cost control, offline use

## Configuration Hierarchy

Voice preferences follow this priority order:

1. **Environment variables** (`VOICEMODE_VOICES=voice1,voice2`)
2. **Project `.voicemode.env`** files (searched up directory tree)
3. **Global `~/.voicemode/voicemode.env`**
4. **Built-in defaults** (`F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy`)

## Testing Voice Selection

You can test specific voices:

```bash
VOICEMODE_VOICES=F1 voicemode converse
```

## Troubleshooting

**Voice not working?**
1. Verify the provider is healthy
2. Try a different voice as fallback

**Provider switching unexpectedly?**
- Voice-first selection will switch providers to get your preferred voice
- This is intentional behavior for the best voice experience
- Add multiple voices from the same provider if you want to stick to one provider

## Best Practices

1. **Always include fallbacks** - List multiple voices in case one isn't available
2. **Mix providers** - Include both local and cloud voices for flexibility  
3. **Test your setup** - Use `voice_registry()` to verify availability
4. **Project-specific voices** - Use different voices for different types of projects
5. **Consider context** - Professional voices for work, expressive for creative projects
