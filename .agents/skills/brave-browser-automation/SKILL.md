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
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from load_or_launch import load_or_launch

browser, page, reused = load_or_launch()
if reused:
    print("Reconnected to existing session")
else:
    print("Launched new session")
# Now use 'page' for all actions — no need to call load_or_launch again
```

The script is at `scripts/load_or_launch.py` in the skill directory. It handles session detection, validation, and recovery automatically.

To customize config (Brave path, debug port, user data dir), edit `scripts/load_or_launch.py` directly — all settings are at the top as module-level constants.

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

### Tips

#### Faster page loads

Use `wait_until='domcontentloaded'` instead of the default `'load'` when navigating to SPAs or pages with heavy assets. It waits for the DOM to be ready but skips waiting for images, stylesheets, and other subresources:

```python
page.goto("https://example.com", wait_until='domcontentloaded')
```

This can shave seconds off navigation time on complex pages.

#### Efficient data extraction

Use `eval_on_selector_all()` to run JavaScript in-page and extract structured data from all matching elements at once, instead of iterating element-by-element:

```python
# Extract all links in one call instead of looping
links = page.eval_on_selector_all('a', 'els => els.map(e => ({href: e.href, text: e.innerText.trim()}))')
for link in links:
    print(link['href'], link['text'])
```

This avoids multiple round-trips between Python and the browser, which adds up with many elements.