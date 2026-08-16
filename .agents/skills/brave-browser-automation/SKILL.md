---
name: brave-browser-automation
description: Automate Brave browser via Playwright CDP connection. Use this skill whenever the user wants to automate a browser, control Brave/Chrome/Chromium programmatically, keep a browser session alive across multiple steps, or interact with websites through a persistent browser instance. Trigger when the user mentions Playwright, browser automation, CDP, remote debugging, persistent browser sessions, or wants to control a browser from code. Also trigger for web scraping, testing, or any browser control task that needs to span multiple script invocations. If the user mentions "browser", "automation", "Playwright", "CDP", "remote debugging", or "persistent session" in the context of web interaction, use this skill.
---

## Brave Browser Automation via Playwright CDP

When the user needs to interact with a website through a visible Brave (or Chromium-based) browser instance, use this pattern. The key principle: **launch Brave once in the background, then reconnect to it on every subsequent step**. Never use `browser.close()` until the user is done.

### Setup (one-time, run once per machine)

Before using this skill, ensure dependencies are installed:

```bash
cd <skill-dir>   # Path to this skill's directory
bash scripts/setup.sh
```

This creates a `.venv` with Playwright and installs Chromium browsers. All subsequent Python code should run inside this venv:

```bash
source .venv/bin/activate
python3 your_script.py
```

### Step 0 — Load or Launch (run once at the start of work)

**Run this ONCE when starting a browser automation task.** It checks if a session is alive and reconnects or launches as needed. Do NOT call this on every click/fill — it takes ~1.5 seconds due to the CDP handshake overhead.

```python
import subprocess, json, time, urllib.request, os
from playwright.sync_api import sync_playwright

USER_DATA_DIR = "/tmp/playwright-brave-persistent"
SESSION_FILE = "./.cache/session.json"

def load_or_launch():
    """Check for existing Brave session; launch if none found or session is dead.
    Run ONCE at the start of work. Reuse the returned page for all subsequent actions."""
    
    # Check if a session file exists
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            info = json.load(f)
        ws_url = info["ws_endpoint"]
        
        # Try to connect and verify the browser is responsive
        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(ws_url)
                time.sleep(1)  # Let CDP settle
                
                if browser.contexts and browser.contexts[0].pages:
                    page = browser.contexts[0].pages[0]
                    _ = page.url  # Quick ping
                    return browser, page, True  # reused=True
                else:
                    browser.close()
            except Exception:
                pass
    
    # Launch a new Brave session
    proc = subprocess.Popen([
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "--remote-debugging-port=9322",
        "--user-data-dir=" + USER_DATA_DIR,
        "--no-first-run",
        "--no-default-browser-check",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(5)
    
    resp = urllib.request.urlopen("http://localhost:9322/json/version")
    data = json.loads(resp.read())
    ws_url = data["webSocketDebuggerUrl"]
    
    # Save session info for future steps
    session_info = {"ws_endpoint": ws_url}
    with open(SESSION_FILE, "w") as f:
        json.dump(session_info, f)
    
    # Connect and return
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url)
        time.sleep(1)
        context = browser.contexts[0]
        page = context.new_page()
        return browser, page, False  # reused=False

# === Usage ===
# browser, page, reused = load_or_launch()
# if reused:
#     print("Reconnected to existing session")
# else:
#     print("Launched new session")
# # Now use 'page' for all actions — no need to call load_or_launch again
```

### Step 1+ — Interact with the page

Use the `page` object returned from `load_or_launch()` for all actions. No need to reconnect:

```python
# All actions use the same 'page' object
page.goto("https://example.com")
time.sleep(2)
page.click("button#submit")
time.sleep(1)
content = page.inner_text("#result")
# ... etc
```

### Key rules

1. **Never call `browser.close()`** while the user is still working. Only close when the session is truly done.
2. **Call `load_or_launch()` ONCE at the start of a task** — it returns a `page` object to reuse for all subsequent actions. Do NOT call it on every click/fill.
3. **Use the same `--user-data-dir`** every time to persist cookies, extensions, and session state.
4. The `contexts[0]` approach works because connecting over CDP gives you access to the existing browser context.

### When the user is done

Only when the user explicitly says they're done with browser automation:

```python
browser.close()
os.remove("/tmp/brave_session_info.json")  # Clean up session file
print("Brave closed. Session ended.")
```

### Cross-platform notes

- **macOS**: `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`
- **Windows**: `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe`
- **Linux**: `/usr/bin/brave-browser` (or `brave` depending on installation)

### Troubleshooting

- **Connection refused**: Brave may have crashed. Kill all Brave processes (`killall Brave Browser`) and restart.
- **Port conflict**: If 9322 is busy, try `--remote-debugging-port=9323` and update the URL accordingly.
- **CDP disconnect**: If the connection drops, call `load_or_launch()` again — it will detect the dead session and start fresh.

### Common pitfalls

- `browser.contexts` is `None` right after `connect_over_cdp()` — always `time.sleep(1)` first
- The WebSocket URL from `/json/version` is the correct endpoint (not `/devtools/browser/default`)
- If port 9322 is in use, pick a different port (e.g., 9323)
- Do not mix `launch_persistent_context()` with `connect_over_cdp()` — use one or the other