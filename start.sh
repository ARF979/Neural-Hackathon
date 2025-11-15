#!/bin/bash

# AI Social Media Content Generator - Startup Script
# This script starts both backend and frontend servers

echo "════════════════════════════════════════════════════════════"
echo "   🚀 AI SOCIAL MEDIA CONTENT GENERATOR"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}📁 Project Directory: ${NC}$SCRIPT_DIR"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi
echo "✅ Python 3 found"

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found"

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi
echo "✅ npm found"

echo ""

# Install backend dependencies if needed
echo -e "${YELLOW}📦 Setting up backend...${NC}"
cd "$SCRIPT_DIR/backend"

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

if [ ! -f "venv/installed" ]; then
    echo "Installing Python dependencies (this may take a few minutes)..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/installed
    echo "✅ Backend dependencies installed"
else
    echo "✅ Backend dependencies already installed"
fi

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo ""

# Install frontend dependencies if needed
echo -e "${YELLOW}📦 Setting up frontend...${NC}"
cd "$SCRIPT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies (this may take a few minutes)..."
    npm install
    echo "✅ Frontend dependencies installed"
else
    echo "✅ Frontend dependencies already installed"
fi

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Starting servers..."
echo ""

# Start backend in background
echo -e "${BLUE}🚀 Starting Backend API on http://localhost:8000${NC}"
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait a bit for backend to start
sleep 3

# Start frontend
echo ""
echo -e "${BLUE}🎨 Starting Frontend on http://localhost:3000${NC}"
cd "$SCRIPT_DIR/frontend"
npm start &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}🎉 Application Started!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📱 Frontend:  http://localhost:3000"
echo "📡 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "⚠️  Note: First content generation will take 5-10 minutes"
echo "    as AI models need to be downloaded (~10GB)"
echo ""
echo "To stop the servers, press Ctrl+C or run:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Backend logs: tail -f backend/backend.log"
echo ""
echo "════════════════════════════════════════════════════════════"

# Wait for user interrupt
wait
