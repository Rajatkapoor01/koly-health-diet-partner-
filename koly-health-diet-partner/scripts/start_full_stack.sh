#!/bin/bash

# KOYL AI Full Stack Startup Script
echo "🚀 Starting KOYL AI Full Stack Application..."

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if required ports are available
echo "🔍 Checking port availability..."
if ! check_port 3000; then
    echo "❌ Frontend port 3000 is in use. Please stop the process or use a different port."
    exit 1
fi

if ! check_port 5000; then
    echo "❌ Backend port 5000 is in use. Please stop the process or use a different port."
    exit 1
fi

# Start backend in background
echo "🐍 Starting Flask backend..."
cd scripts/backend
source ../../koyl_ai_env/bin/activate
python run_backend.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 10

# Check if backend is running
if ! curl -s http://localhost:5000/health > /dev/null; then
    echo "❌ Backend failed to start properly"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend is running on http://localhost:5000"

# Start frontend
echo "⚛️  Starting Next.js frontend..."
cd ../..
export FLASK_BACKEND_URL=http://localhost:5000
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 5

echo ""
echo "🎉 KOYL AI is now running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "🏥 Health Check: http://localhost:5000/health"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down KOYL AI..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Shutdown complete"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
