from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import settings
from app.api import auth, users, asset_categories, purchases, transfers, dashboard

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="REST API for Military Asset Management System with complete authentication and user management"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(asset_categories.router)
app.include_router(purchases.router)
app.include_router(transfers.router)
app.include_router(dashboard.router)

# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Military Asset Management System API",
        "version": settings.APP_VERSION,
        "status": "running",
        "database": settings.DATABASE_NAME,
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "login": "/api/v1/auth/login",
            "users": "/api/v1/users",
            "categories": "/api/v1/categories",
            "purchases": "/api/v1/purchases",
            "transfers": "/api/v1/transfers",
            "dashboard": "/api/v1/dashboard/metrics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.APP_VERSION
    }
