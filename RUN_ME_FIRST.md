# 🚀 Run Your API - Super Simple!

## ✨ I've Created 3 Batch Scripts For You

Just **double-click** these files in order:

### 1️⃣ **setup.bat** - Install Everything
- Installs all Python packages
- Initializes Alembic
- Takes ~2-3 minutes

### 2️⃣ **Edit 2 Files** (One-Time Setup)

After running setup.bat, edit these files:

**File: `backend\alembic.ini`** (Line 63)
```ini
# Comment this line by adding # at the start:
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

**File: `backend\migrations\env.py`** (Add after imports, around line 8)
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import settings
from app.db.session import Base
from app.models.user import User

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

**File: `backend\migrations\env.py`** (Find line ~21, replace with)
```python
target_metadata = Base.metadata
```

### 3️⃣ **setup_database.bat** - Create Tables
- Creates database tables
- Creates test admin user
- Takes ~30 seconds

### 4️⃣ **start_server.bat** - Run the API!
- Starts your FastAPI server
- Opens on http://localhost:8000
- Keep this window open while using the API

## 🌐 Test in Chrome

Once `start_server.bat` is running:

1. Open Chrome
2. Visit: **http://localhost:8000/docs**
3. Test the login endpoint:
   - Username: `admin`
   - Password: `Admin123!`

## 🎯 Using Antigravity Extension

With your server running and Swagger UI open in Chrome:
- You can ask me questions about the API
- I can help you understand the endpoints
- Test and explore the API interactively

## 📝 Quick Reference

**Test User:**
- Username: `admin`
- Password: `Admin123!`

**URLs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API Root: http://localhost:8000/

**Stop Server:**
- Press `CTRL+C` in the command window

## 🔧 If Something Goes Wrong

**"Python not found":**
- Make sure Python is installed
- Try: `python --version`

**"Module not found":**
- Run `setup.bat` again
- Or manually: `pip install -r requirements.txt`

**Database connection error:**
- Make sure PostgreSQL is running
- Check `.env` file has correct password

## ✅ That's It!

Just run the 3 batch files in order, and you're done! 🎉
