from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,        # Connection pool size
    max_overflow=20,     # Max connections beyond pool_size
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    """
    Database session dependency.
    Use in route handlers: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
