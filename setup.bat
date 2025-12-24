@echo off
echo 🚀 AI Study Pal - Windows Setup Script
echo =====================================

echo.
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo 🔄 Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 🔄 Attempting to install dependencies...
echo 📦 Trying standard requirements first...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ⚠️ Standard installation failed. Trying flexible requirements...
    pip install -r requirements-flexible.txt
    
    if %errorlevel% neq 0 (
        echo ⚠️ Flexible installation also failed. Running troubleshooter...
        python fix_installation.py
    )
)

echo.
echo 🔄 Downloading NLTK data...
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')" 2>nul

echo.
echo 🧪 Running tests...
python test_all_modules.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Setup completed successfully!
    echo.
    echo 📋 To start the application:
    echo 1. cd web_app
    echo 2. python app.py
    echo 3. Open http://127.0.0.1:5000 in your browser
) else (
    echo.
    echo ⚠️ Some tests failed. Try running: python fix_installation.py
    echo Or manually install packages: pip install pandas numpy matplotlib flask tensorflow nltk
)

echo.
echo 💡 If you're still having issues, check INSTALLATION_GUIDE.md for detailed troubleshooting
pause