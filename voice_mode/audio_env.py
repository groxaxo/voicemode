"""Audio session environment helpers.

MCP servers are often launched with a narrow environment that omits desktop
session variables. On Linux, PortAudio/sounddevice needs those variables to
reach PulseAudio or PipeWire, even when the user's shell audio works.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def _first_existing_runtime_dir(explicit_runtime_dir: Optional[Path] = None) -> Optional[Path]:
    candidates = []
    if explicit_runtime_dir is not None:
        candidates.append(explicit_runtime_dir)

    existing_env = os.environ.get("XDG_RUNTIME_DIR")
    if existing_env:
        candidates.append(Path(existing_env))

    if hasattr(os, "getuid"):
        candidates.append(Path(f"/run/user/{os.getuid()}"))

    for candidate in candidates:
        try:
            if candidate.is_dir():
                return candidate
        except OSError:
            continue

    return None


def _path_exists(path: Path) -> bool:
    try:
        return path.exists()
    except OSError:
        return False


def ensure_audio_session_env(runtime_dir: Optional[Path] = None) -> dict[str, str]:
    """Populate missing Linux desktop audio variables for MCP child processes.

    Existing variables always win. The returned mapping contains only values
    set by this call, which keeps the helper easy to assert in tests.
    """
    if os.name != "posix":
        return {}

    resolved_runtime_dir = _first_existing_runtime_dir(runtime_dir)
    if resolved_runtime_dir is None:
        return {}

    updates: dict[str, str] = {}

    if not os.environ.get("XDG_RUNTIME_DIR"):
        updates["XDG_RUNTIME_DIR"] = str(resolved_runtime_dir)

    pulse_socket = resolved_runtime_dir / "pulse" / "native"
    if not os.environ.get("PULSE_SERVER") and _path_exists(pulse_socket):
        updates["PULSE_SERVER"] = f"unix:{pulse_socket}"

    pipewire_socket = resolved_runtime_dir / "pipewire-0"
    if not os.environ.get("PIPEWIRE_REMOTE") and _path_exists(pipewire_socket):
        updates["PIPEWIRE_REMOTE"] = "pipewire-0"

    bus_socket = resolved_runtime_dir / "bus"
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS") and _path_exists(bus_socket):
        updates["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path={bus_socket}"

    os.environ.update(updates)
    return updates
