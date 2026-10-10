#!/usr/bin/env python3
"""Print one local HTML file to PDF with Playwright's bundled Chromium.

Usage: print_html_pdf.py INPUT.html OUTPUT.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: print_html_pdf.py INPUT.html OUTPUT.pdf")
    html = Path(sys.argv[1]).resolve()
    pdf = Path(sys.argv[2]).resolve()
    if not html.is_file():
        sys.exit(f"html not found: {html}")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(html.as_uri(), wait_until="load")
        page.pdf(path=str(pdf), print_background=True, prefer_css_page_size=True)
        browser.close()
    print(pdf)


if __name__ == "__main__":
    main()
