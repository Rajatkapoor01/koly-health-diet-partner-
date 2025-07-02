#!/bin/bash

# KOYL AI Backend Setup Script
echo "🚀 Setting up KOYL AI Backend..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"

# Check if we're in the right directory
if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found in $BACKEND_DIR"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv koyl_ai_env

# Check if virtual environment was created successfully
if [ ! -d "koyl_ai_env" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source koyl_ai_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Change to backend directory
cd "$BACKEND_DIR"

# Make installation script executable and run it
echo "📚 Installing dependencies..."
chmod +x install_dependencies.sh
bash install_dependencies.sh

if [ $? -ne 0 ]; then
    echo "❌ Dependency installation failed"
    exit 1
fi

# Check dependencies
echo "🔍 Checking dependencies..."
python3 check_dependencies.py

if [ $? -ne 0 ]; then
    echo "❌ Dependency check failed"
    exit 1
fi

# Make run script executable
chmod +x run_backend.py

# Go back to project root
cd "$SCRIPT_DIR/.."

echo "✅ Backend setup complete!"
echo ""
echo "🚀 To start the backend server:"
echo "1. Activate the virtual environment: source koyl_ai_env/bin/activate"
echo "2. Run the backend: python scripts/backend/run_backend.py"
echo ""
echo "🧠 To train AI models (optional):"
echo "1. Activate the virtual environment: source koyl_ai_env/bin/activate"
echo "2. Run training: python scripts/backend/ai_trainer.py"
echo ""
echo "📊 To check dependencies anytime:"
echo "   python scripts/backend/check_dependencies.py"
echo ""
echo "The backend will be available at: http://localhost:5000"
