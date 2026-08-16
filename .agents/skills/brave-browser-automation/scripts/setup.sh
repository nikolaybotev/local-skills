#!/usr/bin/env bash
# One-time setup: creates a venv, installs dependencies, and downloads Playwright browsers.
# Run this once when cloning or setting up on a new machine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$ROOT_DIR/.venv"

echo "=== Brave Browser Automation Skill Setup ==="

# Check for Python 3.14
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.14 via mise (see mise.toml) or Homebrew."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYTHON_VERSION" != "3.14" ]]; then
    echo "WARNING: Python $PYTHON_VERSION detected. This skill requires Python 3.14."
    echo "Use 'mise use python@3.14' to select the correct version."
fi

# Create venv if it doesn't exist
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing dependencies ..."
pip install -r "$ROOT_DIR/requirements.txt"

# Install Playwright browsers
echo "Installing Playwright browsers ..."
playwright install chromium
playwright install-deps chromium

echo ""
echo "=== Setup complete! ==="
echo "The skill is ready to use."
echo "Python venv: $VENV_DIR"
echo "Playwright browsers: installed"
