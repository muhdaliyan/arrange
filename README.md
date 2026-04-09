# stup

> 🚀 Scaffold production-ready project structures in seconds. Install once, scaffold forever.

```bash
pip install stup
```

## Foundation Commands

### `stup uv`

Bootstraps a complete uv Python project. Run this first before any template.

```bash
$ stup uv
```

- `uv init` — creates pyproject.toml and project skeleton
- `uv python pin 3.12` — pins Python version
- `uv venv` — creates virtual environment
- Prints activation command (cross-platform)

### `stup activate`

Smart cross-platform venv activator — detects your shell and prints the right command.

- **Windows PowerShell:** `.venv\Scripts\Activate`
- **Linux/Mac bash/zsh:** `source .venv/bin/activate`

### `stup add <packages>`

Add packages using `uv` and automatically maintain a clean `requirements.txt`.

```bash
$ stup add requests pandas
```

---

## Template Commands

Each template builds on top of `stup uv`. Run `stup uv` first, then pick your template.

### `stup react-fastapi`

| | |
|---|---|
| **Description** | Full-stack web app — React frontend + FastAPI backend with Docker Compose and CORS pre-configured |
| **Stack** | Python + JavaScript (Vite, React, Tailwind, FastAPI, Alembic) |
| **Installs** | `uv add fastapi uvicorn alembic` \| `npm install react tailwindcss vite` |
| **Structure** | `frontend/` `backend/` `docker-compose.yml` `.env` |

### `stup notebook`

| | |
|---|---|
| **Description** | Data science workspace with Jupyter notebooks, uv-managed deps, kernel auto-registered |
| **Stack** | Python + Jupyter |
| **Installs** | `uv add ipykernel pandas numpy matplotlib` |
| **Structure** | `notebooks/` `data/raw/` `data/processed/` |

### `stup openai-agent`

| | |
|---|---|
| **Description** | Modern OpenAI agent with function calling (tools), environment config, and helper stubs |
| **Stack** | Python (OpenAI SDK, python-dotenv) |
| **Installs** | `uv add openai python-dotenv` |
| **Structure** | `agent.py` `tools/` `.env` (OPENAI_API_KEY) |

### `stup lang-agent`

| | |
|---|---|
| **Description** | LangGraph AI agent with tool stubs, memory/checkpointing, and Ollama config |
| **Stack** | Python (LangGraph, LangChain, Ollama) |
| **Installs** | `uv add langgraph langchain-community` |
| **Structure** | `agent.py` `tools/` `memory/` `.env` (OLLAMA_BASE_URL) |

### `stup django`

| | |
|---|---|
| **Description** | Production-ready Django + DRF + Celery + Redis + PostgreSQL setup with python-decouple |
| **Stack** | Python (Django, DRF, Celery, Redis, PostgreSQL) |
| **Installs** | `uv add django djangorestframework celery redis python-decouple` |
| **Structure** | `config/` `apps/users/` `apps/api/` `tasks/` `.env` |

### `stup ml`

| | |
|---|---|
| **Description** | ML project scaffold with experiment tracking, model versioning, and MLflow stub |
| **Stack** | Python (scikit-learn, PyTorch, MLflow) |
| **Installs** | `uv add scikit-learn torch mlflow` |
| **Structure** | `data/` `models/` `experiments/runs/` `experiments/configs/` |

### `stup scraper`

| | |
|---|---|
| **Description** | Web scraping project with Playwright, BeautifulSoup, pandas output pipeline and scheduler |
| **Stack** | Python (Playwright, BeautifulSoup4, pandas) |
| **Installs** | `uv add playwright beautifulsoup4 pandas schedule` + `playwright install chromium` |
| **Structure** | `spider.py` `pipeline.py` `data/raw/` `data/cleaned/` |

### `stup cli`

| | |
|---|---|
| **Description** | PyPI-ready Python CLI package with Typer + Rich, entry_points wired in pyproject.toml |
| **Stack** | Python (Typer, Rich) |
| **Installs** | `uv add typer rich` |
| **Structure** | `src/<project>/` `commands/` `pyproject.toml` `README.md` |

---

## Quick Reference

| Command | Stack | Use Case |
|---------|-------|----------|
| `stup uv` | Python | Start any Python project |
| `stup activate` | Python | Activate venv cross-platform |
| `stup add` | Python | Add deps & sync requirements.txt |
| `stup react-fastapi` | Py + JS | Full-stack web app |
| `stup notebook` | Python | Data science / Jupyter |
| `stup openai-agent` | Python | Modern OpenAI Agent |
| `stup lang-agent` | Python | LangGraph AI agent |
| `stup django` | Python | Full Django + Celery API |
| `stup ml` | Python | ML project + MLflow |
| `stup scraper` | Python | Web scraping pipeline |
| `stup cli` | Python | PyPI-ready CLI package |

---

## Development

```bash
git clone https://github.com/muhdaliyan/stup.git
cd stup
uv venv
uv pip install -e ".[dev]"
stup --help
```

## License

MIT
