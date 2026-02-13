# 🚨 SERVER NOT STARTING - MANUAL FIX

## Problem
ERR_CONNECTION_REFUSED means the server isn't running.

## ✅ SOLUTION - Start Server Manually

### Step 1: Open Command Prompt (NOT PowerShell)
1. Press `Win + R`
2. Type: `cmd`
3. Press Enter

### Step 2: Navigate and Start Server
Copy and paste these commands ONE AT A TIME:

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
```

Then:

```cmd
python -m uvicorn app.main:app --reload
```

### Step 3: Watch for Success Message

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Step 4: If You See Errors

**"ModuleNotFoundError: No module named 'fastapi'"**
```cmd
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings passlib python-jose email-validator
```

**"ModuleNotFoundError: No module named 'pydantic_settings'"**
```cmd
pip install pydantic-settings
```

**"Database connection error"**
- Make sure PostgreSQL is running
- Make sure database `raja` exists in pgAdmin
- Check `.env` file has correct password

**"Port 8000 already in use"**
```cmd
netstat -ano | findstr :8000
taskkill /PID <number_you_see> /F
```

Then try starting the server again.

### Step 5: Once Server Starts

**Keep the Command Prompt window open!**

Then open Chrome and visit:
- **http://127.0.0.1:8000/docs**

## 🎯 Quick Test

Before starting the server, test if Python can import the app:

```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python -c "from app.main import app; print('OK')"
```

If this shows "OK", the server should start fine.

If you see errors, install missing packages:
```cmd
pip install -r ../requirements.txt
```

## ✅ Success Indicators

1. Command Prompt shows "Application startup complete"
2. Chrome loads http://127.0.0.1:8000/docs
3. You see Swagger UI with API endpoints

## 🛑 To Stop Server

Press `CTRL+C` in the Command Prompt window

---

**IMPORTANT**: Use Command Prompt (cmd), NOT PowerShell, so you can see all error messages clearly!
