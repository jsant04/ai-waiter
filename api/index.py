"""
Vercel serverless entry point for the AI Waiter FastAPI backend.

Repo layout:
  api/index.py       ← Vercel entry point (this file)
  backend/main.py    ← FastAPI app
  backend/routers/   ← route handlers
  backend/services/  ← business logic
  backend/agents/    ← LangGraph agent
  backend/models/    ← Pydantic schemas

Vercel executes from /var/task/ (repo root). Without an explicit sys.path
fix, `from routers import ...` inside backend/main.py cannot be resolved.
This file adds backend/ to sys.path before anything else is imported.
"""
import os
import sys

# /var/task/api/../backend  →  /var/task/backend
_backend_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Import the FastAPI app – @vercel/python looks for a top-level `app`
from main import app  # noqa: E402
