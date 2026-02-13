@echo off
echo ========================================
echo Creating Database Tables
echo ========================================
echo.

cd backend

echo Creating migration...
python -m alembic revision --autogenerate -m "Create users table"
if errorlevel 1 (
    echo ERROR: Failed to create migration
    echo Make sure you edited migrations\env.py correctly
    pause
    exit /b 1
)

echo.
echo Applying migration...
python -m alembic upgrade head
if errorlevel 1 (
    echo ERROR: Failed to apply migration
    pause
    exit /b 1
)

echo.
echo Creating test user...
python create_test_user.py
if errorlevel 1 (
    echo ERROR: Failed to create test user
    pause
    exit /b 1
)

echo.
echo ========================================
echo Database Setup Complete!
echo ========================================
echo.
echo Test user created:
echo   Username: admin
echo   Password: Admin123!
echo.
echo Run: start_server.bat to start the API
echo.
pause
