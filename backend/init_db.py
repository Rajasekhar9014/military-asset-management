"""
Database initialization script for Render deployment.
Creates all tables and initializes admin user.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import engine, SessionLocal, Base
from app.models.user import User
from app.models.asset_category import AssetCategory
from app.models.purchase import Purchase
from app.models.transfer import Transfer
from app.utils.security import hash_password

def init_database():
    """Initialize database with tables and admin user"""
    print("Creating database tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")
    
    # Create admin user
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        
        if not existing_admin:
            print("Creating admin user...")
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
            print("✓ Admin user created successfully")
            print("  Username: admin")
            print("  Password: Admin123!")
        else:
            print("✓ Admin user already exists")
            
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n✓ Database initialization complete!")

if __name__ == "__main__":
    init_database()
