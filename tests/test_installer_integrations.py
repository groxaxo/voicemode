"""Tests for VoiceMode agent integration installers."""

import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner


INSTALLER_ROOT = Path(__file__).resolve().parent.parent / "installer"
if str(INSTALLER_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALLER_ROOT))


def load_integrations_module():
    """Import the integrations module after home-directory isolation is active."""
    module_name = "voicemode_install.integrations"
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)


def load_cli_module():
    """Import the installer CLI module."""
    module_name = "voicemode_install.cli"
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)


def test_parse_integrations_supports_all_and_dedupes():
    integrations = load_integrations_module()

    assert integrations.parse_integrations("codex,qwen,codex") == ["codex", "qwen"]
    assert integrations.parse_integrations("all") == ["codex", "opencode", "qwen", "gemini"]


def test_parse_integrations_rejects_unknown_target():
    integrations = load_integrations_module()

    with pytest.raises(ValueError):
        integrations.parse_integrations("codex,unknown")


def test_detect_installed_integrations_reports_command_presence():
    integrations = load_integrations_module()

    with patch("voicemode_install.integrations.shutil.which") as mock_which:
        mock_which.side_effect = lambda name: f"/usr/bin/{name}" if name in {"codex", "qwen"} else None
        detected = integrations.detect_installed_integrations()

    status = {item.target: item.detected for item in detected}
    assert status == {
        "codex": True,
        "opencode": False,
        "qwen": True,
        "gemini": False,
    }


def test_codex_integration_is_idempotent():
    integrations = load_integrations_module()

    first = integrations.install_codex_integration()
    assert first.changed is True
    assert first.path.exists()

    content = first.path.read_text()
    assert "[mcp_servers.voicemode]" in content
    assert '[mcp_servers.voicemode.env]' in content
    assert 'command = "voicemode"' in content
    assert 'VOICEMODE_TTS_BASE_URLS = "http://127.0.0.1:8880/v1"' in content
    assert 'VOICEMODE_STT_BASE_URLS = "http://127.0.0.1:5092/v1"' in content
    assert 'VOICEMODE_STT_MODELS = "parakeet-tdt-0.6b-v3"' in content
    assert 'VOICEMODE_LOCAL_STT_PORT = "5092"' in content
    assert "https://api.openai.com/v1" not in content

    second = integrations.install_codex_integration()
    assert second.changed is False
    assert second.path.read_text() == content


def test_opencode_integration_merges_existing_jsonc():
    integrations = load_integrations_module()

    config_path = Path.home() / ".config" / "opencode" / "opencode.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        """{
  // existing preference
  "$schema": "https://opencode.ai/config.json",
  "theme": "opencode",
  "mcp": {
    "other": {
      "type": "local",
      "command": ["other"]
    },
  },
}
"""
    )

    result = integrations.install_opencode_integration()
    assert result.changed is True

    updated_text = config_path.read_text()
    assert "// existing preference" in updated_text
    data = integrations._load_json_like(config_path)
    assert data["theme"] == "opencode"
    assert data["mcp"]["other"]["command"] == ["other"]
    assert data["mcp"]["voicemode"]["type"] == "local"
    assert data["mcp"]["voicemode"]["command"] == ["voicemode"]
    assert data["mcp"]["voicemode"]["environment"]["VOICEMODE_TTS_BASE_URLS"] == "http://127.0.0.1:8880/v1"
    assert data["mcp"]["voicemode"]["environment"]["VOICEMODE_STT_BASE_URLS"] == "http://127.0.0.1:5092/v1"
    assert data["mcp"]["voicemode"]["environment"]["VOICEMODE_STT_MODELS"] == "parakeet-tdt-0.6b-v3"
    assert data["mcp"]["voicemode"]["environment"]["VOICEMODE_STT_MODEL"] == "parakeet-tdt-0.6b-v3"
    assert data["mcp"]["voicemode"]["environment"]["VOICEMODE_LOCAL_STT_PORT"] == "5092"


def test_gemini_and_qwen_integrations_write_expected_paths():
    integrations = load_integrations_module()

    gemini = integrations.install_gemini_integration()
    qwen = integrations.install_qwen_integration()

    assert gemini.path == Path.home() / ".gemini" / "settings.json"
    assert qwen.path == Path.home() / ".qwen" / "settings.json"
    assert gemini.path.exists()
    assert qwen.path.exists()


def test_choose_integrations_interactively_accepts_detected_defaults():
    cli = load_cli_module()
    integrations = load_integrations_module()

    detections = [
        integrations.DetectedIntegration("codex", "codex", True),
        integrations.DetectedIntegration("opencode", "opencode", False),
        integrations.DetectedIntegration("qwen", "qwen", True),
        integrations.DetectedIntegration("gemini", "gemini", False),
    ]

    with patch("voicemode_install.cli.detect_installed_integrations", return_value=detections), \
         patch("voicemode_install.cli.click.prompt", return_value="codex,qwen"):
        chosen = cli._choose_integrations_interactively()

    assert chosen == ["codex", "qwen"]


def test_choose_integrations_interactively_supports_numeric_selection():
    cli = load_cli_module()
    integrations = load_integrations_module()

    detections = [
        integrations.DetectedIntegration("codex", "codex", True),
        integrations.DetectedIntegration("opencode", "opencode", True),
        integrations.DetectedIntegration("qwen", "qwen", False),
        integrations.DetectedIntegration("gemini", "gemini", False),
    ]

    with patch("voicemode_install.cli.detect_installed_integrations", return_value=detections), \
         patch("voicemode_install.cli.click.prompt", return_value="2,4"):
        chosen = cli._choose_integrations_interactively()

    assert chosen == ["opencode", "gemini"]


def test_resolve_integration_targets_autodetects_in_noninteractive_mode():
    cli = load_cli_module()
    integrations = load_integrations_module()

    detections = [
        integrations.DetectedIntegration("codex", "codex", True),
        integrations.DetectedIntegration("opencode", "opencode", False),
        integrations.DetectedIntegration("qwen", "qwen", True),
        integrations.DetectedIntegration("gemini", "gemini", False),
    ]

    with patch("voicemode_install.cli.detect_installed_integrations", return_value=detections):
        chosen = cli._resolve_integration_targets(
            integrations="",
            no_integrations=False,
            non_interactive=True,
        )

    assert chosen == ["codex", "qwen"]


def test_resolve_integration_targets_can_disable_autodetection():
    cli = load_cli_module()

    chosen = cli._resolve_integration_targets(
        integrations="",
        no_integrations=True,
        non_interactive=True,
    )

    assert chosen == []


def test_existing_install_skip_still_runs_selected_integrations():
    cli = load_cli_module()
    runner = CliRunner()

    with patch("voicemode_install.cli.check_existing_installation", return_value=True), \
         patch("voicemode_install.cli.get_installed_version", return_value="8.6.1"), \
         patch("voicemode_install.cli.get_latest_version", return_value="8.6.1"):
        result = runner.invoke(
            cli.main,
            ["--dry-run", "--integrations", "codex"],
            input="n\n",
        )

    assert result.exit_code == 0
    assert "Skipping VoiceMode reinstall; continuing with selected integrations." in result.output
    assert "Would write Codex MCP config" in result.output
