# 🚀 AI Study Pal - Quick Start Guide

## ⚡ 30-Second Setup

### Windows Users
```bash
# 1. Download and extract the project
# 2. Open Command Prompt in the project folder
# 3. Run the setup script
setup.bat
```

### macOS/Linux Users
```bash
# 1. Download and extract the project
# 2. Open Terminal in the project folder
# 3. Run the setup script
chmod +x setup.sh && ./setup.sh
```

### All Platforms (Python Script)
```bash
python setup.py
```

## 🎯 Manual Setup (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download NLTK data
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')"

# 3. Test everything works
python test_all_modules.py

# 4. Start the application
cd web_app
python app.py
```

## 🌐 Access the Application

Open your browser and go to: **http://127.0.0.1:5000**

## 🎮 How to Use

1. **Select Subject**: Mathematics, Physics, Chemistry, etc.
2. **Choose Topics**: Pick specific topics (e.g., Algebra, Calculus)
3. **Set Study Hours**: 0.5 to 12 hours per day
4. **Pick Scenario**: 
   - General Study (balanced)
   - Exam Preparation (intensive)
   - Homework Help (task-focused)
   - Project Work (research-heavy)
5. **Generate Plan**: Get your personalized AI study plan!

## 🔧 If Something Goes Wrong

### Python Not Found?
```bash
# Try these alternatives:
python3 app.py    # macOS/Linux
py -3 app.py      # Windows
```

### Dependencies Failed?
```bash
# Upgrade pip first:
pip install --upgrade pip
pip install -r requirements.txt
```

### Tests Failed?
```bash
# Check Python version (need 3.10+):
python --version

# Try downloading all NLTK data:
python -c "import nltk; nltk.download('all')"
```

## 📋 What You Get

- ✅ **Smart Study Plans**: 7-day personalized schedules
- ✅ **Topic Selection**: Focus on specific subjects
- ✅ **Scenario Planning**: Different approaches for different goals
- ✅ **AI Quizzes**: Machine learning-powered questions
- ✅ **Study Tips**: NLP-generated recommendations
- ✅ **Download Options**: Export plans as CSV files

## 🆘 Need Help?

1. Check `INSTALLATION_GUIDE.md` for detailed instructions
2. Check `README.md` for comprehensive documentation
3. Run `python test_all_modules.py` to diagnose issues

---

**Ready to boost your studying with AI? Let's go! 🎓**