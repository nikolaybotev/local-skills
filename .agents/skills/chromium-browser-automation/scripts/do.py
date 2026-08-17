#!/usr/bin/env python3
"""One-action CLI against the existing CDP session. Never launches. Never closes the browser.

Default target is main tab[0]. Pass --popup to act on the newest extra tab
(site picker / window.open), then close-popup and continue on main.

Exit 0 on success, 1 if the action failed, 2 if the CDP session is dead.
"""

import argparse
import os
import sys
import textwrap

from config import CACHE_DIR, EXIT_ACTION, EXIT_OK
from connect import (
    connect_browser,
    die_action,
    listed_pages,
    main_page,
    popup_page,
)

VISIBLE_TEXT_LIMIT = 8000


def load_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        die_action("playwright is not installed. Run: bash scripts/setup.sh")
    return sync_playwright


def tab_status(page, target):
    browser = page.context.browser
    pages = listed_pages(browser) if browser is not None else [page]
    extra = pages[1:]
    lines = [
        f"target={target}",
        f"tabs={len(pages)}",
        f"extra_tabs={len(extra)}",
    ]
    if extra:
        popup = extra[-1]
        lines.append(f"popup_url={popup.url}")
        try:
            lines.append(f"popup_title={popup.title()}")
        except Exception as exc:
            lines.append(f"popup_title=(unavailable: {exc})")
    for i, p in enumerate(pages):
        role = "main" if i == 0 else "popup"
        mark = "*" if p == page else " "
        try:
            title = (p.title() or "").replace("\n", " ")
        except Exception:
            title = ""
        lines.append(f"  [{i}] {mark} {role} {p.url}  {title}")
    return lines


def ok(page, target, extra_lines=None):
    print(f"OK url={page.url}")
    try:
        print(f"title={page.title()}")
    except Exception as exc:
        print(f"title=(unavailable: {exc})")
    for line in tab_status(page, target):
        print(line)
    if extra_lines:
        for line in extra_lines:
            print(line)


def visible_text(page):
    try:
        text = page.inner_text("body")
    except Exception as exc:
        return f"(could not read body text: {exc})"
    text = "\n".join(line.rstrip() for line in text.splitlines())
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    text = text.strip()
    if len(text) > VISIBLE_TEXT_LIMIT:
        omitted = len(text) - VISIBLE_TEXT_LIMIT
        text = text[:VISIBLE_TEXT_LIMIT] + f"\n… truncated, {omitted} more chars"
    return text


def cmd_snapshot(page, args):
    ok(page, args.target, ["visible:", visible_text(page)])


def cmd_goto(page, args):
    page.goto(args.url, wait_until="domcontentloaded")
    ok(page, args.target)


def cmd_click(page, args):
    page.click(args.selector)
    ok(page, args.target)


def cmd_fill(page, args):
    page.fill(args.selector, args.value)
    ok(page, args.target)


def cmd_text(page, args):
    value = page.inner_text(args.selector)
    ok(page, args.target, [f"text={value}"])


def cmd_screenshot(page, args):
    path = os.path.abspath(args.path or os.path.join(CACHE_DIR, "screenshot.png"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    page.screenshot(path=path, full_page=bool(args.full_page))
    ok(page, args.target, [f"screenshot={path}"])


def cmd_press(page, args):
    page.keyboard.press(args.key)
    ok(page, args.target)


def cmd_wait(page, args):
    page.wait_for_selector(args.selector)
    ok(page, args.target)


def cmd_eval(page, args):
    js = " ".join(args.js)
    result = page.evaluate(js)
    ok(page, args.target, [f"result={result!r}"])


def cmd_close_popup(browser, args):
    del args
    pages = listed_pages(browser)
    if len(pages) < 2:
        die_action("no popup tab to close; only main tab[0] is open")
    closed = []
    for page in reversed(pages[1:]):
        closed.append(page.url)
        page.close()
    main = main_page(browser)
    try:
        main.bring_to_front()
    except Exception:
        pass
    extra = [f"closed={url}" for url in closed]
    ok(main, "main", extra)


class ArgumentParser(argparse.ArgumentParser):
    """Usage errors must be exit 1, not argparse's default 2 (SESSION_DEAD)."""

    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"FAIL: {message}", file=sys.stderr)
        sys.exit(EXIT_ACTION)


def build_parser():
    parser = ArgumentParser(
        description="Run one action against the existing CDP session.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Tab model:
              Default: main tab[0] (the dedicated working tab).
              --popup: newest extra tab (site picker / window.open).
              close-popup: close extras and return to main. Do not open tabs.

            Exit codes:
              0  action succeeded
              1  action failed (selector, timeout, usage) — session still assumed live
              2  SESSION_DEAD — CDP connect failed; stop and report to the user
            """
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15000,
        help="Playwright action timeout in ms (default 15000)",
    )
    parser.add_argument(
        "--popup",
        action="store_true",
        help="Act on the newest extra tab, not main tab[0]",
    )
    sub = parser.add_subparsers(dest="verb", required=True)

    p = sub.add_parser("snapshot", help="URL, title, tab roles, visible text")
    p.set_defaults(func=cmd_snapshot)

    p = sub.add_parser("goto", help="Navigate to a URL")
    p.add_argument("url")
    p.set_defaults(func=cmd_goto)

    p = sub.add_parser("click", help="Click a selector")
    p.add_argument("selector")
    p.set_defaults(func=cmd_click)

    p = sub.add_parser("fill", help="Fill an input (clears existing value)")
    p.add_argument("selector")
    p.add_argument("value")
    p.set_defaults(func=cmd_fill)

    p = sub.add_parser("text", help="Print inner text of a selector")
    p.add_argument("selector")
    p.set_defaults(func=cmd_text)

    p = sub.add_parser("screenshot", help="Save a PNG")
    p.add_argument("path", nargs="?", default=None)
    p.add_argument("--full-page", action="store_true")
    p.set_defaults(func=cmd_screenshot)

    p = sub.add_parser("press", help="Press a key (Enter, Meta+a, ...)")
    p.add_argument("key")
    p.set_defaults(func=cmd_press)

    p = sub.add_parser("wait", help="Wait until a selector appears")
    p.add_argument("selector")
    p.set_defaults(func=cmd_wait)

    p = sub.add_parser("eval", help="Evaluate a JS expression in the page")
    p.add_argument("js", nargs="+")
    p.set_defaults(func=cmd_eval)

    p = sub.add_parser(
        "close-popup",
        help="Close every tab except main tab[0] and return to main",
    )
    p.set_defaults(func=cmd_close_popup)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.target = "popup" if args.popup else "main"

    if args.popup and args.verb == "close-popup":
        die_action("close-popup always targets extras; do not pass --popup")

    sync_playwright = load_playwright()
    try:
        with sync_playwright() as p:
            browser = connect_browser(p)
            if args.verb == "close-popup":
                args.func(browser, args)
            else:
                page = popup_page(browser) if args.popup else main_page(browser)
                try:
                    page.bring_to_front()
                except Exception:
                    pass
                page.set_default_timeout(args.timeout)
                args.func(page, args)
    except SystemExit:
        raise
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(EXIT_ACTION)

    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
