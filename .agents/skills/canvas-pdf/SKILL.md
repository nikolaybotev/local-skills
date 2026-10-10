---
name: canvas-pdf
description: >-
  Print a Cursor canvas to a PDF that looks like the canvas on screen. Use
  whenever the user wants a PDF, print, or saved file of a canvas or a
  .canvas.tsx, says the canvas is beautiful and should be kept, or asks to
  update that PDF after a canvas edit. Also use it when they ask for a
  localhost URL for a canvas. Do not use it for PDFs that are not of a canvas.
---

# Canvas to PDF

A Cursor canvas is a `.canvas.tsx` file the IDE compiles beside the chat. It is not a website. There is no localhost URL, and the canvas panel itself cannot be printed. Rebuild the canvas as one HTML page that matches what is on screen, then print that page.

The print that worked used Playwright's bundled Chromium, headless, in one shot. System Brave with `--print-to-pdf` hung on crashpad and display-link errors and wrote nothing. Do not use the visible-browser skill for this. That skill attaches over CDP and tells you not to call `chromium.launch()`.

## What to match

Match the canvas the user is looking at, not the editor theme name. `workbench.colorTheme` can say Cursor Dark while the canvas surface is light. That mismatch produced a dark PDF of a white canvas.

If the user shows the canvas, sample that image. Otherwise use the Cursor light surface unless they say the canvas is dark.

| | Light canvas | Dark canvas |
|---|---|---|
| Page | `#FCFCFC` | `#181818` |
| Text | `#141414` | `#F0F0F0` |
| Secondary text | `rgba(20,20,20,0.55)`–`0.72` | `rgba(240,240,240,0.6)`–`0.74` |
| Accent figures | `#2778C1` | `#81A1C1` |
| Table header and stripe | `#EEEEEE` | `rgba(240,240,240,0.06)` |
| Info bars | `#82BADD` | `#2E79B5` at 90% opacity |
| Grid lines | `#E6E6E6` | `rgba(240,240,240,0.12)` |

Leave out the IDE chrome: the canvas tab title, Publish, and the window frame. Print the canvas body.

Set `-webkit-print-color-adjust: exact` and `print-color-adjust: exact` on the page. Without that, the PDF drops the stripe, the accent, and the bars.

Use `"SF Pro Text", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif`. Copy the canvas heading, lede, stats, table, and chart. Keep the user's wording, including capitalization they corrected.

A bar chart is linear from zero. Check each bar height against its value before printing. The canvas abbreviates labels (`815K GB`) and ticks (`0 GB`, `500K GB`, `1M GB`). A label that looks like `10K` on a mid-chart line is usually `500K` with the 5 cut off. Put the sale dates under the bars.

`@page { size: letter portrait; margin: 0.55in; }` unless a wide table needs landscape. Prefer one page. If a long title spills a few lines onto a blank second page, tighten spacing instead of shipping that page.

## Print

Write the HTML to a temp file. Run `scripts/print_html_pdf.py` with a Python that already imports `playwright`. The usual one is the sibling skill's venv:

```bash
PY="<this-skill>/../chromium-browser-automation/.venv/bin/python"
"$PY" "<this-skill>/scripts/print_html_pdf.py" /tmp/canvas.html "/Users/<user>/Documents/<title>.pdf"
```

The script launches Playwright Chromium, opens the HTML with `file://`, and calls `page.pdf` with backgrounds and the CSS page size. It exits when the file is written.

Save the PDF where the user asked. When they say "my files" and name no folder, use `~/Documents/`. Do not guess a project folder.

When they edit the canvas after a PDF already exists, change the canvas and reprint that same PDF.

## Check

Open a full-page screenshot of the HTML and look at it. The page should be the same light or dark surface as the canvas, the accent column should be blue, and the bars should agree with the numbers. Count PDF pages. Embedded fonts hide the title from a raw byte search, so the screenshot is the check.
