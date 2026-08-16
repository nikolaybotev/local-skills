# Local Agent Skills

Reusable skills for local AI agents (LM Studio Bionic, Claude Code, etc.).

Each skill is a self-contained `SKILL.md` file that teaches the agent how to perform a specific automation task reliably.

## Skills

- **[brave-browser-automation](.agents/skills/brave-browser-automation/SKILL.md)** — Automate Brave browser via Playwright CDP connection. Launch once, reconnect across multiple steps, keep browser alive.

## Adding a Skill

1. Create a folder under `.agents/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter (`name`, `description`) and Markdown instructions
3. Commit and push

## Structure

```
.local-skills/
├── README.md
└── .agents/
    └── skills/
        └── brave-browser-automation/
            └── SKILL.md
```
