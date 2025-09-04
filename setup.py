#!/usr/bin/env python3
"""
Setup script for ATS Resume Optimizer
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("\n# Optional: Set to production for deployment\n")
            f.write("FLASK_ENV=development\n")
        print("✅ .env file created! Please add your OpenAI API key.")
    else:
        print("✅ .env file already exists.")

def create_directories():
    """Create necessary directories"""
    directories = [
        "backend/uploads",
        "backend/logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 Setting up ATS Resume Optimizer...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation.")
        return
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add your OpenAI API key to the .env file")
    print("2. Run: cd backend && python app.py")
    print("3. Open http://127.0.0.1:8000 in your browser")
    print("\n🔑 Get your OpenAI API key from: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()
