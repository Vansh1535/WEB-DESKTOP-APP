@echo off
echo ============================================
echo   Starting Equipment Analytics Desktop
echo ============================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if backend is running
echo Checking backend connection...
python -c "import requests; requests.get('http://localhost:8000', timeout=2)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Cannot connect to backend server at http://localhost:8000
    echo Please ensure the backend server is running first.
    echo.
    echo To start backend:
    echo   1. Open new terminal
    echo   2. Navigate to backend folder
    echo   3. Run: python manage.py runserver
    echo.
    pause
)

REM Run the application
echo.
echo Starting application...
python main.py

REM Deactivate venv on exit
call venv\Scripts\deactivate.bat
