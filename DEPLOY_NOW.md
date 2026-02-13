# 🚀 DEPLOYMENT GUIDE - Step by Step

**Time:** 22:22 PM  
**Goal:** Deploy backend to Render, frontend to Vercel

---

## 📋 STEP 1: Push Code to GitHub (10 minutes)

### 1.1 Initialize Git Repository

Open a **NEW terminal** and run:

```bash
cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API
git init
```

### 1.2 Create .gitignore (Root)

Create a file called `.gitignore` in the root folder with:

```
# Virtual Environment
.venv/
venv/

# Environment files
.env
*.env.local

# Database
*.db
*.sqlite3

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc

# Node
node_modules/
dist/
build/

# Logs
*.log
```

### 1.3 Add All Files

```bash
git add .
```

### 1.4 Commit

```bash
git commit -m "Initial commit - Military Asset Management System"
```

### 1.5 Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon (top right)
3. Click **"New repository"**
4. Repository name: `military-asset-management` (or any name you like)
5. Description: "Military Asset Management System - Assignment Project"
6. Keep it **Public** (or Private if you prefer)
7. **DO NOT** check "Initialize with README"
8. Click **"Create repository"**

### 1.6 Push to GitHub

GitHub will show you commands. Run these:

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

**Replace:**
- `YOUR-USERNAME` with your GitHub username
- `YOUR-REPO-NAME` with your repository name

✅ **Your code is now on GitHub!**

---

## 🗄️ STEP 2: Deploy Backend to Render (30 minutes)

### 2.1 Create Render Account

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest)
4. Authorize Render to access your GitHub

### 2.2 Create PostgreSQL Database

1. In Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Fill in:
   - **Name:** `military-assets-db`
   - **Database:** `military_assets`
   - **User:** (auto-filled)
   - **Region:** Singapore (closest to you)
   - **PostgreSQL Version:** 15 (default)
   - **Plan:** **Free**
4. Click **"Create Database"**
5. Wait 1-2 minutes for database to be created

### 2.3 Copy Database URL

1. Once created, you'll see the database dashboard
2. Scroll down to **"Connections"**
3. Find **"Internal Database URL"**
4. Click the **copy icon** to copy it
5. **SAVE THIS URL** - you'll need it in a moment!

**Format:** `postgresql://user:password@hostname/database`

### 2.4 Create Web Service

1. Click **"New +"** again
2. Select **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Click **"Next"**
5. Find your repository in the list and click **"Connect"**

### 2.5 Configure Web Service

Fill in these settings:

**Basic Settings:**
- **Name:** `military-assets-api` (or any name)
- **Region:** Singapore (same as database)
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Runtime:** **Python 3**

**Build Settings:**
- **Build Command:**
  ```
  pip install -r backend/requirements.txt
  ```
- **Start Command:**
  ```
  cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- **Plan:** **Free**

### 2.6 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables one by one:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Paste your Internal Database URL from step 2.3 |
| `SECRET_KEY` | `military-secret-key-2026-change-in-production` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `APP_NAME` | `Military Asset Management System` |
| `APP_VERSION` | `1.0.0` |
| `DEBUG` | `False` |
| `ALLOWED_ORIGINS` | `*` |

### 2.7 Deploy!

1. Click **"Create Web Service"**
2. Render will start building your app
3. Watch the logs - you'll see:
   - Installing dependencies
   - Starting the server
4. Wait 5-10 minutes for first deployment

### 2.8 Check Deployment Status

- **Building:** Yellow dot - in progress
- **Live:** Green dot - success! ✅
- **Failed:** Red dot - check logs

### 2.9 Get Your Backend URL

Once live, you'll see:
```
https://military-assets-api.onrender.com
```

**Save this URL!** You'll need it for frontend.

### 2.10 Initialize Database

We need to create tables and admin user. Two options:

**Option A: Add to main.py (Easier)**

Add this to `backend/app/main.py` (after imports):

```python
from app.db.session import engine, Base
from app.models import user, asset_category, unit, asset, purchase, transfer, assignment

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    
    # Create admin user if not exists
    from app.db.session import SessionLocal
    from app.utils.security import hash_password
    db = SessionLocal()
    admin = db.query(user.User).filter(user.User.username == "admin").first()
    if not admin:
        admin = user.User(
            username="admin",
            email="admin@military.gov",
            hashed_password=hash_password("Admin123!"),
            full_name="System Administrator",
            role="admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
    db.close()
```

Then push to GitHub and Render will auto-redeploy.

**Option B: Use Render Shell**

1. Go to database dashboard
2. Click **"Connect"** → Copy PSQL command
3. Run in your local terminal
4. Run your `create_all_tables.sql` script

### 2.11 Test Backend

1. Visit: `https://your-app.onrender.com/docs`
2. You should see Swagger UI!
3. Try the login endpoint
4. Should work! ✅

---

## 🎨 STEP 3: Deploy Frontend to Vercel (20 minutes)

### 3.1 Update Frontend .env

Edit `frontend/.env`:

```
VITE_API_URL=https://your-backend.onrender.com
```

**Replace with your actual Render URL!**

### 3.2 Test Build Locally

```bash
cd frontend
npm run build
```

Should complete without errors.

### 3.3 Commit Changes

```bash
cd ..
git add .
git commit -m "Update API URL for production"
git push
```

### 3.4 Create Vercel Account

1. Go to https://vercel.com
2. Click **"Sign Up"**
3. Sign up with **GitHub**
4. Authorize Vercel

### 3.5 Import Project

1. Click **"Add New..."** → **"Project"**
2. Find your repository
3. Click **"Import"**

### 3.6 Configure Project

**Framework Preset:** Vite (auto-detected)

**Root Directory:** `frontend`

**Build Settings:**
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

**Environment Variables:**
Click **"Add"** and add:
- **Name:** `VITE_API_URL`
- **Value:** `https://your-backend.onrender.com`

### 3.7 Deploy!

1. Click **"Deploy"**
2. Wait 2-5 minutes
3. You'll get a URL like: `https://military-assets.vercel.app`

### 3.8 Update Backend CORS

1. Go back to Render
2. Find your backend service
3. Go to **"Environment"**
4. Update `ALLOWED_ORIGINS`:
   ```
   https://your-app.vercel.app,http://localhost:5173
   ```
5. Save (will auto-redeploy)

### 3.9 Test Frontend

1. Visit your Vercel URL
2. Login with: `admin` / `Admin123!`
3. Should work! ✅

---

## ✅ SUCCESS CHECKLIST

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Database URL copied
- [ ] Backend deployed to Render
- [ ] Environment variables set
- [ ] Database initialized
- [ ] Backend API docs accessible
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Frontend environment variable set
- [ ] Backend CORS updated
- [ ] Can login on live site
- [ ] Dashboard shows metrics
- [ ] Can create purchases
- [ ] Can create transfers

---

## 🎯 YOUR DEPLOYMENT URLS

**Backend API:** `_______________________`

**Frontend App:** `_______________________`

**Demo Credentials:**
- Username: `admin`
- Password: `Admin123!`

---

## 🐛 Troubleshooting

**Build fails on Render:**
- Check build logs
- Verify `requirements.txt` is correct
- Check Python version compatibility

**Frontend blank page:**
- Check browser console (F12)
- Verify `VITE_API_URL` is set correctly
- Check backend is running

**CORS errors:**
- Add Vercel URL to `ALLOWED_ORIGINS`
- Redeploy backend

**Login fails:**
- Check database was initialized
- Verify admin user was created
- Check backend logs

---

**Let's do this! Start with Step 1!** 🚀
