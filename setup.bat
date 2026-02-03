@echo off
REM ===================================================================
REM Quick Setup Script for Chemical Equipment Visualizer
REM Windows Batch Script
REM ===================================================================

echo.
echo ============================================
echo  Chemical Equipment Visualizer - Setup
echo ============================================
echo.

REM Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

REM Check Node.js
echo [2/4] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo.

REM Setup Backend
echo [3/4] Setting up Django Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo Running database migrations...
python manage.py migrate --no-input

echo Creating test users...
python create_desktop_users.py

cd ..
echo Backend setup complete!
echo.

REM Setup Frontend
echo [4/4] Setting up Next.js Frontend...
cd Web-Frontend

if not exist .env.local (
    echo Creating environment file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
)

echo Installing frontend dependencies...
call npm install -q

cd ..
echo Frontend setup complete!
echo.

REM Setup Desktop App
echo [Bonus] Setting up Desktop Application...
cd Desktop-App
echo Installing desktop dependencies...
pip install -r requirements.txt -q
cd ..
echo Desktop app setup complete!
echo.

echo ============================================
echo  Setup Complete! 🎉
echo ============================================
echo.
echo To start the application:
echo.
echo 1. Backend:  cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
echo 2. Frontend: cd Web-Frontend ^&^& npm run dev
echo 3. Desktop:  cd Desktop-App ^&^& python main.py
echo.
echo Default login: admin / admin123
echo.
pause
