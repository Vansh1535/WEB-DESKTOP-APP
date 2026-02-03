#!/bin/bash
# ===================================================================
# Quick Start Script for Chemical Equipment Visualizer
# Starts all three components
# ===================================================================

echo "Starting Chemical Equipment Visualizer..."
echo ""

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
    echo "ERROR: Backend not set up. Please run ./setup.sh first"
    exit 1
fi

if [ ! -d "Web-Frontend/node_modules" ]; then
    echo "ERROR: Frontend not set up. Please run ./setup.sh first"
    exit 1
fi

# Start Backend
echo "Starting Backend Server..."
cd backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!
cd ..
sleep 3

# Start Frontend
echo "Starting Web Frontend..."
cd Web-Frontend
if command -v pnpm &> /dev/null; then
    pnpm dev &
else
    npm run dev &
fi
FRONTEND_PID=$!
cd ..
sleep 3

# Start Desktop App (in foreground)
echo "Starting Desktop Application..."
cd Desktop-App
python main.py

# When desktop app closes, kill backend and frontend
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null

echo ""
echo "All components stopped."
