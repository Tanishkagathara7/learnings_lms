#!/usr/bin/env python3
"""
Emergency Installation Script for AI Study Pal
Fixes the "requirements.txt not found" error and installs dependencies
"""

import os
import sys
import subprocess

def emergency_install():
    """Emergency installation when requirements.txt is not found"""
    print("🚨 AI Study Pal - Emergency Installation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('setup.py') and not os.path.exists('README.md'):
        print("❌ ERROR: Not in the correct project directory!")
        print("Please navigate to the AI-Study-Pal-project folder first:")
        print("cd path/to/AI-Study-Pal-project")
        print("Then run this script again.")
        return False
    
    print("✓ Found project files, proceeding with emergency installation...")
    
    # Core packages that are essential
    packages = [
        "pandas>=2.0.0",
        "numpy>=1.24.0", 
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "scikit-learn>=1.3.0",
        "flask>=2.3.0",
        "nltk>=3.8.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "jupyter>=1.0.0"
    ]
    
    print(f"\n📦 Installing {len(packages)} essential packages...")
    
    # Try to install each package
    failed_packages = []
    for i, package in enumerate(packages, 1):
        try:
            print(f"[{i}/{len(packages)}] Installing {package.split('>=')[0]}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            print(f"✓ {package.split('>=')[0]} installed")
        except subprocess.CalledProcessError:
            print(f"✗ {package.split('>=')[0]} failed")
            failed_packages.append(package)
    
    # Try TensorFlow separately (often problematic)
    print("\n🧠 Installing TensorFlow...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'tensorflow>=2.13.0'], 
                     check=True, capture_output=True)
        print("✓ TensorFlow installed")
    except subprocess.CalledProcessError:
        print("⚠️  TensorFlow failed, trying CPU version...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'tensorflow-cpu'], 
                         check=True, capture_output=True)
            print("✓ TensorFlow CPU installed")
        except subprocess.CalledProcessError:
            print("✗ TensorFlow installation failed (you can skip this for now)")
            failed_packages.append('tensorflow')
    
    # Download NLTK data
    print("\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("✓ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️  NLTK data download failed: {e}")
    
    # Test imports
    print("\n🧪 Testing imports...")
    test_modules = ['pandas', 'numpy', 'matplotlib', 'sklearn', 'flask', 'nltk', 'requests']
    import_failures = []
    
    for module in test_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module}")
            import_failures.append(module)
    
    # Summary
    print("\n" + "=" * 50)
    if not failed_packages and not import_failures:
        print("🎉 EMERGENCY INSTALLATION SUCCESSFUL!")
        print("\n🚀 Next steps:")
        print("1. cd web_app")
        print("2. python app.py")
        print("3. Open http://127.0.0.1:5000")
        return True
    else:
        print("⚠️  PARTIAL INSTALLATION COMPLETED")
        if failed_packages:
            print(f"Failed packages: {', '.join([p.split('>=')[0] for p in failed_packages])}")
        if import_failures:
            print(f"Import failures: {', '.join(import_failures)}")
        
        print("\n💡 Try these solutions:")
        print("1. Run: python fix_installation.py")
        print("2. Install failed packages manually:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
        print("3. Check QUICK_FIX.md for more solutions")
        return False

if __name__ == "__main__":
    try:
        success = emergency_install()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Emergency installation failed: {e}")
        print("Please check QUICK_FIX.md or INSTALLATION_TROUBLESHOOTING.md")
        sys.exit(1)