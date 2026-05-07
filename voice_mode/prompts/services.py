"""Service management prompts for voice endpoints."""

from voice_mode.server import mcp


@mcp.prompt(name="whisper")
def whisper_prompt(action: str = "status") -> str:
    """Manage Whisper speech-to-text service.
    
    Args:
        action: Service action (status, start, stop, restart, enable, disable, logs) or install request
    """
    valid_actions = ["status", "start", "stop", "restart", "enable", "disable", "logs"]
    
    # Check if user wants to install
    install_keywords = ["install", "setup", "configure", "download", "get"]
    if action.lower() in install_keywords or any(keyword in action.lower() for keyword in install_keywords):
        return "The user wants to install Whisper. Use the whisper_install tool to install the Whisper STT service."
    
    if action not in valid_actions:
        return f"Invalid action '{action}'. Use one of: {', '.join(valid_actions)}"
    
    return f"Use the service tool with service_name='whisper' and action='{action}'"


@mcp.prompt(name="kokoro")
def kokoro_prompt(action: str = "status") -> str:
    """Manage Kokoro text-to-speech service.
    
    Args:
        action: Service action (status, start, stop, restart, enable, disable, logs) or install request
    """
    valid_actions = ["status", "start", "stop", "restart", "enable", "disable", "logs"]
    
    # Check if user wants to install
    install_keywords = ["install", "setup", "configure", "download", "get"]
    if action.lower() in install_keywords or any(keyword in action.lower() for keyword in install_keywords):
        return "The user wants to install Kokoro. Use the kokoro_install tool to install the Kokoro TTS service."
    
    if action not in valid_actions:
        return f"Invalid action '{action}'. Use one of: {', '.join(valid_actions)}"
    
    return f"Use the service tool with service_name='kokoro' and action='{action}'"


@mcp.prompt(name="supertonic")
def supertonic_prompt(action: str = "status") -> str:
    """Check Supertonic Express text-to-speech endpoint."""
    if action != "status":
        return "Supertonic Express is an external OpenAI-compatible TTS server. Check its health with curl http://127.0.0.1:8880/health or manage it from /home/op/supertonic-express."
    return "Check Supertonic Express with curl http://127.0.0.1:8880/health and use VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1,https://api.openai.com/v1."


@mcp.prompt(name="parakeet")
def parakeet_prompt(action: str = "status") -> str:
    """Check Parakeet OpenAI-compatible speech-to-text endpoint."""
    if action != "status":
        return "Parakeet is managed locally from /home/op/parakeet-tdt-0.6b-v3-fastapi-openai. Start it with systemctl --user start parakeet-tdt or conda run -n parakeet-onnx python app.py."
    return "Check Parakeet with curl http://127.0.0.1:5092/health and use VOICEMODE_STT_BASE_URLS=http://127.0.0.1:5092/v1,https://api.openai.com/v1 plus VOICEMODE_STT_MODELS=parakeet-tdt-0.6b-v3,whisper-1."
