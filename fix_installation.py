#!/usr/bin/env python3
"""
AI Study Pal - Installation Troubleshooter
Fixes common installation issues and provides alternative installation methods
"""

import os
import sys
import subprocess
import platform

def run_command(command, description, ignore_errors=False):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"⚠️ {description} failed (continuing anyway): {e}")
            return False
        else:
            print(f"❌ {description} failed: {e}")
            print(f"Error output: {e.stderr}")
            return False

def check_environment():
    """Check the current Python environment"""
    print("🔍 Checking Python environment...")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    
    # Check if we're in a conda environment
    if 'conda' in sys.executable.lower() or 'anaconda' in sys.executable.lower():
        print("📦 Detected Anaconda/Conda environment")
        return 'conda'
    else:
        print("🐍 Detected standard Python environment")
        return 'pip'

def fix_conda_installation():
    """Fix installation issues in Conda environment"""
    print("\n🔧 Fixing Conda installation issues...")
    
    # Update conda first
    run_command("conda update conda", "Updating conda", ignore_errors=True)
    
    # Install packages via conda first (these are pre-compiled)
    conda_packages = [
        "pandas", "numpy", "matplotlib", "seaborn", 
        "scikit-learn", "flask", "jupyter", "requests"
    ]
    
    for package in conda_packages:
        run_command(f"conda install -y {package}", f"Installing {package} via conda", ignore_errors=True)
    
    # Install remaining packages via pip
    pip_packages = ["tensorflow", "nltk", "beautifulsoup4"]
    for package in pip_packages:
        run_command(f"pip install {package}", f"Installing {package} via pip", ignore_errors=True)

def fix_pip_installation():
    """Fix installation issues in standard pip environment"""
    print("\n🔧 Fixing pip installation issues...")
    
    # Upgrade pip first
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Try installing with flexible requirements
    if os.path.exists('requirements-flexible.txt'):
        run_command("pip install -r requirements-flexible.txt", "Installing flexible requirements")
    else:
        # Install packages individually with flexible versions
        packages = [
            "pandas>=2.0.0",
            "numpy>=1.24.0", 
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "scikit-learn>=1.3.0",
            "flask>=2.3.0",
            "nltk>=3.8.0",
            "requests>=2.31.0",
            "beautifulsoup4>=4.12.0"
        ]
        
        for package in packages:
            run_command(f"pip install '{package}'", f"Installing {package}", ignore_errors=True)
        
        # Try TensorFlow last (most problematic)
        if not run_command("pip install tensorflow>=2.13.0", "Installing TensorFlow"):
            print("⚠️ TensorFlow installation failed. Trying CPU-only version...")
            run_command("pip install tensorflow-cpu>=2.13.0", "Installing TensorFlow CPU", ignore_errors=True)

def alternative_installation_methods():
    """Provide alternative installation methods"""
    print("\n🔄 Alternative installation methods:")
    
    print("\n1️⃣ Method 1: Install without specific versions")
    print("pip install pandas numpy matplotlib seaborn scikit-learn tensorflow flask nltk requests beautifulsoup4")
    
    print("\n2️⃣ Method 2: Install one by one")
    print("pip install pandas")
    print("pip install numpy")
    print("pip install matplotlib")
    print("# ... continue for each package")
    
    print("\n3️⃣ Method 3: Use conda for scientific packages")
    print("conda install pandas numpy matplotlib seaborn scikit-learn")
    print("pip install tensorflow flask nltk")
    
    print("\n4️⃣ Method 4: Use pre-compiled wheels")
    print("pip install --only-binary=all pandas numpy matplotlib")
    
    print("\n5️⃣ Method 5: Increase timeout and retries")
    print("pip install --timeout 1000 --retries 10 -r requirements.txt")

def download_nltk_data():
    """Download NLTK data"""
    print("\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt_tab', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded successfully")
    except Exception as e:
        print(f"⚠️ NLTK data download failed: {e}")

def test_installation():
    """Test if all packages are working"""
    print("\n🧪 Testing installation...")
    
    packages_to_test = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('matplotlib.pyplot', 'plt'),
        ('seaborn', 'sns'),
        ('sklearn', None),
        ('flask', None),
        ('nltk', None),
        ('requests', None)
    ]
    
    failed_packages = []
    
    for package, alias in packages_to_test:
        try:
            if alias:
                exec(f"import {package} as {alias}")
            else:
                exec(f"import {package}")
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} failed to import: {e}")
            failed_packages.append(package)
    
    # Test TensorFlow separately (it's often problematic)
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ TensorFlow failed to import: {e}")
        failed_packages.append('tensorflow')
    
    return failed_packages

def main():
    """Main troubleshooting function"""
    print("🚀 AI Study Pal - Installation Troubleshooter")
    print("=" * 50)
    
    # Check environment
    env_type = check_environment()
    
    # Try to fix based on environment
    if env_type == 'conda':
        fix_conda_installation()
    else:
        fix_pip_installation()
    
    # Download NLTK data
    download_nltk_data()
    
    # Test installation
    failed_packages = test_installation()
    
    if not failed_packages:
        print("\n🎉 All packages installed successfully!")
        print("\n📋 Next steps:")
        print("1. cd web_app")
        print("2. python app.py")
        print("3. Open http://127.0.0.1:5000")
    else:
        print(f"\n⚠️ Some packages failed to install: {failed_packages}")
        print("\n🔧 Try these solutions:")
        alternative_installation_methods()
        
        print(f"\n💡 For the failed packages, try installing them individually:")
        for package in failed_packages:
            print(f"pip install {package}")

if __name__ == "__main__":
    main()