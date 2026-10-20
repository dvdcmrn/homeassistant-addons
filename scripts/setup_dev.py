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
    print(f"Running: {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"OK: {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAIL: {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def setup_virtual_environment():
    """Set up a Python virtual environment."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("Virtual environment already exists")
        return True

    print("Creating virtual environment...")
    try:
        venv.create("venv", with_pip=True)
        print("OK: Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"FAIL: Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install project dependencies."""
    if os.name == "nt":
        pip_cmd = "venv\\Scripts\\pip"
    else:
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
    """Icons are not shipped. HA creates an empty www/cupertino-icons/ at runtime."""
    print(
        "No sample icons are created. Export SVGs from SF Symbols into www/cupertino-icons/"
    )
    return True


def setup_git_hooks():
    """Set up Git hooks for code quality."""
    hooks_dir = Path(".git/hooks")
    if not hooks_dir.exists():
        print(
            "WARN: Git hooks directory not found. Make sure this is a Git repository."
        )
        return

    pre_commit_hook = hooks_dir / "pre-commit"
    pre_commit_content = """#!/bin/sh
# Pre-commit hook for code quality checks

echo "Running code quality checks..."

python -m black --check --diff . || {
    echo "FAIL: Code formatting check failed. Run 'black .' to fix."
    exit 1
}

python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 || {
    echo "FAIL: Linting check failed. Fix the issues above."
    exit 1
}

echo "OK: Code quality checks passed"
"""

    pre_commit_hook.write_text(pre_commit_content)
    pre_commit_hook.chmod(0o755)
    print("OK: Git pre-commit hook installed")


def main():
    """Main setup function."""
    print("Setting up Cupertino Icons development environment")
    print("=" * 70)

    if not Path("custom_components/cupertino_icons").exists():
        print("FAIL: Please run this script from the project root directory")
        sys.exit(1)

    steps = [
        ("Setting up virtual environment", setup_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Skipping bundled icons", create_sample_icons),
        ("Setting up Git hooks", setup_git_hooks),
    ]

    for step_name, step_func in steps:
        print(f"\nStep: {step_name}")
        print("-" * 40)
        if not step_func():
            print(f"FAIL: Setup failed at: {step_name}")
            sys.exit(1)

    print("\nDevelopment environment setup complete.")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    if os.name == "nt":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run tests: python -m pytest tests/")
    print("3. Format code: black .")
    print("4. Lint code: flake8 .")
    print("5. Start developing!")


if __name__ == "__main__":
    main()
