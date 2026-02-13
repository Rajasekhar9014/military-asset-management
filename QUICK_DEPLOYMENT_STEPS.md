# 🚀 Quick Deployment Steps

**Time Required:** 2-3 hours  
**Current Time:** 01:20 AM

---

## ✅ Pre-Deployment Checklist

### Local Testing
- [ ] Backend running on http://127.0.0.1:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can login with admin/Admin123!
- [ ] Dashboard shows metrics
- [ ] Can create purchases
- [ ] Can create transfers

---

## 🎯 Step 1: Deploy Backend to Render (1 hour)

### A. Create Render Account
1. Go to https://render.com
2. Sign up with GitHub or email
3. Verify your email

### B. Create PostgreSQL Database
1. Dashboard → **New +** → **PostgreSQL**
2. Settings:
   - Name: `military-assets-db`
   - Database: `military_assets`
   - Region: Singapore (closest to you)
   - Plan: **Free**
3. Click **Create Database**
4. ⚠️ **COPY THE INTERNAL DATABASE URL** (you'll need this!)

### C. Create Web Service
1. Dashboard → **New +** → **Web Service**
2. Choose: **Build and deploy from a Git repository**
3. Connect your GitHub account (or use public repo)
4. If no repo, choose **Deploy from Git URL** and paste your repo URL

### D. Configure Web Service
**Basic Settings:**
- Name: `military-assets-api`
- Region: Same as database (Singapore)
- Branch: `main`
- Root Directory: Leave blank
- Runtime: **Python 3**

**Build Settings:**
- Build Command: `pip install -r backend/requirements.txt`
- Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:** Free

### E. Environment Variables
Click **Advanced** → Add these variables:

```
DATABASE_URL = <paste your Internal Database URL>
SECRET_KEY = military-secret-key-2026-change-in-production
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
APP_NAME = Military Asset Management System
APP_VERSION = 1.0.0
DEBUG = False
ALLOWED_ORIGINS = *
```

⚠️ Replace `<paste your Internal Database URL>` with actual URL from step B!

### F. Deploy
1. Click **Create Web Service**
2. Wait for build (5-10 minutes)
3. Check logs for errors
4. Once live, you'll get a URL like: `https://military-assets-api.onrender.com`

### G. Initialize Database
**Option 1: Using Render Shell**
1. Go to your database dashboard
2. Click **Connect** → **PSQL Command**
3. Copy and run in your local terminal
4. Once connected, paste contents of `create_all_tables.sql`

**Option 2: Add to main.py (Easier)**
Add this to `backend/app/main.py`:
```python
from app.db.session import engine, Base

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
```
Then redeploy.

### H. Test Backend
1. Visit: `https://your-app.onrender.com/docs`
2. Try login endpoint with admin/Admin123!
3. ✅ If you get a token, backend is working!

---

## 🎯 Step 2: Deploy Frontend to Vercel (1 hour)

### A. Update Frontend Config
1. Edit `frontend/.env`:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```
   (Use your actual Render URL from Step 1!)

2. Test build locally:
   ```bash
   cd frontend
   npm run build
   ```
   Should complete without errors.

### B. Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel

### C. Deploy Frontend
1. Dashboard → **Add New...** → **Project**
2. **Import Git Repository** → Select your repo
3. Configure:
   - Framework Preset: **Vite**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

### D. Add Environment Variable
1. Click **Environment Variables**
2. Add:
   - Name: `VITE_API_URL`
   - Value: `https://your-backend.onrender.com`
3. Select: Production, Preview, Development

### E. Deploy
1. Click **Deploy**
2. Wait for build (2-5 minutes)
3. You'll get a URL like: `https://military-assets.vercel.app`

### F. Update Backend CORS
1. Go back to Render dashboard
2. Find your backend service
3. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:5173
   ```
4. Save (auto-redeploys)

### G. Test Frontend
1. Visit your Vercel URL
2. Login with admin/Admin123!
3. Check dashboard loads
4. Try creating a purchase
5. ✅ If everything works, you're done!

---

## 🎯 Step 3: Create Documentation (30 min)

### A. Convert to PDF
**Option 1: Online (Easiest)**
1. Go to https://www.markdowntopdf.com
2. Upload `ASSIGNMENT_DOCUMENTATION.md`
3. Download PDF

**Option 2: VS Code**
1. Install "Markdown PDF" extension
2. Open `ASSIGNMENT_DOCUMENTATION.md`
3. Right-click → "Markdown PDF: Export (pdf)"

### B. Add Your Details
Edit the PDF or markdown to add:
- Your name
- Student ID
- Course name
- Instructor name
- Deployed URLs

### C. Take Screenshots
1. Login page
2. Dashboard with metrics
3. Purchases page
4. Transfers page
5. Swagger UI at `/docs`

---

## 🎯 Step 4: Record Video (45 min)

### A. Setup
**Recommended Tool:** Loom.com (free, easy)
1. Go to https://loom.com
2. Sign up free
3. Install Chrome extension or desktop app

**Alternative:** OBS Studio (free, more control)

### B. Recording Script (3-5 minutes)
Follow the script in `SUBMISSION_CHECKLIST.md` section "Video Recording Steps"

**Quick Outline:**
1. Introduction (30 sec)
2. Architecture overview (1 min)
3. Database design (1 min)
4. Live demo (2-3 min):
   - Login
   - Dashboard + filters
   - Create purchase
   - Create transfer
   - Show API docs
5. Conclusion (30 sec)

### C. Upload
- Upload to YouTube (unlisted)
- Or upload to Google Drive (share link)
- Test the link works

---

## 🎯 Step 5: Create Code Archive (30 min)

### A. Prepare Structure
```
YourName_MilitaryAssetManagement/
├── backend/
├── frontend/
├── database/
│   └── create_all_tables.sql
├── documentation/
│   └── ASSIGNMENT_DOCUMENTATION.pdf
└── README.md
```

### B. Clean Up
Remove these before zipping:
- `node_modules/`
- `.venv/`
- `dist/`
- `__pycache__/`
- `.env` files (keep .env.example)

### C. Create .env.example Files
**backend/.env.example:**
```
DATABASE_URL=postgresql://user:password@localhost/database
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**frontend/.env.example:**
```
VITE_API_URL=http://127.0.0.1:8000
```

### D. Create Root README
```markdown
# Military Asset Management System

## Live Demo
- Frontend: https://your-app.vercel.app
- Backend: https://your-api.onrender.com/docs

## Demo Credentials
- Username: admin
- Password: Admin123!

## Quick Start
See documentation/ASSIGNMENT_DOCUMENTATION.pdf
```

### E. Zip It
- Select all files
- Right-click → Send to → Compressed (zipped) folder
- Name: `YourName_MilitaryAssetManagement.zip`

---

## 🎯 Step 6: Submit (15 min)

### Email Template
**Subject:** Assignment Submission - Military Asset Management System - [Your Name]

**Body:**
```
Dear [Instructor],

Please find my assignment submission:

📦 Attachments:
1. YourName_MilitaryAssetManagement.zip (code + database)
2. ASSIGNMENT_DOCUMENTATION.pdf

🎥 Video Walkthrough:
[Your YouTube/Drive Link]

🌐 Live Demo:
- Frontend: https://your-app.vercel.app
- Backend API: https://your-api.onrender.com/docs

🔑 Demo Credentials:
- Username: admin
- Password: Admin123!

✅ Features Implemented:
- Dashboard with opening/closing balance
- Net movement with detailed breakdown
- Purchase tracking with filters
- Transfer management with status workflow
- Complete RBAC with JWT
- API logging and audit trail
- PostgreSQL database (8 tables)
- 24 REST API endpoints
- Responsive React frontend
- Production deployment

Thank you!

Best regards,
[Your Name]
[Student ID]
```

---

## ⚡ Quick Troubleshooting

**Backend won't deploy:**
- Check build logs in Render
- Verify DATABASE_URL is correct (use Internal URL)
- Check requirements.txt has all dependencies

**Frontend blank page:**
- Check browser console (F12)
- Verify VITE_API_URL is correct
- Check backend is running

**CORS errors:**
- Add Vercel URL to backend ALLOWED_ORIGINS
- Redeploy backend

**Database empty:**
- Run create_all_tables.sql in Render database
- Or add startup event to create tables

---

## 📞 Support Links

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Loom Help:** https://support.loom.com

---

## ✅ Final Checklist

- [ ] Backend deployed and working
- [ ] Frontend deployed and working
- [ ] Can login on live site
- [ ] Dashboard shows metrics
- [ ] Purchases work
- [ ] Transfers work
- [ ] PDF documentation ready
- [ ] Screenshots added
- [ ] Video recorded and uploaded
- [ ] Code archive created
- [ ] Email drafted
- [ ] Submitted!

---

**You've got this! 🚀**

**Estimated completion: 4:00 AM**  
**Plenty of time before deadline!**
