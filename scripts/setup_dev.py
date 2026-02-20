#!/usr/bin/env python3
"""
Development setup script for SF Symbols Home Assistant integration.
This script helps set up the development environment.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def setup_virtual_environment():
    """Set up a Python virtual environment."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    print("🐍 Creating virtual environment...")
    try:
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install project dependencies."""
    # Determine the pip command based on the platform
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -r requirements.txt", "Installing dependencies"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    return True


def create_sample_icons():
    """Create sample SVG icons for testing."""
    icons_dir = Path("www/dvdcmrn_icons/icons")
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    sample_icons = {
        "house.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M12 2L2 12h3v8h6v-6h2v6h6v-8h3L12 2z"/>
</svg>''',
        "heart.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
</svg>''',
        "star.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>'''
    }
    
    for filename, content in sample_icons.items():
        icon_path = icons_dir / filename
        if not icon_path.exists():
            icon_path.write_text(content)
            print(f"✅ Created sample icon: {filename}")
    
    print(f"📁 Sample icons created in {icons_dir}")


def setup_git_hooks():
    """Set up Git hooks for code quality."""
    hooks_dir = Path(".git/hooks")
    if not hooks_dir.exists():
        print("⚠️  Git hooks directory not found. Make sure this is a Git repository.")
        return
    
    pre_commit_hook = hooks_dir / "pre-commit"
    pre_commit_content = '''#!/bin/sh
# Pre-commit hook for code quality checks

echo "Running code quality checks..."

# Run black formatting check
python -m black --check --diff . || {
    echo "❌ Code formatting check failed. Run 'black .' to fix."
    exit 1
}

# Run flake8 linting
python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 || {
    echo "❌ Linting check failed. Fix the issues above."
    exit 1
}

echo "✅ Code quality checks passed"
'''

    pre_commit_hook.write_text(pre_commit_content)
    pre_commit_hook.chmod(0o755)
    print("✅ Git pre-commit hook installed")


def main():
    """Main setup function."""
    print("Setting up dvdcmrn Home Assistant Icons development environment")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not Path("custom_components/dvdcmrn_icons").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    steps = [
        ("Setting up virtual environment", setup_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Creating sample icons", create_sample_icons),
        ("Setting up Git hooks", setup_git_hooks),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        print("-" * 40)
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n🎉 Development environment setup complete!")
    print("\n📝 Next steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("2. Run tests: python -m pytest tests/")
    print("3. Format code: black .")
    print("4. Lint code: flake8 .")
    print("5. Start developing!")


if __name__ == "__main__":
    main() 