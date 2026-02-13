@echo off
echo ========================================
echo Creating Database Tables - Simple Method
echo ========================================
echo.

cd backend

echo Creating tables in database: kristalball
python create_tables.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create tables
    echo.
    echo Troubleshooting:
    echo 1. Make sure PostgreSQL is running
    echo 2. Check .env file has correct database credentials
    echo 3. Database: postgresql://postgres:1234@localhost:5432/kristalball
    echo.
    pause
    exit /b 1
)

echo.
echo Creating test admin user...
python create_test_user.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create test user
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Database is ready!
echo ========================================
echo.
echo Test user created:
echo   Username: admin
echo   Password: Admin123!
echo.
echo Next: Run start_server.bat to start the API
echo.
pause
