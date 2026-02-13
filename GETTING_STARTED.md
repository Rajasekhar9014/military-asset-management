# 🎉 Complete Setup Instructions

## ✅ What You Have Now

Your Military Asset Management System includes:

1. **✅ User Model** - Complete database model
2. **✅ Authentication** - Login with JWT tokens
3. **✅ Auth Middleware** - Protect routes with `Depends(get_current_user)`
4. **✅ User Management** - Full CRUD operations
5. **✅ Security** - Password hashing, token verification
6. **✅ Validation** - Pydantic schemas with strong validation

## 🚀 Quick Setup (Copy & Paste)

### Step 1: Install Dependencies

```powershell
# Open PowerShell in F-API directory
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Initialize Alembic

```powershell
cd backend
alembic init migrations
```

### Step 3: Configure Alembic

**Edit `backend/alembic.ini`** - Line 63, comment out:
```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Edit `backend/migrations/env.py`** - Add after the imports (around line 8):
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import settings
from app.db.session import Base
from app.models.user import User

# Set database URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

**Edit `backend/migrations/env.py`** - Find `target_metadata = None` (around line 21) and replace with:
```python
target_metadata = Base.metadata
```

### Step 4: Create Database Tables

```powershell
# Still in backend directory
alembic revision --autogenerate -m "Create users table"
alembic upgrade head
```

### Step 5: Create Test User

```powershell
python create_test_user.py
```

**Test User Credentials:**
- Username: `admin`
- Password: `Admin123!`

### Step 6: Start the Server

```powershell
uvicorn app.main:app --reload
```

## 🎯 Test Your API

### Open Swagger UI
Visit: **http://localhost:8000/docs**

### Test Authentication Flow

1. **Login** - `POST /api/v1/auth/login`
   ```json
   {
     "username": "admin",
     "password": "Admin123!"
   }
   ```
   Copy the `access_token` from response

2. **Authorize** - Click the 🔒 "Authorize" button (top right)
   - Enter: `Bearer <your_access_token>`
   - Click "Authorize"

3. **Get Current User** - `GET /api/v1/users/me`
   - Click "Try it out"
   - Click "Execute"
   - You should see your user info! 🎉

4. **List Users** - `GET /api/v1/users/`
   - Should return list of users

5. **Create User** - `POST /api/v1/users/`
   ```json
   {
     "username": "john_doe",
     "email": "john@military.mil",
     "password": "SecurePass123",
     "full_name": "John Doe",
     "role_id": 2
   }
   ```

## 📋 Available Endpoints

### Public Endpoints (No Auth Required)
- `GET /` - API info
- `GET /health` - Health check
- `POST /api/v1/auth/login` - Login

### Protected Endpoints (Auth Required)
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users/` - Create new user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `POST /api/v1/users/change-password` - Change password

## 🔧 Troubleshooting

**PowerShell script execution blocked:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alembic can't find models:**
- Make sure you added the imports in `migrations/env.py`
- Verify `target_metadata = Base.metadata` is set

**Database connection error:**
- Check PostgreSQL is running
- Verify `.env` has correct credentials
- Connection string: `postgresql://postgres:1234@localhost:5432/kristalball`

**Import errors:**
- Make sure you're in the `backend` directory
- Virtual environment is activated

## 📁 Project Structure

```
F-API/
├── backend/
│   ├── app/
│   │   ├── main.py              ← FastAPI app
│   │   ├── config.py            ← Settings
│   │   ├── models/
│   │   │   └── user.py          ← User model
│   │   ├── schemas/
│   │   │   ├── auth.py          ← Auth schemas
│   │   │   └── user.py          ← User schemas
│   │   ├── api/
│   │   │   ├── auth.py          ← Login endpoint
│   │   │   └── users.py         ← User CRUD endpoints
│   │   ├── middleware/
│   │   │   └── auth.py          ← JWT middleware
│   │   ├── utils/
│   │   │   └── security.py      ← Password & JWT
│   │   └── db/
│   │       └── session.py       ← Database
│   ├── migrations/              ← Alembic migrations
│   └── create_test_user.py      ← Test user script
├── venv/
├── .env
└── requirements.txt
```

## 🎓 Next Steps

Now that you have authentication working, you can:

1. **Add More Models** - Asset, Transaction, Unit, etc.
   - See [model_implementations.md](file:///C:/Users/Harinathreddy/.gemini/antigravity/brain/323abdd8-077f-44d1-9356-5515a690a1bb/model_implementations.md)

2. **Add RBAC** - Role-based permissions
   - See [rbac_implementation_guide.md](file:///C:/Users/Harinathreddy/.gemini/antigravity/brain/323abdd8-077f-44d1-9356-5515a690a1bb/rbac_implementation_guide.md)

3. **Add Asset Management** - Core business logic
   - See [api_design_guide.md](file:///C:/Users/Harinathreddy/.gemini/antigravity/brain/323abdd8-077f-44d1-9356-5515a690a1bb/api_design_guide.md)

## 📚 Documentation

All comprehensive guides are available:
- [README.md](file:///C:/Users/Harinathreddy/.gemini/antigravity/brain/323abdd8-077f-44d1-9356-5515a690a1bb/README.md) - Master index
- [quick_start_guide.md](file:///C:/Users/Harinathreddy/.gemini/antigravity/brain/323abdd8-077f-44d1-9356-5515a690a1bb/quick_start_guide.md) - Detailed walkthrough

## ✨ You're All Set!

Follow the 6 steps above and you'll have a fully functional API with authentication in minutes! 🚀
