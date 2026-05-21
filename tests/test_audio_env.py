import os

from voice_mode.audio_env import ensure_audio_session_env


def test_audio_session_env_populates_missing_linux_runtime_values(tmp_path, monkeypatch):
    runtime_dir = tmp_path / "runtime"
    (runtime_dir / "pulse").mkdir(parents=True)
    (runtime_dir / "pulse" / "native").touch()
    (runtime_dir / "pipewire-0").touch()
    (runtime_dir / "bus").touch()

    for name in (
        "XDG_RUNTIME_DIR",
        "PULSE_SERVER",
        "PIPEWIRE_REMOTE",
        "DBUS_SESSION_BUS_ADDRESS",
    ):
        monkeypatch.delenv(name, raising=False)

    updates = ensure_audio_session_env(runtime_dir=runtime_dir)

    assert updates == {
        "XDG_RUNTIME_DIR": str(runtime_dir),
        "PULSE_SERVER": f"unix:{runtime_dir / 'pulse' / 'native'}",
        "PIPEWIRE_REMOTE": "pipewire-0",
        "DBUS_SESSION_BUS_ADDRESS": f"unix:path={runtime_dir / 'bus'}",
    }


def test_audio_session_env_preserves_existing_values(tmp_path, monkeypatch):
    runtime_dir = tmp_path / "runtime"
    (runtime_dir / "pulse").mkdir(parents=True)
    (runtime_dir / "pulse" / "native").touch()
    (runtime_dir / "pipewire-0").touch()
    (runtime_dir / "bus").touch()

    monkeypatch.setenv("XDG_RUNTIME_DIR", "/custom/runtime")
    monkeypatch.setenv("PULSE_SERVER", "unix:/custom/pulse")
    monkeypatch.setenv("PIPEWIRE_REMOTE", "custom-pipewire")
    monkeypatch.setenv("DBUS_SESSION_BUS_ADDRESS", "unix:path=/custom/bus")

    updates = ensure_audio_session_env(runtime_dir=runtime_dir)

    assert updates == {}
    assert os.environ["XDG_RUNTIME_DIR"] == "/custom/runtime"
    assert os.environ["PULSE_SERVER"] == "unix:/custom/pulse"
    assert os.environ["PIPEWIRE_REMOTE"] == "custom-pipewire"
    assert os.environ["DBUS_SESSION_BUS_ADDRESS"] == "unix:path=/custom/bus"
