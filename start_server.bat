@echo off
echo ========================================
echo Starting Military Asset Management API
echo ========================================
echo.

REM Change to backend directory
cd /d "%~dp0backend"

echo Starting server from: %CD%
echo.
echo Server URL: http://127.0.0.1:8000
echo Swagger UI: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

REM Start uvicorn
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
