import os
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Vercel runs from the repo root (/var/task), so `backend/` subdirectories
# (routers, services, models, agents) are not on sys.path by default.
# This ensures all relative imports resolve correctly both locally and on Vercel.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("🍽️  AI Waiter API starting up...")
    yield
    logger.info("AI Waiter API shutting down...")


app = FastAPI(
    title="AI Waiter API",
    description=(
        "Intelligent restaurant assistant powered by LangGraph Agentic RAG. "
        "Upload your Excel menu and let customers chat with an AI that knows every dish."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────
origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:3000")
origins = [o.strip() for o in origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # Automatically allow all Vercel preview deployment URLs (*.vercel.app)
    allow_origin_regex=r"https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────
from routers import chat, upload  # noqa: E402

app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(upload.router, prefix="/api", tags=["Menu Upload"])


# ── Health Endpoints ──────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "AI Waiter API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "message": "Your AI Waiter is ready to serve 👋",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "AI Waiter API"}
