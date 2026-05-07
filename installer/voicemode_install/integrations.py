"""Integration installers for agent CLIs that support VoiceMode via MCP."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_INTEGRATIONS = ("codex", "opencode", "qwen", "gemini")

VOICEMODE_ENV = {
    "VOICEMODE_TTS_BASE_URLS": "http://127.0.0.1:8880/v1",
    "VOICEMODE_STT_BASE_URLS": "http://127.0.0.1:5092/v1",
    "VOICEMODE_TTS_MODELS": "tts-1,tts-1-hd",
    "VOICEMODE_TTS_AUDIO_FORMAT": "mp3",
    "VOICEMODE_STT_MODELS": "parakeet-tdt-0.6b-v3",
    "VOICEMODE_STT_MODEL": "parakeet-tdt-0.6b-v3",
    "VOICEMODE_VOICES": "F1,F2,F3,F4,F5,M1,M2,M3,M4,M5,alloy",
    "VOICEMODE_DEFAULT_LOCAL_VOICE": "F1",
    "VOICEMODE_LOCAL_TTS_PORT": "8880",
    "VOICEMODE_LOCAL_TTS_DIR": str(Path.home() / "supertonic-express"),
    "VOICEMODE_LOCAL_STT_PORT": "5092",
    "VOICEMODE_PREFER_LOCAL": "true",
    "VOICEMODE_ALWAYS_TRY_LOCAL": "true",
}

CODEX_BLOCK_START = "# BEGIN VOICEMODE MCP"
CODEX_BLOCK_END = "# END VOICEMODE MCP"


@dataclass
class IntegrationResult:
    """Outcome of configuring one integration target."""

    target: str
    path: Path
    changed: bool
    message: str


@dataclass(frozen=True)
class DetectedIntegration:
    """Represents one supported CLI and whether it is available."""

    target: str
    command: str
    detected: bool


def parse_integrations(raw_value: str | None) -> list[str]:
    """Parse a comma-separated integration list."""
    if not raw_value:
        return []

    values = [item.strip().lower() for item in raw_value.split(",") if item.strip()]
    if not values:
        return []
    if "all" in values:
        return list(SUPPORTED_INTEGRATIONS)

    invalid = sorted(set(values) - set(SUPPORTED_INTEGRATIONS))
    if invalid:
        allowed = ", ".join((*SUPPORTED_INTEGRATIONS, "all"))
        raise ValueError(f"Unknown integration target(s): {', '.join(invalid)}. Allowed: {allowed}")

    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            deduped.append(value)
            seen.add(value)
    return deduped


def detect_installed_integrations() -> list[DetectedIntegration]:
    """Detect which supported agent CLIs are available on this machine."""
    detection_order = {
        "codex": "codex",
        "opencode": "opencode",
        "qwen": "qwen",
        "gemini": "gemini",
    }
    results: list[DetectedIntegration] = []
    for target in SUPPORTED_INTEGRATIONS:
        command = detection_order[target]
        results.append(
            DetectedIntegration(
                target=target,
                command=command,
                detected=shutil.which(command) is not None,
            )
        )
    return results


def install_integrations(targets: list[str], dry_run: bool = False) -> list[IntegrationResult]:
    """Install or update one or more VoiceMode integrations."""
    results: list[IntegrationResult] = []
    for target in targets:
        if target == "codex":
            results.append(install_codex_integration(dry_run=dry_run))
        elif target == "opencode":
            results.append(install_opencode_integration(dry_run=dry_run))
        elif target == "qwen":
            results.append(install_qwen_integration(dry_run=dry_run))
        elif target == "gemini":
            results.append(install_gemini_integration(dry_run=dry_run))
    return results


def install_codex_integration(dry_run: bool = False) -> IntegrationResult:
    """Add or update the Codex MCP configuration."""
    path = Path.home() / ".codex" / "config.toml"
    managed_block = _build_codex_block()
    existing_text = path.read_text() if path.exists() else ""
    cleaned_text = _remove_unmanaged_codex_voicemode_tables(existing_text)
    updated_text = _upsert_managed_block(cleaned_text, CODEX_BLOCK_START, CODEX_BLOCK_END, managed_block)
    changed = updated_text != existing_text

    if changed and not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(updated_text)

    message = "Would write Codex MCP config" if dry_run else "Codex MCP config updated"
    if not changed:
        message = "Codex MCP config already up to date"
    return IntegrationResult("codex", path, changed, message)


def install_opencode_integration(dry_run: bool = False) -> IntegrationResult:
    """Add or update the OpenCode MCP configuration."""
    path = Path.home() / ".config" / "opencode" / "opencode.json"
    server_payload = {
        "type": "local",
        "enabled": True,
        "command": ["voicemode"],
        "environment": dict(VOICEMODE_ENV),
    }
    new_file_payload = {
        "$schema": "https://opencode.ai/config.json",
        "mcp": {
            "voicemode": server_payload,
        },
    }
    return _upsert_jsonc_child_config(
        target="opencode",
        path=path,
        parent_key="mcp",
        child_key="voicemode",
        child_payload=server_payload,
        new_file_payload=new_file_payload,
        dry_run=dry_run,
    )


def install_qwen_integration(dry_run: bool = False) -> IntegrationResult:
    """Add or update the Qwen Code MCP configuration."""
    path = Path.home() / ".qwen" / "settings.json"
    server_payload = {
        "command": "voicemode",
        "args": [],
        "env": dict(VOICEMODE_ENV),
    }
    new_file_payload = {
        "mcpServers": {
            "voicemode": server_payload,
        }
    }
    return _upsert_jsonc_child_config(
        target="qwen",
        path=path,
        parent_key="mcpServers",
        child_key="voicemode",
        child_payload=server_payload,
        new_file_payload=new_file_payload,
        dry_run=dry_run,
    )


def install_gemini_integration(dry_run: bool = False) -> IntegrationResult:
    """Add or update the Gemini CLI MCP configuration."""
    path = Path.home() / ".gemini" / "settings.json"
    server_payload = {
        "command": "voicemode",
        "args": [],
        "env": dict(VOICEMODE_ENV),
    }
    new_file_payload = {
        "mcpServers": {
            "voicemode": server_payload,
        }
    }
    return _upsert_jsonc_child_config(
        target="gemini",
        path=path,
        parent_key="mcpServers",
        child_key="voicemode",
        child_payload=server_payload,
        new_file_payload=new_file_payload,
        dry_run=dry_run,
    )


def _upsert_jsonc_child_config(
    target: str,
    path: Path,
    parent_key: str,
    child_key: str,
    child_payload: dict[str, Any],
    new_file_payload: dict[str, Any],
    dry_run: bool = False,
) -> IntegrationResult:
    """Upsert a nested config object while preserving surrounding JSONC text."""
    raw = path.read_text() if path.exists() else ""
    if raw.strip():
        updated_text = _upsert_jsonc_child(raw, parent_key, child_key, child_payload)
    else:
        updated_text = json.dumps(new_file_payload, indent=2) + "\n"

    changed = updated_text != raw
    if changed and not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(updated_text)

    message = f"Would update {target} config" if dry_run else f"{target.capitalize()} config updated"
    if not changed:
        message = f"{target.capitalize()} config already up to date"
    return IntegrationResult(target, path, changed, message)


def _build_codex_block() -> str:
    lines = [
        CODEX_BLOCK_START,
        "[mcp_servers.voicemode]",
        'command = "voicemode"',
        "args = []",
        "enabled = true",
        "",
        "[mcp_servers.voicemode.env]",
    ]
    for key, value in VOICEMODE_ENV.items():
        lines.append(f'{key} = {json.dumps(value)}')
    lines.append(CODEX_BLOCK_END)
    return "\n".join(lines)


def _upsert_managed_block(text: str, start_marker: str, end_marker: str, block: str) -> str:
    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}\n?",
        re.DOTALL,
    )
    replacement = block.strip() + "\n"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    if text and not text.endswith("\n"):
        text += "\n"
    if text:
        text += "\n"
    return text + replacement


def _remove_unmanaged_codex_voicemode_tables(text: str) -> str:
    """Remove older unmarked Codex VoiceMode tables before writing the managed block."""
    voicemode_tables = {
        "mcp_servers.voicemode",
        "mcp_servers.voicemode.env",
    }
    lines = text.splitlines(keepends=True)
    kept: list[str] = []
    in_managed_block = False
    skipping_table = False

    for line in lines:
        stripped = line.strip()

        if stripped == CODEX_BLOCK_START:
            in_managed_block = True
            skipping_table = False
            kept.append(line)
            continue
        if stripped == CODEX_BLOCK_END:
            in_managed_block = False
            kept.append(line)
            continue

        table_match = re.match(r"^\s*\[([A-Za-z0-9_.-]+)\]\s*(?:#.*)?$", line)
        if table_match and not in_managed_block:
            skipping_table = table_match.group(1) in voicemode_tables
            if skipping_table:
                continue

        if skipping_table and not in_managed_block:
            continue

        kept.append(line)

    return "".join(kept)


def _load_json_like(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    raw = path.read_text().strip()
    if not raw:
        return {}

    sanitized = _strip_json_comments(raw)
    sanitized = _strip_trailing_commas(sanitized)
    data = json.loads(sanitized)
    if not isinstance(data, dict):
        raise ValueError(f"Expected top-level object in {path}")
    return data


def _upsert_jsonc_child(text: str, parent_key: str, child_key: str, child_payload: dict[str, Any]) -> str:
    """Add or replace parent.child in a JSON/JSONC object without rewriting unrelated text."""
    root_open = _skip_ws_and_comments(text, 0)
    if root_open >= len(text) or text[root_open] != "{":
        raise ValueError("Expected top-level JSON object")

    root_close = _find_matching_delimiter(text, root_open)
    parent = _find_direct_property(text, root_open, root_close, parent_key)
    if parent is None:
        parent_payload = {child_key: child_payload}
        parent_block = _format_property(parent_key, parent_payload, "  ")
        return _insert_property_into_object(text, root_open, root_close, parent_block, "")

    _, parent_value_start, parent_value_end = parent
    parent_object_open = _skip_ws_and_comments(text, parent_value_start)
    if parent_object_open >= parent_value_end or text[parent_object_open] != "{":
        raise ValueError(f"Expected '{parent_key}' to be a JSON object")

    parent_object_close = _find_matching_delimiter(text, parent_object_open)
    parent_indent = _line_indent_at(text, parent[0])
    child_indent = _infer_child_indent(text, parent_object_open, parent_object_close, parent_indent)
    child_block = _format_property(child_key, child_payload, child_indent)
    child = _find_direct_property(text, parent_object_open, parent_object_close, child_key)
    if child is not None:
        child_key_start, _, child_value_end = child
        return text[:child_key_start] + child_block + text[child_value_end:]

    return _insert_property_into_object(text, parent_object_open, parent_object_close, child_block, parent_indent)


def _strip_json_comments(text: str) -> str:
    """Remove // and /* */ comments while preserving string contents."""
    result: list[str] = []
    i = 0
    in_string = False
    escape = False

    while i < len(text):
        char = text[i]
        next_char = text[i + 1] if i + 1 < len(text) else ""

        if in_string:
            result.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            i += 1
            continue

        if char == '"':
            in_string = True
            result.append(char)
            i += 1
            continue

        if char == "/" and next_char == "/":
            i += 2
            while i < len(text) and text[i] != "\n":
                i += 1
            continue

        if char == "/" and next_char == "*":
            i += 2
            while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue

        result.append(char)
        i += 1

    return "".join(result)


