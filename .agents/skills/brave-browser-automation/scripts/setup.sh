#!/usr/bin/env bash
# Create the skill venv on first use; reuse it when Playwright is already importable.
# Does not download Playwright's Chromium — this skill drives system Brave over CDP.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$ROOT_DIR/.venv"
VENV_PY="$VENV_DIR/bin/python"

echo "=== Brave Browser Automation Skill Setup ==="

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.14 via mise (see mise.toml) or Homebrew."
    exit 1
fi

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$PYTHON_VERSION" != "3.14" ]]; then
    echo "WARNING: Python $PYTHON_VERSION detected. This skill expects Python 3.14."
    echo "Use 'mise use python@3.14' to select the correct version."
fi

if [[ -x "$VENV_PY" ]] && "$VENV_PY" -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "Already set up: $VENV_PY"
    exit 0
fi

if [[ ! -x "$VENV_PY" ]]; then
    echo "Creating virtual environment at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi

echo "Installing dependencies ..."
"$VENV_PY" -m pip install -r "$ROOT_DIR/requirements.txt"

if ! "$VENV_PY" -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "ERROR: playwright did not import after install."
    exit 1
fi

echo ""
echo "=== Setup complete ==="
echo "Python: $VENV_PY"
echo "This skill uses system Brave over CDP; Playwright's Chromium is not installed."
