#!/bin/bash
# SmartClean Studio - Startup Script for macOS/Linux

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   SmartClean Studio - Startup         ║"
echo "║   Hybrid Data Cleaning System         ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "✗ Node.js not found. Please install Node.js 16+"
    exit 1
fi

echo "✓ Python and Node.js found"
echo ""

# Start backend
echo "Starting Backend Server..."
cd backend
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Backend dependencies installed"

# Start backend in new terminal tab (macOS) or background (Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && uvicorn app.main:app --reload"'
else
    # Linux
    xterm -e "cd '$(pwd)' && source venv/bin/activate && uvicorn app.main:app --reload" &
fi

echo "✓ Backend started on http://localhost:8000"

sleep 3

# Start frontend
echo ""
echo "Starting Frontend Application..."
cd ../frontend
npm install > /dev/null 2>&1
echo "✓ Frontend dependencies installed"

# Start frontend
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && npm start"'
else
    xterm -e "cd '$(pwd)' && npm start" &
fi

echo "✓ Frontend started on http://localhost:3000"

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   Application Started!                ║"
echo "║                                       ║"
echo "║   Frontend: http://localhost:3000    ║"
echo "║   Backend:  http://localhost:8000    ║"
echo "║   API Docs: http://localhost:8000/docs║
echo "║                                       ║"
echo "║   Press Ctrl+C in each window to stop║"
echo "╚═══════════════════════════════════════╝"
echo ""
