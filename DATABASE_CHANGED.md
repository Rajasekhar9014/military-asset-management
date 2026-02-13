# ✅ Database Changed to `raja`!

## 🎯 What I Did

1. ✅ Updated `.env` file to use database: **`raja`**
2. ✅ Created tables in `raja` database
3. ✅ Created admin test user
4. ✅ Created SQL script for manual setup if needed

## 🔍 Verify in pgAdmin

1. Open pgAdmin
2. Navigate to: **Servers → PostgreSQL → Databases → raja → Schemas → public → Tables**
3. Right-click **Tables** → **Refresh**
4. You should see: **`users`** table

## 🚀 Restart Your Server

The server is currently running with the old database. You need to restart it:

### Stop Current Server:
- Find the Command Prompt window running the server
- Press **CTRL+C**

### Start with New Database:
```cmd
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
python -m uvicorn app.main:app --reload
```

**Or double-click:** `start_server.bat`

## 🧪 Test

Once server restarts, visit: **http://127.0.0.1:8000/docs**

Login with:
- Username: `admin`
- Password: `Admin123!`

## 📋 Database Configuration

**New settings in `.env`:**
```env
DATABASE_URL=postgresql://postgres:1234@localhost:5432/raja
DATABASE_NAME=raja
```

## ✨ You're All Set!

Your application is now configured to use the **`raja`** database!

Just restart the server and test it! 🚀
