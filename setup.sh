#!/bin/bash

echo "🔧 Setting up Sago Pitch Deck Analyzer..."
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python 3.11 virtual environment..."
    python3.11 -m venv venv
fi

# Activate and install dependencies
source venv/bin/activate
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your GOOGLE_API_KEY"
fi

cd ..

# Frontend setup
echo ""
echo "🎨 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

# Check for .env.local file
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local..."
    cp .env.local.example .env.local
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your Google Gemini API key to backend/.env"
echo "   Get one free at: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Run the application:"
echo "   ./run.sh"
echo ""
echo "   Or run manually:"
echo "   Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   Frontend: cd frontend && npm run dev"
echo ""