def _skip_ws_and_comments(text: str, index: int) -> int:
    i = index
    while i < len(text):
        if text[i] in " \t\r\n":
            i += 1
            continue
        if text.startswith("//", i):
            i += 2
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        if text.startswith("/*", i):
            i += 2
            while i + 1 < len(text) and not text.startswith("*/", i):
                i += 1
            i = min(i + 2, len(text))
            continue
        break
    return i


def _find_matching_delimiter(text: str, open_index: int) -> int:
    pairs = {"{": "}", "[": "]"}
    open_char = text[open_index]
    close_char = pairs.get(open_char)
    if close_char is None:
        raise ValueError(f"Expected JSON object or array at index {open_index}")

    depth = 0
    i = open_index
    while i < len(text):
        if text.startswith("//", i):
            i += 2
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        if text.startswith("/*", i):
            i += 2
            while i + 1 < len(text) and not text.startswith("*/", i):
                i += 1
            i += 2
            continue
        if text[i] == '"':
            _, i = _parse_json_string(text, i)
            continue
        if text[i] == open_char:
            depth += 1
        elif text[i] == close_char:
            depth -= 1
            if depth == 0:
                return i
        i += 1

    raise ValueError("Unclosed JSON object or array")


def _find_direct_property(text: str, object_open: int, object_close: int, key: str) -> tuple[int, int, int] | None:
    i = object_open + 1
    while i < object_close:
        i = _skip_ws_and_comments(text, i)
        if i >= object_close:
            break
        if text[i] in ",":
            i += 1
            continue
        if text[i] != '"':
            i += 1
            continue

        key_start = i
        parsed_key, key_end = _parse_json_string(text, i)
        colon = _skip_ws_and_comments(text, key_end)
        if colon >= object_close or text[colon] != ":":
            i = key_end
            continue

        value_start = _skip_ws_and_comments(text, colon + 1)
        value_end = _find_json_value_end(text, value_start)
        if parsed_key == key:
            return key_start, value_start, value_end
        i = value_end

    return None


