# 🔄 Recreate Virtual Environment with Python 3.11

## Steps to Fix

### 1. Delete Old Virtual Environment
```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API
rmdir /s .venv
```

When prompted, type `Y` and press Enter.

### 2. Create New Virtual Environment with Python 3.11
```cmd
python3.11 -m venv .venv
```

Or if that doesn't work:
```cmd
py -3.11 -m venv .venv
```

### 3. Activate Virtual Environment
```cmd
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 5. Create Tables in Database

First, make sure you created the tables in pgAdmin (see create_raja_database.sql).

Or run:
```cmd
cd backend
python create_raja_tables_direct.py
```

### 6. Start Server
```cmd
cd backend
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Application startup complete.
```

### 7. Test in Chrome
Visit: **http://127.0.0.1:8000/docs**

Login: admin / Admin123!

## ✅ Success!

Your server should now run without errors! 🚀
