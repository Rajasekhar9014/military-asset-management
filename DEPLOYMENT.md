# 🚀 Military Asset Management System - Deployment Guide

Complete step-by-step guide to deploy this application on any fresh system.

## 📋 Quick Start

1. **Install Prerequisites**
   - Python 3.9+
   - PostgreSQL 14+

2. **Setup Project**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Configure Database**
   - Create database: `kristalball`
   - Copy `.env.example` to `.env`
   - Update database credentials in `.env`

4. **Create Tables**
   ```bash
   cd backend
   python create_tables.py
   python create_test_user.py
   ```

5. **Start Server**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

6. **Test**
   - Visit: http://localhost:8000/docs
   - Login: admin / Admin123!

## 📚 Full Documentation

See **[deployment_guide.md](file:///C:/Users/Harinathreddy/.gemini/antigravity/brain/323abdd8-077f-44d1-9356-5515a690a1bb/deployment_guide.md)** for complete instructions including:
- Detailed prerequisites for Windows/macOS/Linux
- Step-by-step installation
- Database setup options
- Configuration guide
- Troubleshooting
- Verification steps

## 🎯 Test Credentials

- **Username**: admin
- **Password**: Admin123!

## 📁 Project Structure

```
F-API/
├── backend/
│   ├── app/
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── api/         # API endpoints
│   │   ├── middleware/  # Auth middleware
│   │   ├── utils/       # Utilities
│   │   └── db/          # Database config
│   ├── create_tables.py
│   ├── create_test_user.py
│   └── verify_database.py
├── .env                 # Configuration
├── requirements.txt     # Dependencies
└── deployment_guide.md  # Full guide
```

## ✅ Verification

Run to verify everything is working:
```bash
cd backend
python verify_database.py
```

## 🚀 You're Ready!

For detailed instructions, see the full deployment guide.
