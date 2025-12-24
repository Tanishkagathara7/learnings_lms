# 🚀 AI Study Pal - Complete Installation Guide

This guide provides step-by-step instructions for setting up AI Study Pal on a new computer after downloading from GitHub.

## 📋 Quick Setup (Automated)

### For Windows Users
1. Download and extract the project
2. Open Command Prompt or PowerShell in the project folder
3. Run: `setup.bat`
4. Follow the on-screen instructions

### For macOS/Linux Users
1. Download and extract the project
2. Open Terminal in the project folder
3. Run: `chmod +x setup.sh && ./setup.sh`
4. Follow the on-screen instructions

### Using Python Setup Script (All Platforms)
```bash
python setup.py
```

## 🛠️ Manual Setup (Step by Step)

### Step 1: Prerequisites Check

#### Check Python Version
```bash
# Windows
python --version
py -3 --version

# macOS/Linux
python3 --version
```

**Required**: Python 3.10 or higher

#### Install Python (if needed)
- **Windows**: Download from [python.org](https://python.org) and check "Add to PATH"
- **macOS**: Use Homebrew: `brew install python3` or download from python.org
- **Linux**: Use package manager: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### Step 2: Download Project

#### Option A: Git Clone
```bash
git clone <repository-url>
cd ai-study-pal
```

#### Option B: Download ZIP
1. Download ZIP file from GitHub
2. Extract to desired location
3. Open terminal/command prompt in extracted folder

### Step 3: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv ai-study-pal-env

# Activate it
# Windows:
ai-study-pal-env\Scripts\activate
# macOS/Linux:
source ai-study-pal-env/bin/activate
```

### Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**If you get errors**, try:
```bash
# For Windows users with multiple Python versions
py -3 -m pip install -r requirements.txt

# For macOS/Linux users
python3 -m pip install -r requirements.txt
```

### Step 5: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')"
```

### Step 6: Verify Installation

```bash
python test_all_modules.py
```

**Expected Output:**
```
🎉 ALL TESTS PASSED! AI Study Pal is ready for deployment.
```

### Step 7: Start Application

```bash
cd web_app
python app.py
```

### Step 8: Access Application

Open your browser and go to: **http://127.0.0.1:5000**

## 🚨 SPECIFIC FIX FOR YOUR ERROR

**Your error shows Anaconda + Network timeout + Build dependencies failure. Here's the exact solution:**

### Quick Fix (Recommended)
```bash
# 1. Use conda for scientific packages (avoids compilation)
conda install pandas numpy matplotlib seaborn scikit-learn jupyter requests

# 2. Use pip for remaining packages
pip install flask nltk beautifulsoup4

# 3. Try TensorFlow (if it fails, use CPU version)
pip install tensorflow
# If TensorFlow fails:
pip install tensorflow-cpu

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')"

# 5. Test everything
python test_all_modules.py
```

### Alternative: Use Flexible Requirements
```bash
# Instead of requirements.txt, use:
pip install -r requirements-flexible.txt
```

### Last Resort: Run Troubleshooter
```bash
python fix_installation.py
```

## 🔧 Troubleshooting All Common Issues

### Issue 1: "python is not recognized"
**Solution**: 
- Reinstall Python and check "Add to PATH"
- Use `py -3` instead of `python` on Windows
- Use `python3` instead of `python` on macOS/Linux

### Issue 2: "No module named 'xyz'"
**Solution**:
```bash
# Make sure you're in the right directory
pip install -r requirements.txt

# Or try with full path
python -m pip install -r requirements.txt
```

### Issue 3: Permission Denied (macOS/Linux)
**Solution**:
```bash
# Make scripts executable
chmod +x setup.sh

# Or use sudo for pip install
sudo pip3 install -r requirements.txt
```

### Issue 4: TensorFlow Installation Issues
**Solution**:
```bash
# For older CPUs without AVX support
pip install tensorflow-cpu

# For Apple Silicon Macs
pip install tensorflow-macos tensorflow-metal
```

### Issue 5: NLTK Data Download Fails
**Solution**:
```bash
# Download all NLTK data
python -c "import nltk; nltk.download('all')"

# Or download manually in Python
python
>>> import nltk
>>> nltk.download()
```

### Issue 6: Port 5000 Already in Use
**Solution**:
- Kill the process using port 5000
- Or modify `app.py` to use a different port:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Issue 7: Virtual Environment Issues
**Solution**:
```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf ai-study-pal-env  # Linux/macOS
rmdir /s ai-study-pal-env  # Windows

# Create new environment
python -m venv ai-study-pal-env
```

## 📊 System-Specific Instructions

### Windows 10/11
```bash
# Use PowerShell or Command Prompt
# If python doesn't work, try:
py -3 --version
py -3 -m pip install -r requirements.txt
cd web_app
py -3 app.py
```

### macOS (Intel/Apple Silicon)
```bash
# Use Terminal
# Make sure you have Xcode Command Line Tools
xcode-select --install

# Use python3 explicitly
python3 --version
python3 -m pip install -r requirements.txt
cd web_app
python3 app.py
```

### Ubuntu/Debian Linux
```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Continue with normal setup
python3 -m venv ai-study-pal-env
source ai-study-pal-env/bin/activate
pip install -r requirements.txt
```

### CentOS/RHEL/Fedora
```bash
# Install Python and pip
sudo yum install python3 python3-pip  # CentOS/RHEL
sudo dnf install python3 python3-pip  # Fedora

# Continue with normal setup
```

## 🎯 Verification Checklist

Before using the application, verify:

- [ ] Python 3.10+ is installed
- [ ] All dependencies are installed (`pip list` shows required packages)
- [ ] NLTK data is downloaded
- [ ] All tests pass (`python test_all_modules.py`)
- [ ] Web server starts without errors
- [ ] Application is accessible at http://127.0.0.1:5000
- [ ] You can create a study plan successfully

## 🔄 Updating the Application

To update to a newer version:

```bash
# Pull latest changes (if using git)
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run tests to verify
python test_all_modules.py
```

## 🆘 Getting Help

If you're still having issues:

1. **Check the error message** carefully
2. **Search for the error** online (Stack Overflow, GitHub Issues)
3. **Try the troubleshooting steps** above
4. **Run the test suite** to identify specific problems
5. **Check your Python and package versions** for compatibility

## 📱 Alternative Setup Methods

### Using Conda
```bash
# Create conda environment
conda create -n ai-study-pal python=3.11
conda activate ai-study-pal
pip install -r requirements.txt
```

### Using Docker (Advanced)
```bash
# Build Docker image
docker build -t ai-study-pal .

# Run container
docker run -p 5000:5000 ai-study-pal
```

### Using Replit/Codespaces
1. Import the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download NLTK data
4. Run: `cd web_app && python app.py`

---

**Need more help?** Check the main README.md file for additional information and troubleshooting tips.