---
name: brave-browser-automation
description: Automate Brave browser via Playwright CDP connection. Launch once, reconnect across multiple steps, keep browser alive.
---

## Brave Browser Automation via Playwright CDP

When the user needs to interact with a website through a visible Brave browser instance, use this pattern. The key principle: **launch Brave once in the background, then reconnect to it on every subsequent step**. Never use `browser.close()` until the user is done.

### Step 1 — Launch Brave in the background

```python
import subprocess, json, time, urllib.request
from playwright.sync_api import sync_playwright

USER_DATA_DIR = "/tmp/playwright-brave-persistent"

# Launch Brave with remote debugging
proc = subprocess.Popen([
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "--remote-debugging-port=9322",
    "--user-data-dir=" + USER_DATA_DIR,
    "--no-first-run",
    "--no-default-browser-check",
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Wait for it to start
time.sleep(5)

# Get the WebSocket URL
resp = urllib.request.urlopen("http://localhost:9322/json/version")
data = json.loads(resp.read())
ws_url = data["webSocketDebuggerUrl"]
print(ws_url)  # Save this for subsequent steps
```

### Step 2+ — Connect to the running Brave

On every subsequent invocation, **connect to the already-running Brave** (do NOT launch a new one):

```python
import json, time
from playwright.sync_api import sync_playwright

# Load the saved WebSocket URL
with open("/tmp/brave_session_info.json") as f:
    info = json.load(f)
ws_url = info["ws_endpoint"]

with sync_playwright() as p:
    # Connect to the running Brave instance
    browser = p.chromium.connect_over_cdp(ws_url)
    time.sleep(1)  # ← CRITICAL: let the CDP connection settle
    
    context = browser.contexts[0]  # Get the default context
    page = context.pages[0]        # Get the first page/tab
    
    # Now interact with the page
    page.goto("https://example.com")
    time.sleep(2)
    # ... do your work ...
    
    # Do NOT call browser.close() — Brave stays alive for the next step!
```

### Key rules

1. **Never call `browser.close()`** while the user is still working. Only close when the session is truly done.
2. **Always add `time.sleep(1)` after `connect_over_cdp()`** — `browser.contexts` is `None` immediately after connecting.
3. **Save the WebSocket URL** to `/tmp/brave_session_info.json` so subsequent steps can reconnect.
4. **Use the same `--user-data-dir`** every time to persist cookies, extensions, and session state.
5. If Brave is already running (check with `ps aux | grep Brave`), skip the launch step and just connect.
6. The `contexts[0]` approach works because connecting over CDP gives you access to the existing browser context.

### Checking if Brave is already running

```bash
ps aux | grep "Brave Browser" | grep -v grep | head -1
```

If Brave is running, grab the existing WebSocket URL:

```bash
curl -s http://localhost:9322/json/version | python3 -m json.tool
```

### Common pitfalls

- `browser.contexts` is `None` right after `connect_over_cdp()` — always `time.sleep(1)` first
- The WebSocket URL from `/json/version` is the correct endpoint (not `/devtools/browser/default`)
- If port 9322 is in use, pick a different port (e.g., 9323)
- Do not mix `launch_persistent_context()` with `connect_over_cdp()` — use one or the other
