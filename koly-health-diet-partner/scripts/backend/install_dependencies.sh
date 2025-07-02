#!/bin/bash

# KOYL AI Backend Dependencies Installation Script
echo "🚀 Installing KOYL AI Backend Dependencies..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo "🐍 Checking Python version..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
    echo "✅ Python version: $PYTHON_VERSION"
    
    # Check if Python version is 3.8 or higher
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        echo "✅ Python version is compatible"
    else
        echo "❌ Python 3.8+ required. Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if pip is available
if command_exists pip3; then
    PIP_CMD="pip3"
elif command_exists pip; then
    PIP_CMD="pip"
else
    echo "❌ pip not found. Please install pip"
    exit 1
fi

echo "📦 Using pip command: $PIP_CMD"

# Upgrade pip
echo "⬆️ Upgrading pip..."
$PIP_CMD install --upgrade pip

# Install dependencies in order (some have dependencies on others)
echo "📚 Installing core dependencies..."

# Core Python packages
$PIP_CMD install numpy==1.24.3
$PIP_CMD install requests==2.31.0
$PIP_CMD install python-dotenv==1.0.0

# Data processing
$PIP_CMD install pandas==2.0.3
$PIP_CMD install scikit-learn==1.3.0

# Web framework
$PIP_CMD install Flask==2.3.3
$PIP_CMD install Flask-CORS==4.0.0
$PIP_CMD install gunicorn==21.2.0

# XML and web scraping
$PIP_CMD install lxml==4.9.3
$PIP_CMD install beautifulsoup4==4.12.2

echo "🧠 Installing AI/ML dependencies..."

# PyTorch (CPU version for compatibility)
$PIP_CMD install torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu

# Transformers and related
$PIP_CMD install transformers==4.33.2
$PIP_CMD install sentence-transformers==2.2.2
$PIP_CMD install datasets==2.14.4
$PIP_CMD install accelerate==0.21.0
$PIP_CMD install evaluate==0.4.0

# Vector search
$PIP_CMD install faiss-cpu==1.7.4

echo "📊 Installing visualization and NLP dependencies..."

# Visualization
$PIP_CMD install matplotlib==3.7.2
$PIP_CMD install seaborn==0.12.2

# NLP
$PIP_CMD install nltk==3.8.1

# Optional: spaCy (commented out due to size, uncomment if needed)
# $PIP_CMD install spacy==3.6.1

echo "🧪 Testing installations..."

# Test core imports
python3 -c "
import sys
import traceback

def test_import(module_name, package_name=None):
    try:
        __import__(module_name)
        print(f'✅ {package_name or module_name}')
        return True
    except ImportError as e:
        print(f'❌ {package_name or module_name}: {e}')
        return False

print('🧪 Testing core dependencies:')
success = True
success &= test_import('numpy')
success &= test_import('requests')
success &= test_import('flask', 'Flask')
success &= test_import('sklearn', 'scikit-learn')
success &= test_import('pandas')

print('\n🧪 Testing AI/ML dependencies:')
success &= test_import('torch', 'PyTorch')
success &= test_import('transformers')
success &= test_import('sentence_transformers')
success &= test_import('faiss', 'faiss-cpu')

if success:
    print('\n✅ All dependencies installed successfully!')
else:
    print('\n❌ Some dependencies failed to install')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 KOYL AI Backend dependencies installed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Start the backend: python run_backend.py"
    echo "2. Or train the AI models: python ai_trainer.py"
    echo ""
    echo "💡 Tip: If you encounter memory issues during training,"
    echo "   consider using a machine with more RAM or reducing batch sizes."
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
