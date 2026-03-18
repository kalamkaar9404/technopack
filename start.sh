#!/bin/bash

# PINNs-UPC Calibration System - Full Stack Startup Script

echo "======================================"
echo "  PINNs-UPC Calibration System"
echo "  Starting Full Stack Application"
echo "======================================"

# Check if Python backend dependencies are installed
echo ""
echo "Checking Python dependencies..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Check if Node.js frontend dependencies are installed
echo ""
echo "Checking Node.js dependencies..."
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start Python backend
echo ""
echo "Starting Python backend on http://localhost:8000..."
python api/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Next.js frontend
echo ""
echo "Starting Next.js frontend on http://localhost:3000..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "======================================"
echo "  Application Started Successfully!"
echo "======================================"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
