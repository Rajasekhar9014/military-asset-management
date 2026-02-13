"""
Direct SQL execution to create tables in raja database
"""
import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_PARAMS = {
    'dbname': 'raja',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

def create_tables():
    """Create users table and insert admin user"""
    try:
        # Connect to database
        print("Connecting to database 'raja'...")
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        print("✓ Connected successfully!")
        print()
        
        # Create users table
        print("Creating users table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role_id INTEGER NOT NULL DEFAULT 1,
                unit_id INTEGER,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );
        """)
        
        # Create indexes
        print("Creating indexes...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);")
        
        # Insert admin user
        print("Inserting admin user...")
        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
        """, (
            'admin',
            'admin@military.mil',
            '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS6NzHZUu',
            'System Administrator',
            1,
            True
        ))
        
        # Commit changes
        conn.commit()
        
        # Verify
        print()
        print("Verifying...")
        cur.execute("SELECT COUNT(*) FROM users;")
        count = cur.fetchone()[0]
        
        cur.execute("SELECT id, username, email, full_name FROM users;")
        users = cur.fetchall()
        
        print()
        print("=" * 60)
        print("✅ SUCCESS! Tables created in 'raja' database")
        print("=" * 60)
        print()
        print(f"Total users: {count}")
        for user in users:
            print(f"  - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
        print()
        print("Login credentials:")
        print("  Username: admin")
        print("  Password: Admin123!")
        print()
        print("=" * 60)
        
        cur.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = create_tables()
    if success:
        print()
        print("Next step: Start the server!")
        print("  cd backend")
        print("  python -m uvicorn app.main:app --reload")
    else:
        print()
        print("Failed to create tables. Please check:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'raja' exists")
        print("  3. Password is correct (1234)")
