#!/bin/bash
# ===================================================================
# Quick Setup Script for Chemical Equipment Visualizer
# Linux/macOS Shell Script
# ===================================================================

set -e  # Exit on error

echo ""
echo "============================================"
echo " Chemical Equipment Visualizer - Setup"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi
python3 --version
echo ""

# Check Node.js
echo "[2/4] Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
node --version
echo ""

# Setup Backend
echo "[3/4] Setting up Django Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing backend dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Creating test users..."
python create_desktop_users.py

cd ..
echo -e "${GREEN}Backend setup complete!${NC}"
echo ""

# Setup Frontend
echo "[4/4] Setting up Next.js Frontend..."
cd Web-Frontend

if [ ! -f ".env.local" ]; then
    echo "Creating environment file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi

echo "Installing frontend dependencies..."
if command -v pnpm &> /dev/null; then
    pnpm install -s
else
    npm install -s
fi

cd ..
echo -e "${GREEN}Frontend setup complete!${NC}"
echo ""

# Setup Desktop App
echo "[Bonus] Setting up Desktop Application..."
cd Desktop-App
echo "Installing desktop dependencies..."
pip install -r requirements.txt -q
cd ..
echo -e "${GREEN}Desktop app setup complete!${NC}"
echo ""

echo "============================================"
echo -e " ${GREEN}Setup Complete! 🎉${NC}"
echo "============================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "2. Frontend: cd Web-Frontend && npm run dev"
echo "3. Desktop:  cd Desktop-App && python main.py"
echo ""
echo "Default login: admin / admin123"
echo ""
