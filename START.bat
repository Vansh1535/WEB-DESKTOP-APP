@echo off
REM Quick Start Script for Chemical Equipment Visualizer
REM This script starts both backend and frontend servers

echo ========================================
echo Chemical Equipment Visualizer
echo Quick Start Script
echo ========================================
echo.

REM Check if backend virtual environment exists
if not exist "backend\venv\" (
    echo [ERROR] Backend not set up yet!
    echo Please run: cd backend ^&^& setup.bat
    echo.
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "Web-Frontend\node_modules\" (
    echo [ERROR] Frontend not set up yet!
    echo Please run: cd Web-Frontend ^&^& pnpm install
    echo.
    pause
    exit /b 1
)

echo [1/3] Starting Django Backend...
echo.
start "Django Backend" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"

REM Wait a few seconds for backend to start
timeout /t 5 /nobreak > nul

echo [2/3] Starting Next.js Frontend...
echo.
start "Next.js Frontend" cmd /k "cd Web-Frontend && pnpm dev"

echo [3/3] Opening browser...
timeout /t 5 /nobreak > nul
start http://localhost:3000

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C in each window to stop servers
echo ========================================
echo.
pause
