"""stup saas — Full SaaS boilerplate with Stripe, Celery, Docker."""

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

ENV_FILE = '''\
# Django
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=saas_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# Stripe
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_STRIPE_KEY=pk_test_your_key_here
'''

DOCKER_COMPOSE = '''\
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: saas_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery:
    build: ./backend
    command: celery -A config worker -l info
    volumes:
      - ./backend:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    env_file:
      - .env

volumes:
  postgres_data:
'''

BILLING_VIEWS = '''\
"""Stripe billing views."""

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
@require_POST
def create_checkout_session(request):
    """Create a Stripe checkout session."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": "price_xxx",  # TODO: Replace with your Stripe price ID
                "quantity": 1,
            }],
            mode="subscription",
            success_url="http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:3000/cancel",
        )
        return JsonResponse({"sessionId": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_POST
def webhook(request):
    """Handle Stripe webhooks."""
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Handle events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: Provision the subscription
        print(f"Checkout completed: {session['id']}")

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        # TODO: Handle cancellation
        print(f"Subscription cancelled: {subscription['id']}")

    return JsonResponse({"status": "ok"})
'''

AUTH_VIEWS = '''\
"""Authentication views."""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json


@csrf_exempt
@require_POST
def register(request):
    """Register a new user."""
    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({"message": "User created", "user_id": user.id}, status=201)


@csrf_exempt
@require_POST
def login(request):
    """Login and return token."""
    data = json.loads(request.body)
    user = authenticate(username=data.get("username"), password=data.get("password"))

    if user is not None:
        # TODO: Return JWT or session token
        return JsonResponse({"message": "Login successful", "user_id": user.id})
    return JsonResponse({"error": "Invalid credentials"}, status=401)
'''

BACKEND_DOCKERFILE = '''\
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
'''


def run_command() -> None:
    """Scaffold a full SaaS boilerplate."""
    print_banner("saas", "Full SaaS boilerplate — auth, Stripe, Celery, Docker")

    check_uv()
    check_node()
    ensure_venv_exists()

    # ── Backend ──────────────────────────────────────────────────────
    create_dirs("backend")
    run("uv add django stripe celery redis djangorestframework django-cors-headers python-decouple psycopg2-binary")
    run("uv run django-admin startproject config backend/")

    create_dirs(
        "backend/auth",
        "backend/billing",
        "backend/api",
    )

    write_file("backend/auth/__init__.py", "")
    write_file("backend/auth/views.py", AUTH_VIEWS)
    write_file("backend/billing/__init__.py", "")
    write_file("backend/billing/views.py", BILLING_VIEWS)
    write_file("backend/api/__init__.py", "")
    write_file("backend/Dockerfile", BACKEND_DOCKERFILE)

    # ── Frontend ─────────────────────────────────────────────────────
    print_step("Creating React frontend with Vite...")
    delete_dir("frontend")
    run("npx -y create-vite@latest frontend --template react")
    
    print_step("Installing frontend dependencies...")
    run("npm install", cwd="frontend")
    run("npm install @stripe/stripe-js axios react-router-dom", cwd="frontend")

    # ── Root config ──────────────────────────────────────────────────
    write_file("docker-compose.yml", DOCKER_COMPOSE)
    write_file(".env", ENV_FILE)

    print_done()
