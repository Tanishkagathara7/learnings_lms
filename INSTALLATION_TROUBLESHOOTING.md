# Installation Troubleshooting Guide

## ❌ Common Error: "Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'"

This error occurs when the `requirements.txt` file cannot be found. Here are the solutions:

### 🔧 Solution 1: Check Current Directory

Make sure you're in the correct project directory:

```bash
# Navigate to the project directory first
cd path/to/AI-Study-Pal-project

# Verify you're in the right directory
ls -la
# You should see: requirements.txt, setup.py, README.md, etc.

# Then install dependencies
pip install -r requirements.txt
```

### 🔧 Solution 2: Use Absolute Path

If you're not in the project directory, use the full path:

```bash
pip install -r /full/path/to/project/requirements.txt
```

### 🔧 Solution 3: Use Alternative Requirements Files

We provide multiple requirements files for different scenarios:

```bash
# For flexible version compatibility (RECOMMENDED)
pip install -r requirements-flexible.txt

# For conda users
pip install -r requirements-conda.txt

# For exact versions (may cause compatibility issues)
pip install -r requirements.txt
```

### 🔧 Solution 4: Manual Installation

If requirements files don't work, install packages manually:

```bash
# Core packages
pip install pandas numpy matplotlib seaborn scikit-learn
pip install tensorflow nltk flask jupyter notebook
pip install requests beautifulsoup4

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### 🔧 Solution 5: Use Setup Scripts

We provide automated setup scripts:

**Windows:**
```cmd
# Run the batch file
setup.bat

# Or run Python setup
python setup.py install
```

**macOS/Linux:**
```bash
# Make script executable
chmod +x setup.sh

# Run setup script
./setup.sh

# Or run Python setup
python setup.py install
```

### 🔧 Solution 6: Virtual Environment Setup

Create a clean virtual environment:

```bash
# Create virtual environment
python -m venv ai_study_pal_env

# Activate it
# Windows:
ai_study_pal_env\Scripts\activate
# macOS/Linux:
source ai_study_pal_env/bin/activate

# Install dependencies
pip install -r requirements-flexible.txt
```

### 🔧 Solution 7: Check Python Version

Ensure you're using a compatible Python version:

```bash
python --version
# Should be Python 3.8 or higher

# If using Python 3.12+, use flexible requirements
pip install -r requirements-flexible.txt
```

## 🚀 Quick Start Commands

Copy and paste these commands in order:

```bash
# 1. Navigate to project directory
cd AI-Study-Pal-project

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies (try in this order)
pip install -r requirements-flexible.txt
# OR if above fails:
pip install -r requirements.txt
# OR if both fail:
python setup.py install

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"

# 5. Test installation
python test_all_modules.py

# 6. Run the application
cd web_app
python app.py
```

## 🔍 Debugging Steps

If you're still having issues:

1. **Check file existence:**
   ```bash
   ls -la requirements*.txt
   ```

2. **Check current directory:**
   ```bash
   pwd
   ls -la
   ```

3. **Try different Python commands:**
   ```bash
   python3 -m pip install -r requirements-flexible.txt
   py -m pip install -r requirements-flexible.txt
   ```

4. **Check pip version:**
   ```bash
   pip --version
   python -m pip --version
   ```

5. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

## 📞 Still Need Help?

If none of these solutions work:

1. Check the `QUICK_FIX.md` file for additional solutions
2. Review the `INSTALLATION_GUIDE.md` for detailed setup instructions
3. Try the automated `fix_installation.py` script:
   ```bash
   python fix_installation.py
   ```

## 🎯 Platform-Specific Notes

### Windows
- Use `python` instead of `python3`
- Use backslashes `\` in paths
- May need to run as Administrator

### macOS
- Use `python3` instead of `python`
- May need to install Xcode command line tools
- Use `pip3` instead of `pip`

### Linux
- Use `python3` and `pip3`
- May need to install `python3-venv` package
- Check distribution-specific package managers

## ✅ Verification

After successful installation, verify everything works:

```bash
# Test all modules
python test_all_modules.py

# Should output: "🎉 ALL TESTS PASSED! AI Study Pal is ready for deployment."
```