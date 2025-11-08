#!/usr/bin/env python
"""
Development setup script for Customer 360 application.
Run this script to set up the development environment.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("Setting up Customer 360 Development Environment")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not Path("venv").exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv venv", "Virtual environment creation"):
            sys.exit(1)
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && "
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate && "
    
    # Install requirements
    if not run_command(f"{activate_cmd}pip install -r requirements.txt", "Installing requirements"):
        sys.exit(1)
    
    # Run migrations
    if not run_command(f"{activate_cmd}python manage.py makemigrations", "Creating migrations"):
        sys.exit(1)
    
    if not run_command(f"{activate_cmd}python manage.py migrate", "Running migrations"):
        sys.exit(1)
    
    # Create superuser (optional)
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nTo start the development server:")
    if os.name == 'nt':
        print("1. venv\\Scripts\\activate")
    else:
        print("1. source venv/bin/activate")
    print("2. python manage.py runserver")
    print("\nTo create a superuser:")
    print("python manage.py createsuperuser")

if __name__ == "__main__":
    main()