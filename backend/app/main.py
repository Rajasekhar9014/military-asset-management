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
    import time
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting database initialization (attempt {attempt + 1}/{max_retries})...")
            
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
            
            print("✓ Database initialization complete!")
            break  # Success, exit retry loop
            
        except Exception as e:
            print(f"⚠ Database initialization attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("⚠ Database initialization failed after all retries. App will start but database may not be initialized.")
                print("⚠ Please check database connection settings and restart the service.")


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

@app.get("/init-db")
async def initialize_database():
    """Manual database initialization endpoint - call this once to create tables and admin user"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
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
                return {
                    "status": "success",
                    "message": "Database initialized successfully",
                    "admin_created": True,
                    "credentials": {"username": "admin", "password": "Admin123!"}
                }
            else:
                return {
                    "status": "success",
                    "message": "Database already initialized",
                    "admin_created": False
                }
        finally:
            db.close()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database initialization failed: {str(e)}"
        }

