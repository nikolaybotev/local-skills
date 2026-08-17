#!/usr/bin/env python3
"""Shared paths and CDP settings. Override with BRAVE_PATH / BRAVE_DEBUG_PORT."""

import errno
import json
import os
import sys
import urllib.error
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(SKILL_DIR, ".cache")
USER_DATA_DIR = os.path.join(CACHE_DIR, "brave-user-data")
LAUNCH_LOG = os.path.join(CACHE_DIR, "brave-launch.log")

DEBUG_PORT = int(os.environ.get("BRAVE_DEBUG_PORT", "9322"))
CDP_HTTP = f"http://127.0.0.1:{DEBUG_PORT}"

EXIT_OK = 0
EXIT_ACTION = 1
EXIT_SESSION_DEAD = 2
PROBE_TIMEOUT = 1.0


def default_brave_path():
    if sys.platform == "darwin":
        return "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    if sys.platform.startswith("linux"):
        for path in (
            "/usr/bin/brave-browser",
            "/usr/bin/brave-browser-stable",
            "/usr/bin/brave",
        ):
            if os.path.isfile(path):
                return path
        return "/usr/bin/brave-browser"
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA", "")
        return os.path.join(
            local,
            "BraveSoftware",
            "Brave-Browser",
            "Application",
            "brave.exe",
        )
    return "brave"


BRAVE_PATH = os.environ.get("BRAVE_PATH") or default_brave_path()


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
