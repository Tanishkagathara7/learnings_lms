# AI Study Pal - Intelligent Study Assistant

A comprehensive AI-powered study assistant that combines Machine Learning, Deep Learning, and Natural Language Processing to create personalized study plans, generate quizzes, and provide intelligent study recommendations.

## 🚀 Features

- **Smart Study Plans**: AI-generated personalized 7-day study schedules
- **Topic Selection**: Choose specific topics within subjects for focused learning
- **Scenario-Based Planning**: Different study approaches for exam prep, homework, projects, and general study
- **ML-Powered Quizzes**: Difficulty classification and topic clustering
- **Deep Learning Text Processing**: Neural network-based content summarization
- **NLP Study Tips**: Contextual recommendations using natural language processing
- **Web Interface**: Complete Flask-based user experience with responsive design
- **Download Options**: Export study plans as CSV files

## 📋 Prerequisites

Before setting up the project, ensure you have:

- **Python 3.10 or higher** (Python 3.13 recommended)
- **Git** (for cloning the repository)
- **4GB RAM minimum** (8GB recommended for optimal performance)
- **2GB free disk space**
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 🛠️ Installation & Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd ai-study-pal

# Or if downloading as ZIP, extract and navigate to the folder
```

### Step 2: Check Python Version

```bash
# Check Python version (must be 3.10+)
python --version
# or
python3 --version
# or
py -3 --version
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv ai-study-pal-env

# Activate virtual environment
# On Windows:
ai-study-pal-env\Scripts\activate
# On macOS/Linux:
source ai-study-pal-env/bin/activate
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# If you encounter issues, try upgrading pip first:
pip install --upgrade pip
pip install -r requirements.txt

# 🚨 HAVING INSTALLATION ISSUES? 
# Try these alternatives:

# Option A: Use flexible requirements (recommended)
pip install -r requirements-flexible.txt

# Option B: For Anaconda users (like the error you showed)
conda install pandas numpy matplotlib seaborn scikit-learn jupyter requests
pip install flask nltk beautifulsoup4 tensorflow-cpu

# Option C: Run the automated troubleshooter
python fix_installation.py

# Option D: See QUICK_FIX.md for your specific error
```

### Step 5: Download NLTK Data

```bash
# Download required NLTK data
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet')"
```

### Step 6: Verify Installation

```bash
# Run comprehensive tests to verify everything works
python test_all_modules.py
```

You should see:
```
🎉 ALL TESTS PASSED! AI Study Pal is ready for deployment.
```

### Step 7: Start the Application

```bash
# Navigate to web app directory
cd web_app

# Start the Flask server
python app.py
```

### Step 8: Access the Application

Open your web browser and go to:
- **Local access**: http://127.0.0.1:5000
- **Network access**: http://[your-ip]:5000

## 🎯 Quick Start Guide

1. **Select Subject**: Choose from Mathematics, Physics, Chemistry, Biology, Computer Science, etc.
2. **Choose Topics**: Select specific topics you want to focus on (optional)
3. **Set Study Hours**: Enter daily study hours (0.5 to 12 hours)
4. **Pick Scenario**: 
   - **General Study**: Balanced learning approach
   - **Exam Preparation**: Intensive, exam-focused strategy
   - **Homework Help**: Task-oriented, deadline-driven
   - **Project Work**: Research-heavy, creative approach
5. **Generate Plan**: Click "Generate AI Study Plan"
6. **Use Features**:
   - View personalized study schedule
   - Take AI-generated quizzes
   - Get NLP-based study tips
   - Download study plan as CSV

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Python Version Issues
```bash
# If python command doesn't work, try:
python3 app.py
# or
py -3 app.py
```

#### 2. Module Not Found Errors
```bash
# Ensure you're in the correct directory and virtual environment is activated
pip install -r requirements.txt
```

#### 3. NLTK Data Missing
```bash
# Download NLTK data manually
python -c "import nltk; nltk.download('all')"
```

#### 4. TensorFlow/Keras Warnings
These warnings are normal and don't affect functionality:
```
WARNING: This is a development server. Do not use it in a production deployment.
```

#### 5. Port Already in Use
```bash
# If port 5000 is busy, the app will show an error
# Kill the process using port 5000 or restart your computer
```

#### 6. File Permission Issues
```bash
# On macOS/Linux, you might need to set permissions
chmod +x app.py
```

## 📁 Project Structure

```
ai-study-pal/
├── data/                          # Educational content and user data
│   ├── educational_content.csv    # Subject and topic data
│   └── user_inputs.json          # Saved user preferences
├── src/                           # Core AI modules
│   ├── data_preprocessing.py      # Data handling and EDA
│   ├── ml_quiz_generator.py       # Machine learning quiz system
│   ├── dl_text_processor.py       # Deep learning text processing
│   ├── nlp_study_tips.py         # NLP-based recommendations
│   └── study_planner.py          # Study schedule generation
├── web_app/                       # Flask web application
│   ├── app.py                     # Main Flask application
│   ├── templates/                 # HTML templates
│   └── static/                    # CSS, JS, and assets
├── models/                        # Trained AI models (auto-generated)
├── outputs/                       # Generated files and visualizations
├── notebooks/                     # Jupyter notebooks for demos
├── requirements.txt               # Python dependencies
├── test_all_modules.py           # Comprehensive test suite
└── README.md                     # This file
```

## 🧪 Testing

Run the comprehensive test suite to verify all components:

```bash
# Run all tests
python test_all_modules.py

# Test individual modules
python -c "from src.data_preprocessing import DataPreprocessor; dp = DataPreprocessor(); dp.load_data()"
```

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
# Update all packages
pip install --upgrade -r requirements.txt
```

### Backing Up Data
```bash
# Important files to backup:
# - data/user_inputs.json (user preferences)
# - models/ directory (trained models)
# - outputs/ directory (generated content)
```

## 🌐 Deployment Options

### Local Development
- Use the built-in Flask development server (current setup)
- Perfect for personal use and testing

### Production Deployment
For production use, consider:
- **Gunicorn**: `pip install gunicorn && gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- **Docker**: Create a Dockerfile for containerized deployment
- **Cloud Platforms**: Deploy to Heroku, AWS, Google Cloud, or Azure

## 📊 System Requirements

### Minimum Requirements
- **CPU**: Dual-core processor
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Python**: 3.10+

### Recommended Requirements
- **CPU**: Quad-core processor or better
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **Python**: 3.13 (latest stable)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. **Check the troubleshooting section** above
2. **Run the test suite** to identify specific problems
3. **Check Python and package versions** for compatibility
4. **Ensure all NLTK data is downloaded** properly
5. **Verify file permissions** and directory structure

## 🎓 Academic Use

This project demonstrates:
- **Machine Learning**: Classification and clustering algorithms
- **Deep Learning**: Neural networks with TensorFlow/Keras
- **Natural Language Processing**: Text analysis with NLTK
- **Web Development**: Full-stack application with Flask
- **Data Science**: EDA, visualization, and statistical analysis

Perfect for:
- Computer Science coursework
- AI/ML project demonstrations
- Educational technology research
- Portfolio projects

---

**Made with ❤️ for students and educators worldwide**