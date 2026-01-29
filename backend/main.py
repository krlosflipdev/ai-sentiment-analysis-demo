"""FastAPI application for AI Sentiment Analysis."""

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import close_mongodb_connection, connect_to_mongodb
from app.exceptions import APIException, api_exception_handler
from app.routes import sentiments, stats

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Manages startup and shutdown events for the application.
    Connects to MongoDB on startup and closes the connection on shutdown.
    """
    # Startup
    await connect_to_mongodb()
    yield
    # Shutdown
    await close_mongodb_connection()


app = FastAPI(
    title="AI Sentiment Analysis API",
    description="Real-time sentiment analysis using NLP/ML",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(APIException, api_exception_handler)

# Register routers
app.include_router(sentiments.router)
app.include_router(stats.router)


@app.get("/health")
async def health_check():
    """Root health check endpoint."""
    return {"status": "ok"}


@app.get("/api/v1/health")
async def api_health_check():
    """API v1 health check endpoint with version info."""
    return {"status": "ok", "version": "v1"}
