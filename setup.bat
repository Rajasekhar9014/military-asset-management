@echo off
echo ========================================
echo Military Asset Management System Setup
echo ========================================
echo.

echo Step 1: Installing Python packages...
python -m pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary alembic python-jose[cryptography] passlib[bcrypt] python-dotenv pydantic pydantic-settings email-validator
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Step 2: Initializing Alembic...
cd backend
python -m alembic init migrations
if errorlevel 1 (
    echo ERROR: Failed to initialize Alembic
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\alembic.ini - Comment out line 63
echo 2. Edit backend\migrations\env.py - Add imports (see GETTING_STARTED.md)
echo 3. Run: setup_database.bat
echo.
pause
