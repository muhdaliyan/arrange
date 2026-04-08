"""arrange add — Thin wrapper over uv add that maintains requirements.txt."""

import typer
from arrange.utils import (
    check_uv,
    ensure_venv_exists,
    print_banner,
    print_done,
    run,
)

def run_command(packages: list[str]) -> None:
    """Add packages using uv and update requirements.txt."""
    print_banner("add", f"Adding packages: {', '.join(packages)}")

    check_uv()
    ensure_venv_exists()

    # Add packages
    pkg_str = " ".join(packages)
    run(f"uv add {pkg_str}")

    # Update requirements.txt for compatibility
    run("uv export --format requirements-txt --output-file requirements.txt --quiet")

    print_done()
