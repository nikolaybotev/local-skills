#!/usr/bin/env python3
"""Shared paths, CDP settings, and the chosen Chromium-family engine.

Override the binary with BROWSER_PATH and the debug port with CDP_PORT.
"""

import errno
import json
import os
import sys
import urllib.error
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(SKILL_DIR, ".cache")
USER_DATA_DIR = os.path.join(CACHE_DIR, "user-data")
LAUNCH_LOG = os.path.join(CACHE_DIR, "browser-launch.log")
BROWSER_FILE = os.path.join(CACHE_DIR, "browser.json")

DEBUG_PORT = int(os.environ.get("CDP_PORT", "9322"))
CDP_HTTP = f"http://127.0.0.1:{DEBUG_PORT}"

EXIT_OK = 0
EXIT_ACTION = 1
EXIT_SESSION_DEAD = 2
PROBE_TIMEOUT = 1.0

BROWSER_IDS = ("chrome", "chromium", "brave", "edge", "playwright-chromium")

CONFIGURE_HINT = """\
Ask the user to choose one engine (all over CDP, dedicated profile, not their daily browser):
  chrome | chromium | brave | edge | playwright-chromium
Then run:
  "$PY" "$SKILL_DIR/scripts/configure_browser.py" <id>
"""


def _first_file(paths):
    for path in paths:
        if path and os.path.isfile(path):
            return path
    return None


def system_browser_candidates(browser_id):
    """Possible executable paths for a system browser, in preference order."""
    if sys.platform == "darwin":
        apps = {
            "chrome": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
            "chromium": ["/Applications/Chromium.app/Contents/MacOS/Chromium"],
            "brave": ["/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"],
            "edge": ["/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"],
        }
        return list(apps.get(browser_id, []))

    if sys.platform.startswith("linux"):
        linux = {
            "chrome": ["/usr/bin/google-chrome-stable", "/usr/bin/google-chrome"],
            "chromium": ["/usr/bin/chromium", "/usr/bin/chromium-browser"],
            "brave": [
                "/usr/bin/brave-browser",
                "/usr/bin/brave-browser-stable",
                "/usr/bin/brave",
            ],
            "edge": ["/usr/bin/microsoft-edge-stable", "/usr/bin/microsoft-edge"],
        }
        return list(linux.get(browser_id, []))

    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA", "")
        pf = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        pf86 = os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")
        windows = {
            "chrome": [
                os.path.join(local, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(pf, "Google", "Chrome", "Application", "chrome.exe"),
            ],
            "chromium": [
                os.path.join(local, "Chromium", "Application", "chrome.exe"),
            ],
            "brave": [
                os.path.join(
                    local,
                    "BraveSoftware",
                    "Brave-Browser",
                    "Application",
                    "brave.exe",
                ),
            ],
            "edge": [
                os.path.join(pf86, "Microsoft", "Edge", "Application", "msedge.exe"),
                os.path.join(pf, "Microsoft", "Edge", "Application", "msedge.exe"),
            ],
        }
        return list(windows.get(browser_id, []))

    return []


def resolve_system_browser(browser_id):
    return _first_file(system_browser_candidates(browser_id))


def playwright_chromium_path():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        return p.chromium.executable_path


def read_browser_file():
    if not os.path.isfile(BROWSER_FILE):
        return None
    with open(BROWSER_FILE, encoding="utf-8") as f:
        data = json.load(f)
    browser_id = data.get("id")
    path = data.get("path")
    if not browser_id or not path:
        return None
    return {"id": browser_id, "path": path}


def write_browser_file(browser_id, path):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(BROWSER_FILE, "w", encoding="utf-8") as f:
        json.dump({"id": browser_id, "path": path}, f, indent=2)
        f.write("\n")


def browser_config():
    """Return {id, path} from env and/or browser.json, or None if unset."""
    saved = read_browser_file()
    env_path = os.environ.get("BROWSER_PATH")
    if env_path:
        return {
            "id": saved["id"] if saved else "custom",
            "path": env_path,
        }
    return saved


def require_browser_config():
    cfg = browser_config()
    if cfg is None:
        print("FAIL: no browser configured.", file=sys.stderr)
        print(CONFIGURE_HINT, file=sys.stderr)
        sys.exit(EXIT_ACTION)
    return cfg


def is_connection_refused(exc):
    if isinstance(exc, ConnectionRefusedError):
        return True
    if isinstance(exc, urllib.error.URLError) and exc.reason is not None:
        return is_connection_refused(exc.reason)
    if isinstance(exc, OSError):
        return exc.errno == errno.ECONNREFUSED
    return False


def fetch_json(path, timeout=PROBE_TIMEOUT):
    url = f"{CDP_HTTP}{path}"
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def probe_version():
    """Return /json/version dict, or None if nothing is listening."""
    try:
        return fetch_json("/json/version")
    except urllib.error.URLError as exc:
        if is_connection_refused(exc):
            return None
        raise
