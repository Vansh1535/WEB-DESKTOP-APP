@echo off
echo ========================================
echo Chemical Equipment API - Quick Setup
echo ========================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.10+ is installed
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Running migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo [5/6] Creating superuser...
echo Please enter credentials for the admin user:
python manage.py createsuperuser

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/admin/
echo.
pause
