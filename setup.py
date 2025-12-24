#!/usr/bin/env python3
"""
AI Study Pal - Quick Setup Script
Automates the installation and setup process for new users
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.10 or higher")
        return False

def main():
    """Main setup function"""
    print("🚀 AI Study Pal - Quick Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install --upgrade pip", "Upgrading pip"):
        print("⚠️ Pip upgrade failed, continuing anyway...")
    
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Download NLTK data
    nltk_command = 'python -c "import nltk; nltk.download(\'punkt_tab\'); nltk.download(\'stopwords\'); nltk.download(\'averaged_perceptron_tagger_eng\'); nltk.download(\'wordnet\')"'
    if not run_command(nltk_command, "Downloading NLTK data"):
        print("⚠️ NLTK data download failed. You may need to download it manually.")
    
    # Create necessary directories
    directories = ['models', 'outputs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
    
    # Run tests
    print("\n🧪 Running comprehensive tests...")
    if run_command("python test_all_modules.py", "Testing all modules"):
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Navigate to web_app directory: cd web_app")
        print("2. Start the application: python app.py")
        print("3. Open your browser to: http://127.0.0.1:5000")
        print("\n🎯 Enjoy using AI Study Pal!")
    else:
        print("\n⚠️ Some tests failed. The application may still work, but please check the error messages above.")
        print("You can still try running the application with:")
        print("cd web_app && python app.py")

if __name__ == "__main__":
    main()