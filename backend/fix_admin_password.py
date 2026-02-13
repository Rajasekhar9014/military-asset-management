"""
Quick script to fix the admin user password in the database.
This will update the admin user's password to use a properly hashed bcrypt password.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fix_admin_password():
    """Fix the admin user password"""
    db = SessionLocal()
    
    try:
        # Find admin user
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            print("❌ Admin user not found!")
            print("Creating admin user...")
            
            # Create admin user
            hashed_password = pwd_context.hash("Admin123!")
            admin = User(
                username="admin",
                email="admin@military.gov",
                hashed_password=hashed_password,
                full_name="System Administrator",
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created successfully!")
        else:
            print(f"Found admin user: {admin.username}")
            print(f"Current password hash: {admin.hashed_password[:50]}...")
            
            # Update password
            new_hash = pwd_context.hash("Admin123!")
            admin.hashed_password = new_hash
            db.commit()
            print("✅ Admin password updated successfully!")
            print(f"New password hash: {new_hash[:50]}...")
        
        # Verify the password works
        if pwd_context.verify("Admin123!", admin.hashed_password):
            print("✅ Password verification successful!")
            print("\nYou can now login with:")
            print("  Username: admin")
            print("  Password: Admin123!")
        else:
            print("❌ Password verification failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Fixing admin user password...\n")
    fix_admin_password()
