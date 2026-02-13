from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import settings
from app.api import auth, users, asset_categories, purchases, transfers, dashboard
from app.db.session import engine, SessionLocal, Base
from app.models.user import User
from app.utils.security import hash_password

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

# Startup event to initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created/verified")
        
        # Create admin user if it doesn't exist
        db = SessionLocal()
        try:
            existing_admin = db.query(User).filter(User.username == "admin").first()
            if not existing_admin:
                admin_user = User(
                    username="admin",
                    email="admin@military.gov",
                    full_name="System Administrator",
                    hashed_password=hash_password("Admin123!"),
                    role="admin",
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                print("✓ Admin user created (username: admin, password: Admin123!)")
            else:
                print("✓ Admin user already exists")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠ Database initialization error: {e}")

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
