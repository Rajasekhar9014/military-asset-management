# ✅ FINAL SETUP - Run Your Server Successfully

## 🎯 Current Status

- ✅ Database: `raja` configured in `.env`
- ✅ Code: All files ready
- ✅ Dependencies: Installed

## 🚀 STEP-BY-STEP TO RUN SUCCESSFULLY

### Step 1: Create Tables in pgAdmin (2 minutes)

1. **Open pgAdmin**
2. **Right-click `raja` database** → **Query Tool**
3. **Copy this SQL** and paste into the query window:

```sql
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

INSERT INTO users (username, email, password_hash, full_name, role_id, is_active)
VALUES (
    'admin',
    'admin@military.mil',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS6NzHZUu',
    'System Administrator',
    1,
    TRUE
)
ON CONFLICT (username) DO NOTHING;
```

4. **Click Execute** (▶️ button or F5)
5. **Verify**: Right-click Tables → Refresh → You'll see `users` table!

### Step 2: Start the Server

**Open Command Prompt** (not PowerShell) and run:

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python -m uvicorn app.main:app --reload
```

**You'll see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Step 3: Test in Chrome

1. **Open Chrome**
2. **Visit**: http://127.0.0.1:8000/docs
3. **You'll see**: Swagger UI with all your endpoints!

### Step 4: Login

1. Find **POST /api/v1/auth/login**
2. Click **"Try it out"**
3. Enter:
```json
{
  "username": "admin",
  "password": "Admin123!"
}
```
4. Click **"Execute"**
5. **Copy the `access_token`**

### Step 5: Test Protected Endpoints

1. Click 🔒 **"Authorize"** (top right)
2. Enter: `Bearer <paste_your_token>`
3. Click **"Authorize"**
4. Now test **GET /api/v1/users/me**
5. ✅ **SUCCESS!** You'll see your user info!

## 🎯 Quick Commands Reference

**Start Server:**
```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python -m uvicorn app.main:app --reload
```

**Stop Server:**
Press `CTRL+C` in the terminal

**Access URLs:**
- Swagger UI: http://127.0.0.1:8000/docs
- API Root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health

**Test Credentials:**
- Username: `admin`
- Password: `Admin123!`

## ✅ Success Checklist

- [ ] Tables created in `raja` database (verify in pgAdmin)
- [ ] Server started (see "Application startup complete")
- [ ] Swagger UI loads (http://127.0.0.1:8000/docs)
- [ ] Login works (returns access_token)
- [ ] Protected endpoints work (after authorization)

## 🔧 If Something Goes Wrong

**Tables not showing in pgAdmin:**
- Make sure you selected `raja` database before running SQL
- Refresh the Tables view

**Server won't start:**
```cmd
pip install -r requirements.txt
```

**Port already in use:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <number> /F
```

## ✨ You're Ready!

Just follow the 5 steps above and your server will be running successfully! 🚀
