#!/usr/bin/env bash
# Create the skill venv on first use; reuse it when Playwright is already importable.
# Requires Python 3.14 from PATH (mise, Homebrew, python.org, …).
# Playwright's Chromium binary is installed only if the user picks that engine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$ROOT_DIR/.venv"
VENV_PY="$VENV_DIR/bin/python"

echo "=== Chromium Browser Automation Skill Setup ==="

python_minor() {
    local exe="$1"
    "$exe" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null
}

is_python_314() {
    local exe="$1"
    [[ "$(python_minor "$exe")" == "3.14" ]]
}

find_python_314() {
    local seen="" exe
    for exe in python3.14 python3; do
        if ! command -v "$exe" &>/dev/null; then
            continue
        fi
        exe="$(command -v "$exe")"
        if [[ " $seen " == *" $exe "* ]]; then
            continue
        fi
        seen+=" $exe"
        if is_python_314 "$exe"; then
            printf '%s\n' "$exe"
            return 0
        fi
    done
    return 1
}

print_python_314_hint() {
    echo "ERROR: Python 3.14 is required and was not found on PATH."
    echo "Looked for python3.14, then python3 that reports 3.14.x. Other versions are not used."
    if command -v mise &>/dev/null && [[ -f "$ROOT_DIR/mise.toml" ]]; then
        echo "This skill directory has a mise.toml. Install 3.14, then re-run setup:"
        echo "  cd \"$ROOT_DIR\" && mise install"
    else
        echo "Install Python 3.14 (mise is one way: https://mise.jdx.dev), then re-run setup."
    fi
}

HOST_PY="$(find_python_314)" || {
    print_python_314_hint
    exit 1
}
echo "Host Python 3.14: $HOST_PY ($("$HOST_PY" -c 'import sys; print(sys.version.split()[0])'))"

venv_python_ok() {
    [[ -e "$VENV_PY" ]] || return 1
    is_python_314 "$VENV_PY"
}

if [[ -e "$VENV_DIR" ]] && ! venv_python_ok; then
    echo "Existing venv is unusable (broken interpreter or not 3.14). Recreating ..."
    rm -rf "$VENV_DIR"
fi

if venv_python_ok && "$VENV_PY" -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "Already set up: $VENV_PY"
    exit 0
fi

if [[ ! -e "$VENV_PY" ]]; then
    echo "Creating virtual environment at $VENV_DIR ..."
    "$HOST_PY" -m venv "$VENV_DIR"
fi

if ! venv_python_ok; then
    echo "ERROR: venv python is not 3.14 after create: $VENV_PY"
    exit 1
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
echo "Next: ask the user which engine to use, then run scripts/configure_browser.py"
