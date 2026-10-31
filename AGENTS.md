# AGENTS.md

## Commands

- Lint: `shellcheck` on `install.sh`, `.cursor/install.sh`, `.cursor/start.sh`, and `.agents/skills/chromium-browser-automation/scripts/setup.sh`. Healthy: no findings. The first script is POSIX `sh`. The other three are bash. Shellcheck follows each shebang.
- Test: GitHub Actions jobs `shellcheck`, `install-smoke`, and `skill-frontmatter`. Healthy: all three succeeded. Do not document a local `install.sh` against a real home as the test.
