@echo off
REM ===================================================================
REM Quick Start Script for Chemical Equipment Visualizer
REM Starts all three components in separate windows
REM ===================================================================

echo Starting Chemical Equipment Visualizer...
echo.

REM Start Backend in new window
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"
timeout /t 3 /nobreak >nul

REM Start Frontend in new window
echo Starting Web Frontend...
start "Web Frontend" cmd /k "cd Web-Frontend && npm run dev"
timeout /t 3 /nobreak >nul

REM Start Desktop App in new window
echo Starting Desktop Application...
start "Desktop App" cmd /k "cd Desktop-App && python main.py"

echo.
echo ============================================
echo All components started!
echo ============================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Desktop:  PyQt5 Window
echo.
echo Login: admin / admin123
echo.
echo Close any window to stop that component
echo.
