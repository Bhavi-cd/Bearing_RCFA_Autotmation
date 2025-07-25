#!/usr/bin/env python3
"""
Setup script for Gemini-based Bearing Fault Analysis
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def check_api_key():
    """Check if Google API key is configured"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"✅ Google API key is configured (length: {len(api_key)})")
        return True
    else:
        print("⚠️  Google API key not found in environment")
        print("   Please set it with: export GOOGLE_API_KEY='your-api-key-here'")
        return False

def create_env_file():
    """Create .env file template"""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Google Generative AI Configuration
GOOGLE_API_KEY=your-api-key-here

# API Configuration (optional)
HOST=0.0.0.0
PORT=8001
DEBUG=true
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("   Please edit it and add your Google API key")
        return True
    else:
        print("✅ .env file already exists")
        return True

def test_imports():
    """Test if all imports work correctly"""
    print("🔧 Testing imports...")
    try:
        import fastapi
        import uvicorn
        import pydantic
        import google.generativeai
        import PIL
        import aiohttp
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 SETTING UP GEMINI-BASED BEARING ANALYSIS")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Import test failed")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Check API key
    api_key_configured = check_api_key()
    
    print("\n🎉 SETUP COMPLETED!")
    print("="*60)
    
    if api_key_configured:
        print("✅ Ready to use! You can now:")
        print("   1. Start the server: python -m app.main")
        print("   2. Test analysis: python test_gemini_analysis.py")
        print("   3. Use API client: python gemini_client.py")
    else:
        print("⚠️  Almost ready! Please:")
        print("   1. Set your Google API key: export GOOGLE_API_KEY='your-key'")
        print("   2. Then start the server: python -m app.main")
    
    print("\n📚 For more information, see README_GEMINI.md")

if __name__ == "__main__":
    main() 
