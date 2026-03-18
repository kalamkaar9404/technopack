@echo off
REM PINNs-UPC Calibration System - Full Stack Startup Script (Windows)

echo ======================================
echo   PINNs-UPC Calibration System
echo   Starting Full Stack Application
echo ======================================

REM Check if Python backend dependencies are installed
echo.
echo Checking Python dependencies...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing Python dependencies...
    pip install -r requirements.txt
)

REM Check if Node.js frontend dependencies are installed
echo.
echo Checking Node.js dependencies...
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

REM Start Python backend
echo.
echo Starting Python backend on http://localhost:8000...
start "Backend API" python api/main.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start Next.js frontend
echo.
echo Starting Next.js frontend on http://localhost:3000...
start "Frontend" npm run dev

echo.
echo ======================================
echo   Application Started Successfully!
echo ======================================
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers
echo.

pause
