"""
Test database connection and create tables.
Uses credentials: postgresql://postgres:1234@localhost:5432/kristalball
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

print("=" * 60)
print("CREATING DATABASE TABLES")
print("=" * 60)
print()

try:
    from app.config import settings
    print(f"✓ Configuration loaded")
    print(f"  Database: {settings.DATABASE_NAME}")
    print(f"  Host: {settings.DATABASE_HOST}:{settings.DATABASE_PORT}")
    print(f"  User: {settings.DATABASE_USER}")
    print()
except Exception as e:
    print(f"✗ Failed to load configuration: {e}")
    sys.exit(1)

try:
    from app.db.session import Base, engine
    print(f"✓ Database engine created")
    print(f"  URL: {engine.url}")
    print()
except Exception as e:
    print(f"✗ Failed to create engine: {e}")
    sys.exit(1)

try:
    from app.models.user import User
    print(f"✓ Models imported")
    print()
except Exception as e:
    print(f"✗ Failed to import models: {e}")
    sys.exit(1)

try:
    # Test connection
    with engine.connect() as conn:
        print(f"✓ Database connection successful!")
        print()
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    print()
    print("Troubleshooting:")
    print("1. Is PostgreSQL running?")
    print("2. Does database 'kristalball' exist?")
    print("3. Is password correct? (currently: 1234)")
    sys.exit(1)

try:
    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print()
    
    # List created tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"✓ Tables created successfully!")
    print()
    print("Tables in database:")
    for table in tables:
        columns = inspector.get_columns(table)
        print(f"  • {table} ({len(columns)} columns)")
    
    print()
    print("=" * 60)
    print("SUCCESS! Database tables are ready!")
    print("=" * 60)
    print()
    print("Next step: Run create_test_user.py to create admin user")
    print()
    
except Exception as e:
    print(f"✗ Failed to create tables: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
