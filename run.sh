#!/bin/bash

# PlanLLaMA Backend Run Script

echo "🚀 PlanLLaMA Backend Setup & Run"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ ! -f "venv/installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
else
    echo "✅ Dependencies already installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Check if database exists
if [ ! -f "planllama.db" ]; then
    echo "🗄️  Initializing database with seed data..."
    python init_db.py --seed
else
    echo "✅ Database already exists"
fi

echo ""
echo "🎉 Setup complete! Starting server..."
echo "📍 API will be available at: http://localhost:5000"
echo "📖 API documentation: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py
