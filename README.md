# Local Agent Skills

Reusable skills for local AI agents (LM Studio Bionic, Claude Code, Pi, OpenCode, Cursor, and others that read the Agent Skills layout).

Each skill is a self-contained `SKILL.md` file that teaches the agent how to perform a specific automation task reliably.

## Install

Skills install into `~/.agents/skills`. A folder that is already there is skipped.

Clone this repo, then run the installer from that checkout (it copies this tree instead of cloning again):

```sh
./install.sh
```

Pass another directory when an agent looks somewhere else. Pi and OpenCode read `~/.agents/skills`. Claude Code reads `~/.claude/skills`. Cursor on your machine reads both. A Cursor Cloud Agent reads `~/.cursor/skills-cursor` on its VM, and does not read `~/.agents/skills`.

```sh
./install.sh ~/.claude/skills
./install.sh ~/.cursor/skills-cursor
```

Without a checkout, set `GITHUB_REPOSITORY` (or `LOCAL_SKILLS_REPO_URL`) to this repo, pipe `install.sh` from the matching default branch on GitHub, then pass a destination if needed:

```sh
curl -fsSL "https://raw.githubusercontent.com/${GITHUB_REPOSITORY}/main/install.sh" | sh -s
curl -fsSL "https://raw.githubusercontent.com/${GITHUB_REPOSITORY}/main/install.sh" | sh -s -- ~/.cursor/skills-cursor
```

This repo's Cursor Cloud Agent environment does not use those curl lines. `.cursor/environment.json` runs `bash .cursor/install.sh`, which installs this checkout into `~/.cursor/skills-cursor`.

## Skills

- **[ai-native-sdlc](.agents/skills/ai-native-sdlc/SKILL.md)** — A disciplined cycle for one person building software with an agent: bootstrap, spec and plan, independent review, then a subagent that merges each phase when CI is green. Proved on goldvalue. Includes starter `AGENTS.md` and `REVIEW.md` templates.
- **[canvas-pdf](.agents/skills/canvas-pdf/SKILL.md)** — Print a Cursor canvas to a PDF that matches the canvas on screen. The canvas is not a localhost site. Rebuild it as HTML and print with Playwright Chromium.
- **[chromium-browser-automation](.agents/skills/chromium-browser-automation/SKILL.md)** — Drive a visible Chromium-family browser (Chrome, Chromium, Brave, Edge, or Playwright Chromium) over CDP. Dedicated profile, one-action CLI verbs, session stays open across steps.
- **[cursor-cloud-environments](.agents/skills/cursor-cloud-environments/SKILL.md)** — From a Cursor self-hosted My Machines worker, list, create, update, delete, and inspect history and builds of saved Cloud Agent environments with the worker's existing API key. A new environment is not delivered until a non-draft default-branch build has succeeded. Start that build only when one is not already in progress.

## Adding a Skill

1. Create a folder under `.agents/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter (`name`, `description`) and Markdown instructions
3. Commit and push

## Structure

```
local-skills/
├── README.md
├── AGENTS.md
├── REVIEW.md
├── install.sh
├── intent/
│   ├── config-as-code/
│   └── onboard/
├── .cursor/
│   ├── environment.json
│   ├── install.sh
│   └── start.sh
├── .github/
│   └── workflows/
│       └── test.yml  (.github/workflows/test.yml)
└── .agents/
    └── skills/
        ├── ai-native-sdlc/
        │   ├── SKILL.md
        │   ├── assets/
        │   └── references/
        ├── canvas-pdf/
        │   ├── SKILL.md
        │   └── scripts/print_html_pdf.py
        ├── chromium-browser-automation/
        │   ├── SKILL.md
        │   └── scripts/
        └── cursor-cloud-environments/
            ├── SKILL.md
            ├── scripts/environments.py
            └── references/api.md
```
