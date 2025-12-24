#!/bin/bash

echo "🚀 AI Study Pal - macOS/Linux Setup Script"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+ from https://python.org"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check Python version
python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"
if [ $? -ne 0 ]; then
    echo "❌ Python 3.10+ required. Please upgrade your Python installation."
    exit 1
fi

echo "✅ Python version is compatible"

# Create virtual environment (optional but recommended)
read -p "🤔 Create virtual environment? (y/n): " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "🔄 Creating virtual environment..."
    python3 -m venv ai-study-pal-env
    source ai-study-pal-env/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies
echo "🔄 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Download NLTK data
echo "🔄 Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')"

# Create necessary directories
mkdir -p models outputs

# Run tests
echo "🧪 Running comprehensive tests..."
python3 test_all_modules.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 To start the application:"
    echo "1. cd web_app"
    echo "2. python3 app.py"
    echo "3. Open http://127.0.0.1:5000 in your browser"
    
    if [[ $create_venv =~ ^[Yy]$ ]]; then
        echo ""
        echo "💡 Remember to activate your virtual environment next time:"
        echo "source ai-study-pal-env/bin/activate"
    fi
else
    echo ""
    echo "⚠️ Some tests failed, but you can still try running the application"
fi

echo ""
echo "🎯 Enjoy using AI Study Pal!"