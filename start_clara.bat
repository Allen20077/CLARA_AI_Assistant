@echo off

title CLARA AI

echo ==========================================
echo             CLARA AI
echo ==========================================
echo.

echo Starting Clara Brain...
start "CLARA BACKEND" cmd /k "cd /d D:\Internship projects\CLARA\backend && python -m uvicorn main:app --reload"

timeout /t 4 /nobreak >nul

echo Starting Clara Interface...
start "CLARA FRONTEND" cmd /k "cd /d D:\Internship projects\CLARA\frontend && python -m http.server 5500"

timeout /t 3 /nobreak >nul

echo Opening Clara...
start "" "http://127.0.0.1:5500"

echo.
echo ==========================================
echo          CLARA IS RUNNING
echo ==========================================
echo.
echo Brain    : http://127.0.0.1:8000
echo Frontend : http://127.0.0.1:5500
echo.

exit