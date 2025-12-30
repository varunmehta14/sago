#!/bin/bash

echo "🚀 Starting Sago Pitch Deck Analyzer..."
echo ""

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   cd backend && python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Start backend
echo "📦 Starting FastAPI backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "Backend started (PID: $BACKEND_PID)"
echo ""

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Next.js frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Frontend started (PID: $FRONTEND_PID)"
echo ""
echo "✅ Application is running!"
echo ""
echo "📊 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo 'Stopping servers...' && kill $BACKEND_PID $FRONTEND_PID && exit" INT
wait
