"""Shared utilities for arrange CLI."""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


# ── Rich output helpers ──────────────────────────────────────────────

def print_banner(command: str, description: str) -> None:
    """Print a styled banner when a command starts."""
    title = Text()
    title.append("arrange ", style="bold cyan")
    title.append(command, style="bold white")
    console.print(Panel(title, subtitle=description, border_style="cyan", padding=(0, 2)))


def print_step(msg: str) -> None:
    """Print a step indicator."""
    console.print(f"  [cyan]▸[/cyan] {msg}")


def print_success(msg: str) -> None:
    """Print a success message."""
    console.print(f"  [green]✓[/green] {msg}")


def print_warning(msg: str) -> None:
    """Print a warning message."""
    console.print(f"  [yellow]⚠[/yellow] {msg}")


def print_error(msg: str) -> None:
    """Print an error and exit."""
    console.print(f"  [red]✗[/red] {msg}")


def print_done() -> None:
    """Print final done message."""
    console.print()
    console.print("  [bold green]Done![/bold green] Your project is ready.")
    console.print()


# ── Command execution ────────────────────────────────────────────────

def run(cmd: str, cwd: str | None = None, capture: bool = False, silent: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command with a clean status spinner.

    Args:
        cmd: Command string to execute.
        cwd: Working directory. Defaults to current directory.
        capture: If True, capture stdout/stderr.
        silent: If True, suppress all output (even status).
    """
    msg = f"Running: [dim]{cmd}[/dim]"
    
    if silent:
        return subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or os.getcwd(),
            capture_output=capture,
            text=True,
            check=True,
        )

    with console.status(f"  [cyan]▸[/cyan] {msg}", spinner="dots"):
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or os.getcwd(),
                capture_output=True, # Always capture to keep CLI clean
                text=True,
                check=True,
            )
            return result
        except subprocess.CalledProcessError as e:
            print_error(f"Command failed: {cmd}")
            if e.stdout:
                console.print(f"    [dim]{e.stdout.strip()}[/dim]")
            if e.stderr:
                console.print(f"    [dim red]{e.stderr.strip()}[/dim red]")
            sys.exit(1)


# ── Tool checks ──────────────────────────────────────────────────────

def check_tool(name: str, install_hint: str | None = None) -> None:
    """Check if a CLI tool is available on PATH."""
    if shutil.which(name) is None:
        hint = install_hint or f"Please install '{name}' first."
        print_error(f"'{name}' not found on PATH. {hint}")
        sys.exit(1)


def check_uv() -> None:
    """Verify uv is installed."""
    check_tool("uv", install_hint="Install from https://docs.astral.sh/uv/getting-started/installation/")


def check_node() -> None:
    """Verify node and npm are installed."""
    check_tool("node", install_hint="Install from https://nodejs.org/")
    check_tool("npm", install_hint="Install from https://nodejs.org/")


# ── File / directory helpers ─────────────────────────────────────────

def create_dirs(*paths: str) -> None:
    """Create directories (relative to cwd). Idempotent."""
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)
        print_success(f"Created {p}/")


def write_file(path: str, content: str) -> None:
    """Write content to a file, creating parent dirs as needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print_success(f"Created {path}")


# ── Platform detection ───────────────────────────────────────────────

def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def get_activate_command() -> str:
    """Return the correct venv activation command for the current platform."""
    if is_windows():
        return r".venv\Scripts\Activate.ps1"
    return "source .venv/bin/activate"


def print_activate_hint() -> None:
    """Print how to activate the venv."""
    cmd = get_activate_command()
    console.print()
    console.print(f"  [green]✓[/green] Environment ready. Activate it with:")
    console.print(f"    [bold cyan]{cmd}[/bold cyan]")
    console.print()


def ensure_venv_exists() -> None:
    """Check that .venv exists, or create it automatically."""
    if not Path(".venv").exists():
        print_warning("No .venv found. Bootstrapping environment...")
        from arrange.commands import uv
        uv.run_command()
