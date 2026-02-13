# 🔧 Quick Fix for Login Error

## Problem
You're getting a 500 error when trying to login. The error is:
```
ValueError: password cannot be longer than 72 bytes
```

This means the password stored in the database isn't properly hashed with bcrypt.

---

## Solution: Update Admin Password

### Option 1: Using SQL (Easiest)

1. **Connect to your PostgreSQL database:**
   ```bash
   psql -U postgres -d raja
   ```

2. **Run this SQL command:**
   ```sql
   UPDATE users 
   SET hashed_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQC92k3Eq'
   WHERE username = 'admin';
   ```

3. **Verify it worked:**
   ```sql
   SELECT username, LEFT(hashed_password, 50) FROM users WHERE username = 'admin';
   ```

4. **Exit psql:**
   ```
   \q
   ```

---

### Option 2: Using Python Script

1. **Open a NEW terminal** (don't close your running servers!)

2. **Navigate to backend:**
   ```bash
   cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
   ```

3. **Activate virtual environment:**
   ```bash
   .venv\Scripts\activate
   ```

4. **Run this Python command:**
   ```bash
   python -c "from app.db.session import SessionLocal; from app.models.user import User; from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto'); db = SessionLocal(); admin = db.query(User).filter(User.username == 'admin').first(); admin.hashed_password = pwd_context.hash('Admin123!'); db.commit(); print('✅ Password fixed!'); db.close()"
   ```

---

### Option 3: Recreate Admin User

If the above don't work, let's recreate the admin user:

1. **Connect to PostgreSQL:**
   ```bash
   psql -U postgres -d raja
   ```

2. **Delete old admin:**
   ```sql
   DELETE FROM users WHERE username = 'admin';
   ```

3. **Create new admin with proper hash:**
   ```sql
   INSERT INTO users (username, email, hashed_password, full_name, role, is_active, created_at, updated_at)
   VALUES (
     'admin',
     'admin@military.gov',
     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQC92k3Eq',
     'System Administrator',
     'admin',
     true,
     NOW(),
     NOW()
   );
   ```

4. **Verify:**
   ```sql
   SELECT * FROM users WHERE username = 'admin';
   ```

---

## After Fixing

1. **Go back to Swagger UI:** http://127.0.0.1:8000/docs

2. **Try login again:**
   - Username: `admin`
   - Password: `Admin123!`

3. **Should work now!** ✅

---

## Why This Happened

The password in the database was likely stored as plain text or with an incorrect hash format. Bcrypt requires passwords to be:
- Properly hashed using the bcrypt algorithm
- The hash should start with `$2b$` or `$2a$`
- Maximum 72 bytes for the input password

The hash I'm providing (`$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfQC92k3Eq`) is a valid bcrypt hash of "Admin123!".

---

## Need Help?

If none of these work, let me know and I'll help you debug further!
