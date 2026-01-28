@echo off
REM SmartClean Studio - Startup Script for Windows

echo.
echo ╔═══════════════════════════════════════╗
echo ║   SmartClean Studio - Startup         ║
echo ║   Hybrid Data Cleaning System         ║
echo ╚═══════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.11+
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js not found. Please install Node.js 16+
    exit /b 1
)

echo ✓ Python and Node.js found
echo.

REM Start backend
echo Starting Backend Server...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1
echo ✓ Backend dependencies installed
start cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload"
echo ✓ Backend started on http://localhost:8000

timeout /t 3 /nobreak

REM Start frontend
echo.
echo Starting Frontend Application...
cd ..\frontend
call npm install >nul 2>&1
echo ✓ Frontend dependencies installed
start cmd /k "cd frontend && npm start"
echo ✓ Frontend started on http://localhost:3000

echo.
echo ╔═══════════════════════════════════════╗
echo ║   Application Started!                ║
echo ║                                       ║
echo ║   Frontend: http://localhost:3000    ║
echo ║   Backend:  http://localhost:8000    ║
echo ║   API Docs: http://localhost:8000/docs║
echo ║                                       ║
echo ║   Press Ctrl+C in each window to stop║
echo ╚═══════════════════════════════════════╝
echo.

pause
