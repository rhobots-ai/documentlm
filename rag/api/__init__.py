"""FastAPI for the DocumentLM application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import logger
from .routers import health, chat, documents


# Function to create or get DocumentLM app instance
async def create_documentlm_app():
    """Initialize DocumentLM app instance."""
    try:
        # Try to import and get the app instance - IMPORTANT
        from libs.ktem.ktem.main import App
        try:
            # First try to get instance
            documentlm_app = App.get_instance()
        except (AttributeError, Exception):
            # If that fails, create a new instance
            documentlm_app = App()
    except ImportError:
        # Fallback if App is not available
        from libs.ktem.ktem.app import BaseApp
        documentlm_app = BaseApp.get_instance()
    return documentlm_app


# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Initialize DocumentLM app on startup
    fastapi_app.state.documentlm = await create_documentlm_app()
    logger.info("DocumentLM app initialized and stored in FastAPI state")
    yield
    # Clean up on shutdown if needed
    logger.info("FastAPI application shutting down")


def create_app():
    """Create and configure the FastAPI application."""
    fastapi_app = FastAPI(
        title="DocumentLM API",
        description="FastAPI-based backend for DocumentLM application",
        version="1.0.0",
        lifespan=lifespan
    )

    # Add CORS middleware
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    fastapi_app.include_router(health.router)
    fastapi_app.include_router(chat.router)
    fastapi_app.include_router(documents.router)

    # Log that app is initialized
    logger.info("FastAPI initialized with routers registered")

    return fastapi_app


# This is needed for uvicorn to run the app
app = create_app()
