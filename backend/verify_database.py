"""
Verify database tables and connection.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import engine, SessionLocal
from app.models.user import User
from sqlalchemy import inspect, text

def verify_database():
    """Verify database connection and tables"""
    print("=" * 50)
    print("DATABASE VERIFICATION")
    print("=" * 50)
    print()
    
    # Check connection
    try:
        print(f"📍 Database URL: {engine.url}")
        print(f"📍 Database Name: {engine.url.database}")
        print()
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ PostgreSQL Connection: SUCCESS")
            print(f"   Version: {version[:50]}...")
            print()
    except Exception as e:
        print(f"❌ Database Connection: FAILED")
        print(f"   Error: {e}")
        return False
    
    # Check tables
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"📊 Tables in database '{engine.url.database}':")
        if tables:
            for table in tables:
                columns = inspector.get_columns(table)
                print(f"   ✅ {table} ({len(columns)} columns)")
        else:
            print("   ⚠️  No tables found!")
            print()
            print("   Run this to create tables:")
            print("   python create_tables.py")
            return False
        
        print()
        
        # Check for users table specifically
        if 'users' in tables:
            db = SessionLocal()
            try:
                user_count = db.query(User).count()
                print(f"👥 Users table:")
                print(f"   Total users: {user_count}")
                
                if user_count > 0:
                    users = db.query(User).all()
                    for user in users:
                        print(f"   - {user.username} ({user.email})")
                else:
                    print("   ⚠️  No users found!")
                    print()
                    print("   Run this to create test user:")
                    print("   python create_test_user.py")
            finally:
                db.close()
        
        print()
        print("=" * 50)
        print("✅ DATABASE VERIFICATION COMPLETE")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

if __name__ == "__main__":
    verify_database()
