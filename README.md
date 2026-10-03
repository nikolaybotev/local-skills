# Local Agent Skills

Reusable skills for local AI agents (LM Studio Bionic, Claude Code, Pi, OpenCode, Cursor, and others that read the Agent Skills layout).

Each skill is a self-contained `SKILL.md` file that teaches the agent how to perform a specific automation task reliably.

## Install

Skills install into `~/.agents/skills`. A folder that is already there is skipped.

```sh
curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s
```

From a checkout of this repo, `./install.sh` installs that checkout instead of cloning.

Pass another directory when an agent looks somewhere else. Pi and OpenCode read `~/.agents/skills`. Claude Code reads `~/.claude/skills`. Cursor on your machine reads both. A Cursor Cloud Agent reads `~/.cursor/skills` on its VM, and does not read `~/.agents/skills`.

```sh
curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s -- ~/.claude/skills
curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s -- ~/.cursor/skills
```

The Cursor Cloud Agent environment install command is the `~/.cursor/skills` line. That puts the skills on the VM without cloning this repo next to the project.

## Skills

- **[ai-native-sdlc](.agents/skills/ai-native-sdlc/SKILL.md)** — A disciplined cycle for one person building software with an agent: bootstrap, spec and plan, independent review, then a subagent that merges each phase when CI is green. Proved on goldvalue. Includes starter `AGENTS.md` and `REVIEW.md` templates.
- **[chromium-browser-automation](.agents/skills/chromium-browser-automation/SKILL.md)** — Drive a visible Chromium-family browser (Chrome, Chromium, Brave, Edge, or Playwright Chromium) over CDP. Dedicated profile, one-action CLI verbs, session stays open across steps.

## Adding a Skill

1. Create a folder under `.agents/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter (`name`, `description`) and Markdown instructions
3. Commit and push

## Structure

```
local-skills/
├── README.md
└── .agents/
    └── skills/
        ├── ai-native-sdlc/
        │   ├── SKILL.md
        │   ├── assets/
        │   └── references/
        └── chromium-browser-automation/
            └── SKILL.md
```
