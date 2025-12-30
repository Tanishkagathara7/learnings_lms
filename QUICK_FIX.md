# 🚨 QUICK FIX for Installation Errors

## 🔥 URGENT: "Could not open requirements file" Error

**ERROR:** `Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`

### ⚡ IMMEDIATE SOLUTION (Copy & Paste)

```bash
# 1. Check if you're in the correct directory
ls -la
# You should see: requirements.txt, setup.py, README.md

# 2. If files are missing, navigate to project directory
cd AI-Study-Pal-project

# 3. Use flexible requirements (MOST RELIABLE)
pip install -r requirements-flexible.txt

# 4. If that fails, manual installation:
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow flask nltk requests beautifulsoup4
```

### 🔧 Why This Error Happens

1. **Wrong Directory**: You're not in the project folder
2. **Missing Files**: requirements.txt was not downloaded/extracted properly
3. **Path Issues**: Incorrect file paths or permissions

### 📍 Directory Check

Make sure you see these files:
```
AI-Study-Pal-project/
├── requirements.txt
├── requirements-flexible.txt
├── setup.py
├── README.md
├── web_app/
├── src/
└── data/
```

---

## Your Error: Anaconda + Network Timeout + Build Dependencies

### ⚡ One-Line Solution (Copy & Paste)

```bash
conda install pandas numpy matplotlib seaborn scikit-learn jupyter requests && pip install flask nltk beautifulsoup4 tensorflow-cpu && python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')"
```

### 📋 Step-by-Step (If one-liner fails)

```bash
# 1. Install scientific packages via conda (pre-compiled, no build needed)
conda install pandas numpy matplotlib seaborn scikit-learn jupyter requests

# 2. Install web/ML packages via pip
pip install flask nltk beautifulsoup4

# 3. Install TensorFlow (CPU version is more reliable)
pip install tensorflow-cpu

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')"

# 5. Test installation
python test_all_modules.py

# 6. Start the app
cd web_app
python app.py
```

### 🔄 Alternative Methods

#### Method 1: Use Flexible Requirements
```bash
pip install -r requirements-flexible.txt
```

#### Method 2: Install Without Versions
```bash
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow flask nltk requests beautifulsoup4
```

#### Method 3: Run Automated Fixer
```bash
python fix_installation.py
```

#### Method 4: Virtual Environment (Clean Start)
```bash
python -m venv ai_study_env
# Windows: ai_study_env\Scripts\activate
# macOS/Linux: source ai_study_env/bin/activate
pip install -r requirements-flexible.txt
```

### 💡 Why This Happens

1. **Anaconda Environment**: You're using Anaconda, which sometimes conflicts with pip
2. **Network Timeouts**: PyPI connection issues during download
3. **Build Dependencies**: Some packages need compilation, which fails
4. **Version Conflicts**: Specific versions in requirements.txt need building
5. **File Path Issues**: Wrong directory or missing files

### ✅ The Solution

- **Check directory first**: Make sure you're in the right folder
- Use **conda** for scientific packages (pandas, numpy, matplotlib) - these are pre-compiled
- Use **pip** for pure Python packages (flask, nltk)
- Use **tensorflow-cpu** instead of regular tensorflow (more compatible)
- Use **requirements-flexible.txt** for better compatibility

### 🎯 After Installation

1. `cd web_app`
2. `python app.py`
3. Open http://127.0.0.1:5000

### 📞 Still Having Issues?

1. **Run:** `python fix_installation.py`
2. **Check:** `INSTALLATION_TROUBLESHOOTING.md`
3. **Manual:** Install packages one by one
4. **Help:** Create virtual environment

---

**This should fix your installation issues! 🚀**