#!/usr/bin/env python3
"""Load or launch a persistent Brave browser session via Playwright CDP.

Run this ONCE at the start of a browser automation task. It checks if a
session is alive and reconnects or launches as needed. Reuse the returned
page object for all subsequent actions — do NOT call this on every click/fill
(it takes ~1.5s due to CDP handshake overhead).

Usage:
    python3 load_or_launch.py          # prints ws_endpoint to stdout
    python3 -c "from load_or_launch import load_or_launch; ..."
"""

import subprocess
import json
import time
import urllib.request
import os
import sys

# ---------------------------------------------------------------------------
# Config — tweak these if needed
# ---------------------------------------------------------------------------
USER_DATA_DIR = "/tmp/playwright-brave-persistent"
SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache", "session.json")
BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
DEBUG_PORT = 9322


def load_or_launch():
    """Check for existing Brave session; launch if none found or session is dead.

    Returns:
        (browser, page, reused): browser handle, page object, and bool
        indicating whether an existing session was reused.
    """
    # Check if a session file exists
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            info = json.load(f)
        ws_url = info["ws_endpoint"]

        # Try to connect and verify the browser is responsive
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(ws_url)
                time.sleep(1)  # Let CDP settle

                if browser.contexts and browser.contexts[0].pages:
                    page = browser.contexts[0].pages[0]
                    _ = page.url  # Quick ping
                    return browser, page, True  # reused
                else:
                    browser.close()
            except Exception:
                pass

    # Launch a new Brave session
    proc = subprocess.Popen([
        BRAVE_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(5)

    resp = urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json/version")
    data = json.loads(resp.read())
    ws_url = data["webSocketDebuggerUrl"]

    # Save session info for future steps
    session_info = {"ws_endpoint": ws_url}
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump(session_info, f)

    print(f"Launched new Brave session. WebSocket: {ws_url}")

    # Connect and return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url)
        time.sleep(1)
        context = browser.contexts[0]
        page = context.new_page()
        return browser, page, False


if __name__ == "__main__":
    browser, page, reused = load_or_launch()
    if reused:
        print("Reconnected to existing session")
    else:
        print("Launched new session")
    print(f"Page: {page.url}")
    # Keep browser alive — caller should keep the browser handle