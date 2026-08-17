#!/usr/bin/env python3
"""Attach to the existing CDP session. Never launches. Never closes the browser.

Tab model: pages[0] is the main working tab. Extra pages are transient popups
(site pickers, window.open). Verbs default to main. --popup acts on the newest
extra page. Never create tabs. Never rewrite target=_blank.
"""

import sys
import time

from config import CDP_HTTP, EXIT_ACTION, EXIT_SESSION_DEAD

SKIP_URL_PREFIXES = ("chrome-extension://", "devtools://")


def die_session(message, exc=None):
    if exc is not None:
        print(f"SESSION_DEAD: {message}: {exc}", file=sys.stderr)
    else:
        print(f"SESSION_DEAD: {message}", file=sys.stderr)
    sys.exit(EXIT_SESSION_DEAD)


def die_action(message, exc=None):
    if exc is not None:
        print(f"FAIL: {message}: {exc}", file=sys.stderr)
    else:
        print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(EXIT_ACTION)


def listed_pages(browser):
    """Normal pages in creation order. Index 0 is main; the rest are popups."""
    pages = []
    for context in browser.contexts:
        for page in context.pages:
            url = page.url or ""
            if url.startswith(SKIP_URL_PREFIXES):
                continue
            pages.append(page)
    return pages


def main_page(browser):
    pages = listed_pages(browser)
    if not pages:
        for context in browser.contexts:
            pages.extend(context.pages)
    if not pages:
        die_session("browser has no open pages")
    return pages[0]


def popup_page(browser):
    pages = listed_pages(browser)
    if len(pages) < 2:
        die_action("no popup tab; only main tab[0] is open")
    return pages[-1]


def connect_browser(playwright):
    """Return a CDP browser. Exits 2 if the session is gone. Does not close the browser."""
    try:
        browser = playwright.chromium.connect_over_cdp(CDP_HTTP)
    except Exception as exc:
        die_session(f"CDP connect to {CDP_HTTP} failed", exc)

    # Known CDP race: contexts/pages can be empty for a moment after attach.
    deadline = time.time() + 2
    logged = False
    while not browser.contexts or not listed_pages(browser):
        if time.time() >= deadline:
            break
        if not logged:
            print("CDP connected, waiting for pages", file=sys.stderr)
            logged = True
        time.sleep(0.1)

    if not browser.contexts:
        die_session("CDP connected but browser has no contexts")

    return browser


def connect_page(playwright, popup=False):
    """Return (browser, page) for main or the newest popup. Does not close the browser."""
    browser = connect_browser(playwright)
    page = popup_page(browser) if popup else main_page(browser)
    return browser, page
