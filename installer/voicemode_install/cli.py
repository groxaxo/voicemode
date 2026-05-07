"""Main CLI for VoiceMode installer."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import click

from . import __version__
from .checker import DependencyChecker
from .hardware import HardwareInfo
from .integrations import detect_installed_integrations, install_integrations, parse_integrations
from .installer import PackageInstaller
from .logger import InstallLogger
from .system import detect_platform, get_system_info, check_command_exists, check_homebrew_installed


LOGO = """
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║   ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗    ║
    ║   ██║   ██║██╔═══██╗██║██╔════╝██╔════╝    ║
    ║   ██║   ██║██║   ██║██║██║     █████╗      ║
    ║   ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝      ║
    ║    ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗    ║
    ║     ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝    ║
    ║                                            ║
    ║   ███╗   ███╗ ██████╗ ██████╗ ███████╗     ║
    ║   ████╗ ████║██╔═══██╗██╔══██╗██╔════╝     ║
    ║   ██╔████╔██║██║   ██║██║  ██║█████╗       ║
    ║   ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝       ║
    ║   ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗     ║
    ║   ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝     ║
    ║                                            ║
    ║            VoiceMode Installer             ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
"""


def print_logo():
    """Display the VoiceMode logo in Claude Code orange."""
    # Use ANSI 256-color code 208 (dark orange) which matches Claude Code orange (RGB 208, 128, 0)
    # This works on xterm-256color and other 256-color terminals
    click.echo('\033[38;5;208m' + '\033[1m' + LOGO + '\033[0m')


def print_step(message: str):
    """Print a step message."""
    click.echo(click.style(f"🔧 {message}", fg='blue'))


def print_success(message: str):
    """Print a success message."""
    click.echo(click.style(f"✅ {message}", fg='green'))


def print_warning(message: str):
    """Print a warning message in Claude Code orange."""
    # Use ANSI 256-color code 208 (dark orange)
    click.echo('\033[38;5;208m' + f"⚠️  {message}" + '\033[0m')


def print_error(message: str):
    """Print an error message."""
    click.echo(click.style(f"❌ {message}", fg='red'))


def get_installed_version() -> str | None:
    """Get the currently installed VoiceMode version."""
    try:
        result = subprocess.run(
            ['voicemode', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Output is like "VoiceMode version 6.0.1" or just "6.0.1"
            version = result.stdout.strip().split()[-1]
            return version
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def get_latest_version() -> str | None:
    """Get the latest VoiceMode version from PyPI."""
    try:
        # Use PyPI JSON API to get latest version
        result = subprocess.run(
            ['curl', '-s', 'https://pypi.org/pypi/voice-mode/json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data['info']['version']
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
        pass
    return None


def check_existing_installation() -> bool:
    """Check if VoiceMode is already installed."""
    return check_command_exists('voicemode')


def ensure_homebrew_on_macos(platform_info, dry_run: bool, non_interactive: bool) -> bool:
    """
    Ensure Homebrew is installed on macOS before checking dependencies.

    Returns True if Homebrew is available or successfully installed, False otherwise.
    """
    # Only needed on macOS
    if platform_info.distribution != 'darwin':
        return True

    # Check if already installed
    if check_homebrew_installed():
        return True

    # Not installed
    print_warning("Homebrew is not installed")
    click.echo("Homebrew is the package manager required to install system dependencies on macOS.")
    click.echo("Visit: https://brew.sh")
    click.echo()

    if dry_run:
        print_step("[DRY RUN] Would install Homebrew (macOS package manager)")
        return True

    if non_interactive:
        # Auto-install Homebrew in non-interactive mode using NONINTERACTIVE=1
        print_step("Installing Homebrew (non-interactive)...")
    else:
        # Prompt user
        if not click.confirm("Install Homebrew now?", default=True):
            print_error("Homebrew installation declined")
            click.echo("Please install Homebrew manually and run the installer again.")
            return False
        print_step("Installing Homebrew...")
        click.echo("This may take a few minutes and will require your password.")

    click.echo()

    try:
        # Use NONINTERACTIVE=1 for unattended installation
        env = os.environ.copy()
        if non_interactive:
            env['NONINTERACTIVE'] = '1'
        install_script = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        result = subprocess.run(install_script, shell=True, check=True, env=env)

        if result.returncode == 0:
            print_success("Homebrew installed successfully")

            # Verify
            if check_homebrew_installed():
                return True
            else:
                print_warning("Homebrew was installed but 'brew' command not found in PATH")
                click.echo("You may need to add Homebrew to your PATH. Check the installation output above.")
                return False
        else:
            print_error("Homebrew installation returned non-zero exit code")
            return False

    except subprocess.CalledProcessError as e:
        print_error(f"Error installing Homebrew: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error installing Homebrew: {e}")
        return False


EPILOG = """
\b
Examples:
  # Normal installation
  voice-mode-install

  # Non-interactive installation (auto-accept all prompts)
  voice-mode-install --yes
  voice-mode-install -y

  # Dry run (see what would be installed)
  voice-mode-install --dry-run

  # Install specific version
  voice-mode-install --voice-mode-version=5.1.3

  # Skip service installation
  voice-mode-install --skip-services

  # Configure Codex and OpenCode after installation
  voice-mode-install --integrations codex,opencode

  # Autodetect installed CLIs and choose interactively
  voice-mode-install

  # Only configure agent integrations
  voice-mode-install --integrations all --integrations-only

  # Skip agent integration autodetection
  voice-mode-install --no-integrations

  # Install with specific Whisper model
  voice-mode-install --yes --model large-v2
