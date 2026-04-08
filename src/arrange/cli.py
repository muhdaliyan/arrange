"""arrange CLI — Main entry point."""

import typer
from rich.console import Console

from arrange import __version__
from arrange.commands import (
    activate,
    add,
    api,
    cli_cmd,
    django_cmd,
    docs,
    lang_agent,
    mean,
    mern,
    ml,
    next_django,
    notebook,
    openai_agent,
    react_fastapi,
    saas,
    scraper,
    test_cmd,
    uv,
)

console = Console()

app = typer.Typer(
    name="arrange",
    help="Scaffold production-ready project structures in seconds.",
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"[bold cyan]arrange[/bold cyan] v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit.", callback=_version_callback, is_eager=True
    ),
) -> None:
    """arrange — Install once, scaffold forever."""


# ── Foundation commands ──────────────────────────────────────────────

@app.command()
def uv_cmd() -> None:
    """[bold cyan]Foundation[/bold cyan] · Bootstrap a complete uv Python project."""
    uv.run_command()


# Register as "uv" not "uv-cmd"
uv_cmd.__name__ = "uv"  # type: ignore[attr-defined]
uv_cmd = app.registered_commands[-1]
uv_cmd.name = "uv"


@app.command(name="activate")
def activate_cmd() -> None:
    """[bold cyan]Foundation[/bold cyan] · Smart cross-platform venv activator."""
    activate.run_command()


@app.command(name="add")
def add_cmd(packages: list[str]) -> None:
    """[bold cyan]Foundation[/bold cyan] · Add packages and sync requirements.txt."""
    add.run_command(packages)


# ── Template commands ────────────────────────────────────────────────

@app.command(name="react-fastapi")
def react_fastapi_cmd() -> None:
    """[bold magenta]Full-stack[/bold magenta] · React + FastAPI with Docker Compose & CORS."""
    react_fastapi.run_command()


@app.command(name="notebook")
def notebook_cmd() -> None:
    """[bold green]Data Science[/bold green] · Jupyter notebooks with uv-managed deps."""
    notebook.run_command()


@app.command(name="mern")
def mern_cmd() -> None:
    """[bold magenta]Full-stack[/bold magenta] · MongoDB + Express + React + Node."""
    mern.run_command()


@app.command(name="mean")
def mean_cmd() -> None:
    """[bold magenta]Full-stack[/bold magenta] · MongoDB + Express + Angular + Node."""
    mean.run_command()


@app.command(name="django")
def django_cmd_fn() -> None:
    """[bold blue]Backend[/bold blue] · Django + DRF + Celery + Redis + PostgreSQL."""
    django_cmd.run_command()


@app.command(name="next-django")
def next_django_cmd() -> None:
    """[bold magenta]Full-stack[/bold magenta] · Next.js 14 + Django REST + JWT auth."""
    next_django.run_command()


@app.command(name="ml")
def ml_cmd() -> None:
    """[bold green]Data Science[/bold green] · ML project with experiment tracking & MLflow."""
    ml.run_command()


@app.command(name="lang-agent")
def lang_agent_cmd() -> None:
    """[bold yellow]AI[/bold yellow] · LangGraph agent with tool stubs & Ollama config."""
    lang_agent.run_command()


@app.command(name="openai-agent")
def openai_agent_cmd() -> None:
    """[bold yellow]AI[/bold yellow] · Modern OpenAI agent with function calling."""
    openai_agent.run_command()


@app.command(name="scraper")
def scraper_cmd() -> None:
    """[bold yellow]Automation[/bold yellow] · Playwright + BeautifulSoup scraping pipeline."""
    scraper.run_command()


@app.command(name="cli")
def cli_cmd_fn() -> None:
    """[bold blue]Package[/bold blue] · PyPI-ready CLI package with Typer + Rich."""
    cli_cmd.run_command()


@app.command(name="api")
def api_cmd() -> None:
    """[bold blue]Backend[/bold blue] · Minimal FastAPI microservice with auth middleware."""
    api.run_command()


@app.command(name="saas")
def saas_cmd() -> None:
    """[bold magenta]Full-stack[/bold magenta] · Full SaaS boilerplate with Stripe & Docker."""
    saas.run_command()


@app.command(name="docs")
def docs_cmd() -> None:
    """[bold dim]Addon[/bold dim] · Add MkDocs + Material theme to any project."""
    docs.run_command()


@app.command(name="test")
def test_cmd_fn() -> None:
    """[bold dim]Addon[/bold dim] · Scaffold a full pytest suite with coverage."""
    test_cmd.run_command()


if __name__ == "__main__":
    app()
