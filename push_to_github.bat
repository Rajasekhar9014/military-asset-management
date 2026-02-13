@echo off
echo ========================================
echo Pushing Code to GitHub
echo ========================================
echo.

REM Go to root directory
cd /d C:\Users\Harinathreddy\OneDrive\Desktop\F-API

echo Step 1: Checking git status...
git status

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Committing...
git commit -m "Initial commit - Military Asset Management System"

echo.
echo Step 4: Checking if remote exists...
git remote -v

echo.
echo Step 5: Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Done!
echo ========================================
pause