def _find_json_value_end(text: str, value_start: int) -> int:
    if value_start >= len(text):
        raise ValueError("Missing JSON value")

    char = text[value_start]
    if char in "{[":
        return _find_matching_delimiter(text, value_start) + 1
    if char == '"':
        _, end = _parse_json_string(text, value_start)
        return end

    i = value_start
    while i < len(text) and text[i] not in ",}]":
        i += 1
    return i


def _parse_json_string(text: str, start: int) -> tuple[str, int]:
    i = start + 1
    escape = False
    while i < len(text):
        char = text[i]
        if escape:
            escape = False
        elif char == "\\":
            escape = True
        elif char == '"':
            return json.loads(text[start : i + 1]), i + 1
        i += 1
    raise ValueError("Unclosed JSON string")


def _format_property(key: str, value: Any, indent: str) -> str:
    block = json.dumps({key: value}, indent=2)
    lines = block.splitlines()[1:-1]
    return "\n".join(indent + line[2:] if line.startswith("  ") else indent + line for line in lines)


def _line_indent_at(text: str, index: int) -> str:
    line_start = text.rfind("\n", 0, index) + 1
    segment = text[line_start:index]
    return segment[: len(segment) - len(segment.lstrip(" \t"))]


def _infer_child_indent(text: str, object_open: int, object_close: int, parent_indent: str) -> str:
    first_property = _find_first_direct_property(text, object_open, object_close)
    if first_property is not None:
        return _line_indent_at(text, first_property)
    return parent_indent + "  "


