"""
Create test user with detailed output.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

print("=" * 60)
print("CREATING TEST USER")
print("=" * 60)
print()

try:
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.utils.security import hash_password
    
    db = SessionLocal()
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == "admin").first()
    if existing_user:
        print("⚠️  Test user 'admin' already exists!")
        print()
        print(f"User details:")
        print(f"  ID: {existing_user.id}")
        print(f"  Username: {existing_user.username}")
        print(f"  Email: {existing_user.email}")
        print(f"  Full Name: {existing_user.full_name}")
        print(f"  Active: {existing_user.is_active}")
        print()
        print("You can use this user to login:")
        print("  Username: admin")
        print("  Password: Admin123!")
        db.close()
        sys.exit(0)
    
    # Create test user
    print("Creating admin user...")
    test_user = User(
        username="admin",
        email="admin@military.mil",
        password_hash=hash_password("Admin123!"),
        full_name="System Administrator",
        role_id=1,
        is_active=True
    )
    
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    print()
    print("=" * 60)
    print("✅ TEST USER CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Login credentials:")
    print(f"  Username: admin")
    print(f"  Password: Admin123!")
    print(f"  Email: admin@military.mil")
    print()
    print(f"User ID: {test_user.id}")
    print()
    print("Next step: Run start_server.bat to start the API")
    print()
    
    db.close()
    
except Exception as e:
    print(f"✗ Error creating test user: {e}")
    import traceback
    traceback.print_exc()
    if 'db' in locals():
        db.rollback()
        db.close()
    sys.exit(1)
