---
name: brave-browser-automation
description: Drive a visible Brave browser that stays open across steps. Use whenever the user wants to interact with a live website in a real window — click, fill forms, scrape, log in, or keep a browser session alive. Also applies to Chrome/Chromium when they want the same persistent visible-browser workflow. Do not use for writing Playwright/Cypress test files, headless CI tests, or general programming questions about those frameworks.
---

# Brave Browser Automation

Brave is long-lived. Python is short-lived. After init, every action is one shell command that connects, does one thing, prints a result, and exits.

Do not write multi-step Playwright scripts. Do not keep a `page` object across steps. Do not relaunch the browser if a later command fails to connect.

## Procedure

`SKILL_DIR` is the directory that contains this `SKILL.md`. `PY` is `$SKILL_DIR/.venv/bin/python`. Always call `$PY` — do not `source` the venv.

### 1. Setup (on demand)

```bash
bash "$SKILL_DIR/scripts/setup.sh"
```

Creates `.venv` and installs Playwright’s Python package if needed. Reuses the venv when `import playwright` already works. Does not download Playwright’s Chromium; this skill drives system Brave.

### 2. Ensure session (on demand)

```bash
"$PY" "$SKILL_DIR/scripts/ensure_session.py"
```

Probes `http://127.0.0.1:9322`. Reuses Brave if it is already listening; launches only if the port is not responding. Prints `status=reused` or `status=launched`, the CDP URL, and open tabs.

If this command fails (exit 1), stop and tell the user. Do not continue to work commands.

### 3. Snapshot, then work

```bash
"$PY" "$SKILL_DIR/scripts/do.py" snapshot
```

Then run **one verb per command**. Read stdout. Check the exit code before the next command.

```bash
"$PY" "$SKILL_DIR/scripts/do.py" goto "https://example.com"
"$PY" "$SKILL_DIR/scripts/do.py" click "text=More information"
"$PY" "$SKILL_DIR/scripts/do.py" fill "#email" "user@host"
"$PY" "$SKILL_DIR/scripts/do.py" text "h1"
"$PY" "$SKILL_DIR/scripts/do.py" screenshot
```

Run `"$PY" "$SKILL_DIR/scripts/do.py" --help` to list verbs.

## Exit codes

| Code | Meaning | What to do |
|------|---------|------------|
| 0 | Success | Read stdout (`OK url=...`) and continue |
| 1 | Action failed (bad selector, timeout, usage) | Session is still assumed live. Try a different selector or verb. Do not relaunch Brave |
| 2 | `SESSION_DEAD` — CDP connect failed | **Stop.** Report progress so far and the stderr error to the user. Do not relaunch, retry connect, or call `ensure_session.py` unless the user asks to start again |

`ensure_session.py` and `setup.sh` only use 0 / 1. Exit 2 is reserved for a dead session during work.

## Verbs

Each invocation attaches over CDP, acts on **main tab[0]** unless `--popup` is passed, prints `OK url=`, `title=`, `target=`, and `extra_tabs=`, then disconnects. It never calls `browser.close()`. It never opens a tab.

| Verb | Args | Notes |
|------|------|--------|
| `snapshot` | | URL, title, tab roles, visible body text (truncated) |
| `goto` | URL | Navigates the **current target** in place. Prefer this over a new tab |
| `click` | SELECTOR | CSS or Playwright selectors (`text=Submit`, `#id`) |
| `fill` | SELECTOR VALUE | Clears, then fills |
| `text` | SELECTOR | Prints `text=...` |
| `screenshot` | [PATH] | Default `$SKILL_DIR/.cache/screenshot.png`. `--full-page` allowed |
| `press` | KEY | e.g. `Enter`, `Meta+a` |
| `wait` | SELECTOR | Until it appears (default 15s timeout) |
| `eval` | JS... | One expression in the page; prints `result=...` |
| `close-popup` | | Close every tab except main tab[0]. Then continue **without** `--popup` |

`--popup` before the verb acts on the newest extra tab (a site picker or `window.open`). If no extra tab exists, exit 1 with `FAIL: no popup tab`.

