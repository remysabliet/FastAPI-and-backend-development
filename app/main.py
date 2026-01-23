"""Main FastAPI application."""

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.init_db import init_db

# Initialize database on startup
init_db()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", include_in_schema=False)
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Shipment API",
        "docs": "/docs",
        "scalar_docs": "/docs/scalar",
    }


@app.get("/docs/scalar", include_in_schema=False)
def get_scalar_docs():
    """Get Scalar API documentation."""
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
