"""stup react-fastapi — React frontend + FastAPI backend scaffold."""

from app.utils import (
    check_node,
    check_uv,
    create_dirs,
    delete_dir,
    ensure_venv_exists,
    print_banner,
    print_done,
    print_step,
    run,
    write_file,
)


# ── Templates ────────────────────────────────────────────────────────

BACKEND_MAIN = '''\
"""FastAPI backend entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My App API", version="0.1.0")

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}


@app.get("/health")
async def health():
    return {"status": "ok"}
'''

BACKEND_MODELS = '''\
"""Database models."""

# Add your SQLAlchemy / Pydantic models here.
'''

BACKEND_ROUTERS_INIT = '''\
"""API routers."""
'''

DOCKER_COMPOSE = '''\
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    env_file:
      - .env
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host
'''

ENV_FILE = '''\
# Backend
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=change-me-in-production

# Frontend (Vite exposes VITE_ prefixed vars)
VITE_API_URL=http://localhost:8000
'''

BACKEND_DOCKERFILE = '''\
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn alembic sqlalchemy

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

FRONTEND_DOCKERFILE = '''\
FROM node:20-slim

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

CMD ["npm", "run", "dev", "--", "--host"]
'''


def run_command() -> None:
    """Scaffold a React + FastAPI full-stack project."""
    print_banner("react-fastapi", "React frontend + FastAPI backend with Docker Compose")

    check_uv()
    check_node()
    ensure_venv_exists()

    # ── Backend ──────────────────────────────────────────────────────
    create_dirs("backend", "backend/routers", "backend/models")

    run("uv add fastapi uvicorn alembic sqlalchemy")

    write_file("backend/main.py", BACKEND_MAIN)
    write_file("backend/models/__init__.py", BACKEND_MODELS)
    write_file("backend/routers/__init__.py", BACKEND_ROUTERS_INIT)
    write_file("backend/Dockerfile", BACKEND_DOCKERFILE)

    # Initialize alembic
    run("uv run alembic init backend/alembic")

    # ── Frontend ─────────────────────────────────────────────────────
    print_step("Creating React frontend with Vite...")
    delete_dir("frontend")
    run("npx -y create-vite@latest frontend --template react")
    
    print_step("Installing frontend dependencies (this may take a minute)...")
    run("npm install", cwd="frontend")
    run("npm install -D tailwindcss @tailwindcss/vite", cwd="frontend")
    write_file("frontend/Dockerfile", FRONTEND_DOCKERFILE)

    # ── Root files ───────────────────────────────────────────────────
    write_file("docker-compose.yml", DOCKER_COMPOSE)
    write_file(".env", ENV_FILE)

    print_done()
