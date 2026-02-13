# ⚡ Quick Start - Run Your API Now!

## 🎯 Simple 3-Step Setup

### Step 1: Open PowerShell as Administrator
1. Press `Win + X`
2. Select "Windows PowerShell (Admin)" or "Terminal (Admin)"
3. Navigate to your project:
```powershell
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API
```

### Step 2: Install Dependencies (Without Virtual Environment)
```powershell
# Install dependencies globally (simpler for now)
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 sqlalchemy==2.0.23 psycopg2-binary==2.9.9 alembic==1.12.1 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-dotenv==1.0.0 pydantic==2.5.0 pydantic-settings==2.1.0 email-validator==2.1.0
```

### Step 3: Set Up Database & Run
```powershell
cd backend

# Initialize Alembic
alembic init migrations
```

**Then edit these 2 files:**

**File 1: `backend/alembic.ini`** (Line 63)
```ini
# Comment this line:
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

**File 2: `backend/migrations/env.py`** (Add after imports, around line 8)
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import settings
from app.db.session import Base
from app.models.user import User

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

**File 2: `backend/migrations/env.py`** (Find line ~21, replace `target_metadata = None` with)
```python
target_metadata = Base.metadata
```

**Continue in PowerShell:**
```powershell
# Create database tables
alembic revision --autogenerate -m "Create users table"
alembic upgrade head

# Create test user
python create_test_user.py

# Start the server!
uvicorn app.main:app --reload
```

## 🌐 Access Your API

Once running, open Chrome and visit:
- **Swagger UI**: http://localhost:8000/docs
- **API Root**: http://localhost:8000/

## 🧪 Test with Chrome Extension

With Antigravity extension installed:
1. Visit http://localhost:8000/docs
2. You can ask me questions about the API directly from the browser!
3. Test the `/api/v1/auth/login` endpoint:
   - Username: `admin`
   - Password: `Admin123!`

## 🔧 If You Get Errors

**"pip not recognized":**
```powershell
python -m pip install <package>
```

**"alembic not recognized":**
```powershell
python -m alembic init migrations
python -m alembic revision --autogenerate -m "Create users table"
python -m alembic upgrade head
```

**"Module not found":**
- Make sure you're in the `backend` directory
- Try: `pip install -r ../requirements.txt`

## ✅ Success Indicators

When everything works, you'll see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then visit http://localhost:8000/docs in Chrome! 🎉