Default action timeout is 15s (`--timeout` milliseconds before the verb). Prefer Playwright auto-wait over `sleep`.

One action means one of the rows above. Login, submitting a whole form, pagination, and retry loops are sequences of commands — not one script.

## One main tab, optional popup

This browser is dedicated to the task. **Tab[0] is home.** Do not open tabs (`window.open`, `new_page`, “open in new tab”). Need another URL → `goto` on main.

Sites may still open a popup (dropdown search, OAuth, `target=_blank`). That is a **temporary overlay**, not a second workspace:

1. A command on main prints `extra_tabs=1` and `popup_url=...`.
2. Use `--popup` for the picker (snapshot / click / fill / text).
3. If the site does not close it, `close-popup`.
4. Drop `--popup` and finish the task on main. Check `extra_tabs=0`.

```bash
"$PY" "$SKILL_DIR/scripts/do.py" click "#search-place"
# stdout includes extra_tabs=1 and popup_url=...
"$PY" "$SKILL_DIR/scripts/do.py" --popup snapshot
"$PY" "$SKILL_DIR/scripts/do.py" --popup fill "#q" "Sofia"
"$PY" "$SKILL_DIR/scripts/do.py" --popup click "text=Sofia, Bulgaria"
"$PY" "$SKILL_DIR/scripts/do.py" close-popup   # skip if extra_tabs=0 already
"$PY" "$SKILL_DIR/scripts/do.py" click "button[type=submit]"
```

Do not treat extra tabs as a list to browse. There is no `tab INDEX` switch. If `extra_tabs>1`, `--popup` is the newest extra; `close-popup` closes all extras and returns to main.

If you (the human) accidentally opened a tab, that is drift: `close-popup` or fix the window and ask the agent to resume. If you closed the original tab, the oldest remaining page becomes the new tab[0] — fix the window if that is wrong, then resume.

## Fail-fast after init

If `do.py` prints `SESSION_DEAD:` and exits 2, the user probably closed Brave or it crashed. Do not recover:

1. Stop issuing browser commands.
2. Tell the user what already succeeded.
3. Quote the error.
4. Ask whether to run setup + `ensure_session.py` again. That is a new init, not a retry inside the work loop.

Selector/timeout failures are exit 1. Keep going with another verb if that still makes sense.

Do not swallow exceptions in custom code. The CLIs already print the error and set the exit code.

## When the user is done

Leave Brave open unless they explicitly ask to close it.

```bash
"$PY" "$SKILL_DIR/scripts/stop.py"
```

This only signals the process that has this skill’s `--user-data-dir` and debug port. It does not `killall` Brave.

## Escape hatch

Only if no verb can express the action, write a **one-action** script that imports `connect_page`, does one thing, prints a result, and exits. Do not launch Brave. Do not call `browser.close()`. Do not catch a connect failure and retry — let it hit `SESSION_DEAD` (exit 2).

```bash
cd "$SKILL_DIR"
PYTHONPATH=scripts "$PY" /tmp/one_action.py
```

```python
from playwright.sync_api import sync_playwright
from connect import connect_page

with sync_playwright() as p:
    browser, page = connect_page(p)
    page.set_default_timeout(15000)
    # one action only, then print
    print(f"OK url={page.url}")
```

## Config

| Variable | Default |
|----------|---------|
| `BRAVE_PATH` | macOS `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser` |
| `BRAVE_DEBUG_PORT` | `9322` |

User data lives in `$SKILL_DIR/.cache/brave-user-data` so cookies persist without touching the user’s personal profile.

## Do not

- Call `ensure_session.py` again after a work-loop `SESSION_DEAD` unless the user asked to restart
- Write a script that clicks, fills, and navigates in one process
- Use `time.sleep` loops or `while True` to wait for the page
- Mix `launch_persistent_context()` with this CDP session
- Close the browser at the end of a verb
- Open a new tab (`window.open`, `new_page`, “open in new tab”) — `goto` on main instead
- Keep working with `--popup` after the picker is done — close extras and return to tab[0]
- Rewrite `target=_blank` to `_self`; that can break picker popups. Use `--popup` instead
