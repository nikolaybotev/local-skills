# Local Agent Skills

Reusable skills for local AI agents (LM Studio Bionic, Claude Code, etc.).

Each skill is a self-contained `SKILL.md` file that teaches the agent how to perform a specific automation task reliably.

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
