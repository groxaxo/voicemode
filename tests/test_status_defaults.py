"""Tests for default status output labels."""

from voice_mode.cli_commands import status as status_mod


def test_status_data_uses_supertonic_provider_key(monkeypatch):
    monkeypatch.setattr(
        status_mod,
        "check_whisper_service",
        lambda: status_mod.ServiceInfo(
            name="Whisper",
            type="stt",
            status=status_mod.ServiceStatus.NOT_INSTALLED,
            port=2022,
        ),
    )
    monkeypatch.setattr(
        status_mod,
        "check_openai_compatible_stt_service",
        lambda: status_mod.ServiceInfo(
            name="Parakeet",
            type="stt",
            status=status_mod.ServiceStatus.RUNNING,
            port=5092,
            details={
                "service": "parakeet-tdt",
                "model": "parakeet-tdt-0.6b-v3",
                "default_model": "parakeet-tdt-0.6b-v3",
            },
            health="healthy",
        ),
    )
    monkeypatch.setattr(
        status_mod,
        "check_kokoro_service",
        lambda: status_mod.ServiceInfo(
            name="supertonic-express",
            type="tts",
            status=status_mod.ServiceStatus.RUNNING,
            port=8880,
            details={
                "service": "supertonic-express",
                "voice": "F1",
            },
            health="healthy",
        ),
    )
    monkeypatch.setattr(
        status_mod,
        "check_openai_api",
        lambda: {
            "status": "not_configured",
            "api_key_set": False,
            "tts_model": "tts-1-hd",
            "stt_model": "whisper-1",
        },
    )
    monkeypatch.setattr(
        status_mod,
        "check_ffmpeg",
        lambda: status_mod.DependencyInfo(name="ffmpeg", installed=True),
    )
    monkeypatch.setattr(
        status_mod,
        "check_portaudio",
        lambda: status_mod.DependencyInfo(name="portaudio", installed=True),
    )
    monkeypatch.setattr(
        status_mod,
        "check_uv",
        lambda: status_mod.DependencyInfo(name="uv", installed=True),
    )

    data = status_mod.collect_status_data()

    assert data["runtime"]["command"] == "voicemode"
    assert data["tts"]["active"] == "supertonic-express"
    assert "supertonic" in data["tts"]["providers"]
    assert "kokoro" not in data["tts"]["providers"]
    assert data["tts"]["providers"]["supertonic"]["voice"] == "F1"
    assert data["stt"]["active"] == "parakeet-tdt"
