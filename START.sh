#!/bin/bash

# Quick Start Script for Chemical Equipment Visualizer
# This script starts both backend and frontend servers

echo "========================================"
echo "Chemical Equipment Visualizer"
echo "Quick Start Script"
echo "========================================"
echo ""

# Check if backend virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "[ERROR] Backend not set up yet!"
    echo "Please run: cd backend && ./setup.sh"
    echo ""
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "Web-Frontend/node_modules" ]; then
    echo "[ERROR] Frontend not set up yet!"
    echo "Please run: cd Web-Frontend && pnpm install"
    echo ""
    exit 1
fi

echo "[1/3] Starting Django Backend..."
echo ""
cd backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!
cd ..

# Wait a few seconds for backend to start
sleep 5

echo "[2/3] Starting Next.js Frontend..."
echo ""
cd Web-Frontend
pnpm dev &
FRONTEND_PID=$!
cd ..

echo "[3/3] Waiting for servers to start..."
sleep 5

echo ""
echo "========================================"
echo "Both servers are running!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Login credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers stopped."
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup INT TERM

# Keep script running
wait
