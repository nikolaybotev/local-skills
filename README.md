# Local Agent Skills

Reusable skills for local AI agents (LM Studio Bionic, Claude Code, Pi, OpenCode, Cursor, and others that read the Agent Skills layout).

Each skill is a self-contained `SKILL.md` file that teaches the agent how to perform a specific automation task reliably.

## Install

Skills install into `~/.agents/skills`. Re-running into the same destination adds missing skills and replaces each skill from this repo with the repo copy; other folders in that directory are not touched.

```sh
curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s
```

From a checkout of this repo, `./install.sh` installs that checkout instead of cloning.

Pass another directory when an agent looks somewhere else. Pi and OpenCode read `~/.agents/skills`. Claude Code reads `~/.claude/skills`. Cursor on your machine reads both. A Cursor Cloud Agent reads `~/.cursor/skills-cursor` on its VM, and does not read `~/.agents/skills`.

```sh
curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s -- ~/.claude/skills
curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s -- ~/.cursor/skills-cursor
```

Set `LOCAL_SKILLS_REPO_URL` when installing from a fork.

This repo's Cursor Cloud Agent environment does not use those curl lines. `.cursor/environment.json` runs `bash .cursor/install.sh`, which installs this checkout into `~/.cursor/skills-cursor`.

## Skills

- **[build-practices](.agents/skills/build-practices/SKILL.md)** — Shared rules for build pull requests and build review: writing rules, git workflow, merge gate, and Cloud Agent install boundaries. Loads on its own in any repo that installs this collection.
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