"""


@click.command(epilog=EPILOG, context_settings={'help_option_names': ['-h', '--help']})
@click.option('-d', '--dry-run', is_flag=True, help='Show what would be installed without installing')
@click.option('-v', '--voice-mode-version', default=None, help='Specific VoiceMode version to install')
@click.option('-s', '--skip-services', is_flag=True, help='Skip local service installation')
@click.option('--integrations', default='', help='Comma-separated CLIs to configure: codex, opencode, qwen, gemini, all')
@click.option('--integrations-only', is_flag=True, help='Only configure agent integrations, skip VoiceMode installation')
@click.option('--no-integrations', is_flag=True, help='Do not autodetect or configure agent CLI integrations')
@click.option('-y', '--yes', 'non_interactive', is_flag=True, help='Run without prompts (auto-accept all)')
@click.option('-n', '--non-interactive', is_flag=True, help='Run without prompts (deprecated: use --yes/-y)')
@click.option('-m', '--model', default='base', help='Whisper model to use (base, small, medium, large-v2)')
@click.version_option(__version__, '-V', '--version')
def main(dry_run, voice_mode_version, skip_services, integrations, integrations_only, no_integrations, non_interactive, model):
    """VoiceMode Installer - Install VoiceMode and its system dependencies.

    This installer will:

      1. Detect your operating system and architecture

      2. Check for missing system dependencies

      3. Install required packages (with your permission)

      4. Install VoiceMode using uv

      5. Optionally install local voice services

      6. Configure shell completions

      7. Verify the installation
    """
    # Detect non-interactive environment (no TTY)
    if not sys.stdin.isatty() and not non_interactive and not dry_run and not integrations_only:
        click.echo("Error: Running in non-interactive environment without --yes flag", err=True)
        click.echo("Use --yes or -y to enable automatic installation", err=True)
        click.echo("Example: uvx voice-mode-install --yes", err=True)
        sys.exit(1)

    # Initialize logger
    logger = InstallLogger()

    try:
        # Clear screen and show logo
        if not dry_run:
            click.clear()
        print_logo()
        click.echo()

        integration_targets = _resolve_integration_targets(
            integrations=integrations,
            no_integrations=no_integrations,
            non_interactive=non_interactive,
        )

        if dry_run:
            click.echo(click.style("DRY RUN MODE - No changes will be made", fg='yellow', bold=True))
            click.echo()

        if integration_targets:
            click.echo(f"Requested integrations: {', '.join(integration_targets)}")
            click.echo()

        if integrations_only:
            _run_integration_phase(integration_targets, dry_run=dry_run)
            logger.log_complete(success=True, voicemode_installed=check_command_exists('voicemode'))
            return

        # Detect platform
        print_step("Detecting platform...")
        platform_info = detect_platform()
        system_info = get_system_info()

        logger.log_start(system_info)

        click.echo(f"Detected: {platform_info.os_name} ({platform_info.architecture})")
        if platform_info.is_wsl:
            print_warning("WSL detected - additional audio configuration may be needed")
        click.echo()

        # Ensure Homebrew is installed on macOS (before checking dependencies)
        if not ensure_homebrew_on_macos(platform_info, dry_run, non_interactive):
            logger.log_error("Homebrew installation required but not available")
            sys.exit(1)

        # Check for existing installation
        if check_existing_installation():
            installed_version = get_installed_version()
            latest_version = get_latest_version()

            click.echo(click.style("✓ VoiceMode is currently installed", fg='green'))

            if installed_version:
                click.echo(f"  Installed version: {installed_version}")
            else:
                click.echo("  Installed version: (unable to detect)")

            if latest_version:
                click.echo(f"  Latest version:    {latest_version}")

                # Check if update is available
                if installed_version and latest_version and installed_version != latest_version:
                    click.echo()
                    if non_interactive:
                        print_step("Upgrading VoiceMode...")
                    elif not click.confirm(f"Upgrade to version {latest_version}?", default=True):
                        if _finish_with_integrations_or_exit(
                            integration_targets,
                            dry_run,
                            logger,
                            "\nTo upgrade manually later, run: uv tool install --upgrade voice-mode",
                        ):
                            return
                elif installed_version and latest_version and installed_version == latest_version:
                    click.echo()
                    click.echo(click.style("✓ VoiceMode is up-to-date", fg='green'))
                    if non_interactive:
                        click.echo("Reinstalling...")
                    elif not click.confirm("Reinstall anyway?", default=False):
                        if _finish_with_integrations_or_exit(
                            integration_targets,
                            dry_run,
                            logger,
                            "\nInstallation cancelled.",
                        ):
                            return
                else:
                    click.echo()
                    if not non_interactive:
                        if not click.confirm("Reinstall VoiceMode?", default=False):
                            if _finish_with_integrations_or_exit(
                                integration_targets,
                                dry_run,
                                logger,
                                "\nTo upgrade manually, run: uv tool install --upgrade voice-mode",
                            ):
                                return
            else:
                click.echo("  Latest version:    (unable to check)")
                click.echo()
                if not non_interactive:
                    if not click.confirm("Reinstall/upgrade VoiceMode?", default=False):
                        if _finish_with_integrations_or_exit(
                            integration_targets,
                            dry_run,
                            logger,
                            "\nTo upgrade manually, run: uv tool install --upgrade voice-mode",
                        ):
                            return

            click.echo()

        # Check dependencies
        print_step("Checking system dependencies...")
        checker = DependencyChecker(platform_info)
        core_deps = checker.check_core_dependencies()

        missing_deps = checker.get_missing_packages(core_deps)
        summary = checker.get_summary(core_deps)

        logger.log_check('core', summary['installed'], summary['missing_required'])

        # Display summary
        click.echo()
        click.echo("System Dependencies:")
        for pkg in core_deps:
            if pkg.required:
                status = "✓" if pkg.installed else "✗"
                color = "green" if pkg.installed else "red"
                click.echo(f"  {click.style(status, fg=color)} {pkg.name} - {pkg.description}")

        click.echo()

        # Install missing dependencies
        if missing_deps:
            print_warning(f"Missing {len(missing_deps)} required package(s)")

            missing_names = [pkg.name for pkg in missing_deps]
            click.echo(f"\nPackages to install: {', '.join(missing_names)}")

            if not non_interactive and not dry_run:
                if not click.confirm("\nInstall missing dependencies?", default=True):
                    print_error("Cannot proceed without required dependencies")
                    sys.exit(1)

            installer = PackageInstaller(platform_info, dry_run=dry_run, non_interactive=non_interactive)
            if installer.install_packages(missing_deps):
                print_success("System dependencies installed")
                logger.log_install('system', missing_names, True)
            else:
                print_error("Failed to install some dependencies")
                logger.log_install('system', missing_names, False)
                if not dry_run:
                    sys.exit(1)
        else:
            print_success("All required dependencies are already installed")

        click.echo()

        # Install VoiceMode
        print_step("Installing VoiceMode...")
        installer = PackageInstaller(platform_info, dry_run=dry_run, non_interactive=non_interactive)

        if installer.install_voicemode(version=voice_mode_version):
            print_success("VoiceMode installed successfully")
            logger.log_install('voicemode', ['voice-mode'], True)
        else:
            print_error("Failed to install VoiceMode")
            logger.log_install('voicemode', ['voice-mode'], False)
            if not dry_run:
                sys.exit(1)

        click.echo()

        # Health check
        if not dry_run:
            print_step("Verifying installation...")
            voicemode_path = shutil.which('voicemode')
            if voicemode_path:
                print_success(f"VoiceMode command found: {voicemode_path}")

                # Test that it works
                try:
                    result = subprocess.run(
                        ['voicemode', '--version'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        print_success(f"VoiceMode version: {result.stdout.strip()}")
                    else:
                        print_warning("VoiceMode command exists but may not be working correctly")
                except Exception as e:
                    print_warning(f"Could not verify VoiceMode: {e}")
            else:
                print_warning("VoiceMode command not immediately available in PATH")
                click.echo("You may need to restart your shell or run:")
                click.echo("  source ~/.bashrc  # or your shell's rc file")

        # Shell completion setup
        if not dry_run:
            print_step("Setting up shell completion...")
            shell = Path.home() / '.bashrc'  # Simplified for now
            if shell.exists():
                print_success("Shell completion configured")
            else:
                print_warning("Could not configure shell completion automatically")

        # Hardware recommendations for services
        if not skip_services and not dry_run:
            click.echo()
            click.echo("━" * 70)
            click.echo(click.style("Local Voice Services", fg='blue', bold=True))
            click.echo("━" * 70)
            click.echo()

            hardware = HardwareInfo(platform_info)
            click.echo(hardware.get_recommendation_message())
            click.echo()
            click.echo(f"Estimated download size: {hardware.get_download_estimate()}")
            click.echo()

            if hardware.should_recommend_local_services():
                if non_interactive or click.confirm("Install local voice services now?", default=True):
                    model_flag = f" --model {model}" if model != 'base' else ''

                    # Install Whisper
                    click.echo()
                    print_step(f"Installing Whisper STT service (model: {model})...")
                    whisper_cmd = ['voicemode', 'service', 'install', 'whisper']
                    if model != 'base':
                        whisper_cmd.extend(['--model', model])
                    try:
                        result = subprocess.run(whisper_cmd, check=True)
                        if result.returncode == 0:
                            print_success("Whisper STT service installed")
                            logger.log_install('whisper', ['whisper'], True)
                        else:
                            print_warning("Whisper installation may not have completed successfully")
                            logger.log_install('whisper', ['whisper'], False)
                    except subprocess.CalledProcessError as e:
                        print_error(f"Whisper installation failed: {e}")
                        logger.log_install('whisper', ['whisper'], False)
                    except FileNotFoundError:
                        print_error("VoiceMode command not found. Cannot install Whisper.")
                        logger.log_install('whisper', ['whisper'], False)

                    # Install Kokoro
                    click.echo()
                    print_step("Installing Kokoro TTS service...")
                    kokoro_cmd = ['voicemode', 'service', 'install', 'kokoro']
                    try:
                        result = subprocess.run(kokoro_cmd, check=True)
                        if result.returncode == 0:
                            print_success("Kokoro TTS service installed")
                            logger.log_install('kokoro', ['kokoro'], True)
                        else:
                            print_warning("Kokoro installation may not have completed successfully")
                            logger.log_install('kokoro', ['kokoro'], False)
                    except subprocess.CalledProcessError as e:
                        print_error(f"Kokoro installation failed: {e}")
                        logger.log_install('kokoro', ['kokoro'], False)
                    except FileNotFoundError:
                        print_error("VoiceMode command not found. Cannot install Kokoro.")
                        logger.log_install('kokoro', ['kokoro'], False)
            else:
                click.echo("Cloud services recommended for your system configuration.")
                click.echo("Local services can still be installed if desired:")
                model_flag = f" --model {model}" if model != 'base' else ''
                click.echo(f"  voicemode whisper install{model_flag}")
                click.echo("  voicemode kokoro install")

        integration_results = []
        if integration_targets:
            click.echo()
            click.echo("━" * 70)
            click.echo(click.style("Agent Integrations", fg='blue', bold=True))
            click.echo("━" * 70)
            click.echo()
            integration_results = _run_integration_phase(integration_targets, dry_run=dry_run)

        # Completion summary
        click.echo()
        click.echo("━" * 70)
        click.echo(click.style("Installation Complete!", fg='green', bold=True))
        click.echo("━" * 70)
        click.echo()

        logger.log_complete(success=True, voicemode_installed=True)

        if dry_run:
            click.echo("DRY RUN: No changes were made to your system")
        else:
            click.echo("VoiceMode has been successfully installed!")
            click.echo()
            click.echo("Next steps:")
            click.echo("  1. Restart your terminal (or source your shell rc file)")
            click.echo("  2. Run: voicemode --help")
            if integration_results:
                click.echo("  3. Restart the configured agent CLIs so they reload MCP settings")
            else:
                click.echo("  3. Configure an agent integration, for example:")
                click.echo("     voice-mode-install --integrations codex")
            click.echo()
            click.echo(f"Installation log: {logger.get_log_path()}")

    except KeyboardInterrupt:
        click.echo("\n\nInstallation cancelled by user")
        logger.log_error("Installation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Installation failed: {e}")
        logger.log_error("Installation failed", e)
        if not dry_run:
            click.echo(f"\nFor troubleshooting, see: {logger.get_log_path()}")
        sys.exit(1)


def _print_integration_results(results):
    """Display integration changes in a compact format."""
    if not results:
        click.echo("No integrations requested.")
        return

    for result in results:
        status = "updated" if result.changed else "ok"
        color = "green" if result.changed else "blue"
        click.echo(f"  {click.style(status, fg=color)} {result.target}: {result.path}")
        click.echo(f"     {result.message}")


def _resolve_integration_targets(integrations: str, no_integrations: bool, non_interactive: bool) -> list[str]:
    """Resolve integration targets from flags, autodetection, or the interactive chooser."""
    if no_integrations and integrations:
        raise click.ClickException("--integrations and --no-integrations cannot be used together")

    if no_integrations:
        return []

    explicit_targets = parse_integrations(integrations)
    if explicit_targets:
        return explicit_targets

    if non_interactive or not sys.stdin.isatty():
        return [item.target for item in detect_installed_integrations() if item.detected]

    return _choose_integrations_interactively()


def _run_integration_phase(integration_targets: list[str], dry_run: bool):
    """Configure selected integrations and print a standard summary."""
    print_step("Configuring agent integrations...")
    integration_results = install_integrations(integration_targets, dry_run=dry_run)
    _print_integration_results(integration_results)
    return integration_results


def _finish_with_integrations_or_exit(integration_targets: list[str], dry_run: bool, logger: InstallLogger, exit_message: str) -> bool:
    """Run selected integrations when the user skips reinstalling VoiceMode."""
    if not integration_targets:
        click.echo(exit_message)
        sys.exit(0)

    click.echo("\nSkipping VoiceMode reinstall; continuing with selected integrations.")
    click.echo()
    _run_integration_phase(integration_targets, dry_run=dry_run)
    logger.log_complete(success=True, voicemode_installed=True)
    return True


def _choose_integrations_interactively() -> list[str]:
    """Ask the user which detected agent CLIs should be configured."""
    detections = detect_installed_integrations()
    selected_defaults = [item.target for item in detections if item.detected]

    click.echo("Detected agent CLIs:")
    for item in detections:
        mark = "[x]" if item.detected else "[ ]"
        status = "detected" if item.detected else "not found"
        click.echo(f"  {mark} {item.target:<8} {status} ({item.command})")

    click.echo()
    click.echo("Choose integrations by number or name. Press Enter to accept the preselected boxes.")
    click.echo("Examples: `1,2`, `codex,qwen`, `none`")

    label_map = {str(index): item.target for index, item in enumerate(detections, start=1)}
    for item in detections:
        label_map[item.target] = item.target

    default_display = ",".join(selected_defaults)
    raw = click.prompt("Integrations", default=default_display, show_default=bool(default_display)).strip()
    if not raw or raw == default_display:
        return selected_defaults
    if raw.lower() in {"none", "skip"}:
        return []

    chosen: list[str] = []
    seen: set[str] = set()
    invalid: list[str] = []
    for token in [part.strip().lower() for part in raw.split(",") if part.strip()]:
        resolved = label_map.get(token)
        if not resolved:
            invalid.append(token)
            continue
        if resolved not in seen:
            chosen.append(resolved)
            seen.add(resolved)

    if invalid:
        raise click.ClickException(f"Unknown integration selection: {', '.join(invalid)}")

    return chosen


if __name__ == '__main__':
    main()
