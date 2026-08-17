#!/usr/bin/env python3
"""Save the Chromium-family engine for this skill (CDP to a dedicated profile).

Ask the user in chat first. Then run this with their choice. Not a TTY prompt.
"""

import argparse
import os
import subprocess
import sys

from config import (
    BROWSER_IDS,
    CONFIGURE_HINT,
    EXIT_ACTION,
    EXIT_OK,
    SKILL_DIR,
    browser_config,
    playwright_chromium_path,
    resolve_system_browser,
    system_browser_candidates,
    write_browser_file,
)


def install_playwright_chromium():
    python = sys.executable
    print("Installing Playwright Chromium binary ...", file=sys.stderr)
    subprocess.check_call([python, "-m", "playwright", "install", "chromium"])


def resolve(browser_id):
    if browser_id == "playwright-chromium":
        try:
            path = playwright_chromium_path()
        except Exception:
            path = None
        if not path or not os.path.isfile(path):
            install_playwright_chromium()
            path = playwright_chromium_path()
        if not path or not os.path.isfile(path):
            print(
                "FAIL: Playwright Chromium is not installed "
                f"(executable_path={path!r}).",
                file=sys.stderr,
            )
            sys.exit(EXIT_ACTION)
        return path

    path = resolve_system_browser(browser_id)
    if path:
        return path
    looked = system_browser_candidates(browser_id)
    print(f"FAIL: {browser_id} is not installed.", file=sys.stderr)
    if looked:
        print("Looked for:", file=sys.stderr)
        for candidate in looked:
            print(f"  {candidate}", file=sys.stderr)
    print("Install it, or set BROWSER_PATH to the executable.", file=sys.stderr)
    sys.exit(EXIT_ACTION)


def cmd_show():
    cfg = browser_config()
    if cfg is None:
        print("FAIL: no browser configured.", file=sys.stderr)
        print(CONFIGURE_HINT, file=sys.stderr)
        sys.exit(EXIT_ACTION)
    print(f"id={cfg['id']}")
    print(f"path={cfg['path']}")
    sys.exit(EXIT_OK)


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"FAIL: {message}", file=sys.stderr)
        sys.exit(EXIT_ACTION)


def main():
    parser = ArgumentParser(
        description="Choose the Chromium-family browser this skill will drive over CDP.",
    )
    parser.add_argument(
        "browser_id",
        nargs="?",
        choices=BROWSER_IDS,
        help="Engine to use for this machine",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Print the saved choice and exit",
    )
    args = parser.parse_args()

    if args.show:
        cmd_show()

    if not args.browser_id:
        parser.print_help(sys.stderr)
        print(
            "\nFAIL: pass one of: " + " | ".join(BROWSER_IDS),
            file=sys.stderr,
        )
        sys.exit(EXIT_ACTION)

    path = resolve(args.browser_id)
    write_browser_file(args.browser_id, path)
    print(f"id={args.browser_id}")
    print(f"path={path}")
    print(f"skill_dir={SKILL_DIR}")
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