def _find_first_direct_property(text: str, object_open: int, object_close: int) -> int | None:
    i = object_open + 1
    while i < object_close:
        i = _skip_ws_and_comments(text, i)
        if i >= object_close:
            break
        if text[i] == '"':
            return i
        i += 1
    return None


def _insert_property_into_object(text: str, object_open: int, object_close: int, property_block: str, close_indent: str) -> str:
    prefix = ""
    if _object_has_direct_property(text, object_open, object_close):
        prefix = "" if _last_non_ws_char(text, object_open + 1, object_close) == "," else ","
    insertion = f"{prefix}\n{property_block}\n{close_indent}"
    return text[:object_close] + insertion + text[object_close:]


def _object_has_direct_property(text: str, object_open: int, object_close: int) -> bool:
    return _find_first_direct_property(text, object_open, object_close) is not None


def _last_non_ws_char(text: str, start: int, end: int) -> str | None:
    i = end - 1
    while i >= start:
        if not text[i].isspace():
            return text[i]
        i -= 1
    return None


def _strip_trailing_commas(text: str) -> str:
    """Remove trailing commas before object/array closers."""
    result: list[str] = []
    in_string = False
    escape = False
    i = 0

    while i < len(text):
        char = text[i]

        if in_string:
            result.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            i += 1
            continue

        if char == '"':
            in_string = True
            result.append(char)
            i += 1
            continue

        if char == ",":
            j = i + 1
            while j < len(text) and text[j] in " \t\r\n":
                j += 1
            if j < len(text) and text[j] in "}]":
                i += 1
                continue

        result.append(char)
        i += 1

    return "".join(result)


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
