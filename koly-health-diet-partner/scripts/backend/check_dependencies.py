#!/usr/bin/env python3
"""
KOYL AI Dependencies Checker
Checks if all required dependencies are available and provides helpful information
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print("   Minimum required: Python 3.8")
        return False

def check_package(package_name, import_name=None, optional=False):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        status = "✅" if not optional else "💚"
        print(f"{status} {package_name}")
        return True
    except ImportError:
        status = "❌" if not optional else "⚠️"
        print(f"{status} {package_name} {'(optional)' if optional else ''}")
        return not optional  # Return True for optional packages

def get_package_version(package_name):
    """Get installed package version"""
    try:
        result = subprocess.run([sys.executable, '-c', f'import {package_name}; print({package_name}.__version__)'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "unknown"

def main():
    """Main dependency checking function"""
    print("🔍 KOYL AI Dependencies Checker")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    print()
    
    # Required packages
    print("📦 Checking required packages:")
    required_packages = [
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('Flask', 'flask'),
        ('Flask-CORS', 'flask_cors'),
        ('scikit-learn', 'sklearn'),
        ('pandas', 'pandas'),
        ('torch', 'torch'),
        ('transformers', 'transformers'),
        ('sentence-transformers', 'sentence_transformers'),
        ('faiss-cpu', 'faiss'),
    ]
    
    required_ok = True
    for package_name, import_name in required_packages:
        if not check_package(package_name, import_name):
            required_ok = False
    
    print()
    
    # Optional packages
    print("🔧 Checking optional packages:")
    optional_packages = [
        ('lxml', 'lxml'),
        ('beautifulsoup4', 'bs4'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('nltk', 'nltk'),
        ('spacy', 'spacy'),
    ]
    
    for package_name, import_name in optional_packages:
        check_package(package_name, import_name, optional=True)
    
    print()
    print("=" * 50)
    
    # Summary
    if python_ok and required_ok:
        print("🎉 All required dependencies are available!")
        print("✅ KOYL AI backend should work properly")
        print()
        print("🚀 Ready to run:")
        print("   • python run_backend.py (start backend server)")
        print("   • python ai_trainer.py (train AI models)")
        return True
    else:
        print("❌ Some required dependencies are missing")
        print()
        print("🔧 To install missing dependencies:")
        print("   • Run: pip install -r requirements.txt")
        print("   • Or run: bash install_dependencies.sh")
        print()
        print("📋 Required packages list:")
        for package_name, _ in required_packages:
            print(f"   • {package_name}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
