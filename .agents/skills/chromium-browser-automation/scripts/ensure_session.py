#!/usr/bin/env python3
"""Ensure the configured browser is listening on the CDP port. Launch only if needed.

Does not return browser handles. Prints a short status block on stdout.
Diagnostics go to stderr.

Exit 0 if a session is ready (reused or launched).
Exit 1 if launch/probe fails, or if no browser has been configured.
Never exits 2 — that code is for work-loop connect failures after init.
"""

import json
import os
import subprocess
import sys
import time
import urllib.error

from config import (
    CACHE_DIR,
    CDP_HTTP,
    DEBUG_PORT,
    EXIT_ACTION,
    EXIT_OK,
    LAUNCH_LOG,
    USER_DATA_DIR,
    fetch_json,
    is_connection_refused,
    probe_version,
    require_browser_config,
)

LAUNCH_WAIT_SECONDS = 30


def tab_lines():
    try:
        targets = fetch_json("/json/list")
    except Exception as exc:
        print(f"warning: could not list tabs: {exc}", file=sys.stderr)
        return []
    lines = []
    for target in targets:
        if target.get("type") != "page":
            continue
        title = (target.get("title") or "").replace("\n", " ")
        url = target.get("url") or ""
        role = "main" if len(lines) == 0 else "popup"
        lines.append(f"  [{len(lines)}] {role} {url}  {title}")
    return lines


def print_status(status, version, cfg):
    ws = version.get("webSocketDebuggerUrl", "")
    lines = tab_lines()
    print(f"status={status}")
    print(f"engine={cfg['id']}")
    print(f"cdp={CDP_HTTP}")
    if ws:
        print(f"ws={ws}")
    print(f"browser={version.get('Browser', '')}")
    print(f"tabs={len(lines)}")
    for line in lines:
        print(line)


def launch_browser(cfg):
    binary = cfg["path"]
    if not os.path.isfile(binary):
        print(
            f"FAIL: browser not found at {binary}. "
            "Re-run configure_browser.py or set BROWSER_PATH.",
            file=sys.stderr,
        )
        sys.exit(EXIT_ACTION)

    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    print(
        f"port {DEBUG_PORT} not responding, launching {cfg['id']}",
        file=sys.stderr,
    )
    print(f"binary={binary}", file=sys.stderr)
    print(f"user-data-dir={USER_DATA_DIR}", file=sys.stderr)
    print(f"launch-log={LAUNCH_LOG}", file=sys.stderr)

    logf = open(LAUNCH_LOG, "ab")
    proc = subprocess.Popen(
        [
            binary,
            f"--remote-debugging-port={DEBUG_PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={USER_DATA_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
        ],
        stdout=logf,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )

    deadline = time.time() + LAUNCH_WAIT_SECONDS
    print(
        f"waiting up to {LAUNCH_WAIT_SECONDS}s for CDP on {CDP_HTTP}",
        file=sys.stderr,
    )
    last_err = None
    while time.time() < deadline:
        try:
            version = fetch_json("/json/version")
            logf.close()
            return version
        except urllib.error.URLError as exc:
            last_err = exc
            if is_connection_refused(exc):
                time.sleep(0.25)
                continue
            logf.close()
            raise
        except json.JSONDecodeError as exc:
            last_err = exc
            time.sleep(0.25)

    logf.close()
    tail = ""
    try:
        with open(LAUNCH_LOG, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 4000))
            tail = f.read().decode("utf-8", errors="replace")
    except OSError:
        pass

    print(
        f"FAIL: {cfg['id']} did not open CDP on {CDP_HTTP} within "
        f"{LAUNCH_WAIT_SECONDS}s (pid={proc.pid}, poll={proc.poll()}): {last_err}",
        file=sys.stderr,
    )
    if tail.strip():
        print("--- launch log (tail) ---", file=sys.stderr)
        print(tail, file=sys.stderr)
    sys.exit(EXIT_ACTION)


def main():
    cfg = require_browser_config()

    try:
        version = probe_version()
    except urllib.error.HTTPError as exc:
        print(f"FAIL: CDP HTTP error from {CDP_HTTP}: {exc}", file=sys.stderr)
        sys.exit(EXIT_ACTION)
    except json.JSONDecodeError as exc:
        print(
            f"FAIL: {CDP_HTTP} is in use but did not return CDP JSON: {exc}",
            file=sys.stderr,
        )
        sys.exit(EXIT_ACTION)
    except Exception as exc:
        print(f"FAIL: unexpected error probing {CDP_HTTP}: {exc}", file=sys.stderr)
        sys.exit(EXIT_ACTION)

    if version is not None:
        print_status("reused", version, cfg)
        sys.exit(EXIT_OK)

    version = launch_browser(cfg)
    print_status("launched", version, cfg)
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
