# 🔧 Fix: No Tables in Database

## Problem
You're not seeing tables in your `kristalball` database in pgAdmin.

## Solution - Run These Commands

### Option 1: Double-Click This File
**File: `create_db_simple.bat`** (in F-API folder)

This will:
1. Create the `users` table
2. Create a test admin user

### Option 2: Manual Commands (If batch file doesn't work)

Open **Command Prompt** (not PowerShell) and run:

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend

python verify_database.py
```

This will show you:
- ✅ If database connection works
- ✅ What tables exist
- ✅ How many users exist

If no tables exist, run:

```cmd
python create_tables.py
```

Then create test user:

```cmd
python create_test_user.py
```

Then verify again:

```cmd
python verify_database.py
```

### Option 3: Check in pgAdmin

1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Navigate to: Servers → PostgreSQL → Databases → kristalball → Schemas → public → Tables
4. Right-click on "Tables" → Refresh
5. You should see the `users` table

### What You Should See

After running the scripts successfully, in pgAdmin you should see:

**Tables:**
- `users` (with columns: id, username, email, password_hash, full_name, role_id, unit_id, is_active, created_at, updated_at, last_login)

**Test User:**
- Username: `admin`
- Email: `admin@military.mil`

## Troubleshooting

**"ModuleNotFoundError":**
```cmd
pip install fastapi sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings passlib python-jose
```

**"Connection refused":**
- Make sure PostgreSQL is running
- Check your `.env` file has correct password (currently: `1234`)

**"Database does not exist":**
- Make sure you created the `kristalball` database in pgAdmin
- Connection string: `postgresql://postgres:1234@localhost:5432/kristalball`

## Quick Test

Run this one command to test everything:

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python verify_database.py
```

This will tell you exactly what's in your database!
