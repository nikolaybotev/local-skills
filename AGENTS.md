# Local Agent Skills

Reusable agent skills for local and cloud agents that read the Agent Skills layout. Skill sources live under `.agents/skills/`. The current change is documented in `intent/config-as-code/`.

## Commands

- Install (checkout only, never a real home): `./install.sh /path/to/empty-dest`. Healthy output includes `installed <name> ->` or `updated <name> ->` lines and ends with `done: <n> installed, <updated> updated, <removed> removed, destination <absolute>`. The default destination of `install.sh` is `$HOME/.agents/skills`; automation must not use it. `.cursor/install.sh` takes no destination argument; its only safe use is with a temporary `HOME` (it installs into `${HOME}/.cursor/skills-cursor`). Do not run either installer against a real home.
- Lint: `shellcheck` on `install.sh`, `.cursor/install.sh`, `.cursor/start.sh`, and `.agents/skills/chromium-browser-automation/scripts/setup.sh`. Healthy: no findings. The first script is POSIX `sh`. The other three are bash. Shellcheck follows each shebang.
- Test: GitHub Actions jobs `shellcheck`, `install-smoke`, and `skill-frontmatter`. Healthy: all three succeeded. Do not document a local `install.sh` against a real home as the test.

## Conventions

- For build and build-review, load and follow the installed **build-practices** skill. Required merge checks here are `shellcheck`, `install-smoke`, and `skill-frontmatter`.
- Use the **ai-native-sdlc** skill for bootstrap, spec, plan, and build orchestration. Historical folders under `intent/` are not edited in place.

## Architecture

- `.agents/skills/` — skill packages (`SKILL.md` plus scripts and references).
- `install.sh` — copies skills from a checkout or a shallow clone into a destination directory.
- `.cursor/` — Cloud Agent environment hooks (`environment.json`, `install.sh`, `start.sh`).
- `intent/<change>/` — intent, spec, and plan for the active change (currently `intent/config-as-code/`). `intent/onboard/` is historical.
- Root `AGENTS.md` and `REVIEW.md` — handbook and review guide for this repo (not the templates under `.agents/skills/ai-native-sdlc/assets/`).

## Things agents get wrong

- Do not run `install.sh` or `.cursor/install.sh` against a real `$HOME`. An explicit destination applies only to `install.sh`. `.cursor/install.sh` takes no destination. It always runs the root installer into `${HOME}/.cursor/skills-cursor`. For `.cursor/install.sh`, the only safe use is a temporary `HOME`. The default destination of `install.sh` is `$HOME/.agents/skills`.
- Re-running `install.sh` into the same destination replaces skills from the current source, removes installed skill directories that no longer appear in the source, and leaves other paths in the destination alone.
- A piped install runs `git clone --depth 1` with no branch, so it clones the default branch (today `main`), when the script is not a file beside `.agents/skills`. A checkout installs that checkout. Do not expect a pipe to carry a branch. The default clone URL works with no env vars; set `LOCAL_SKILLS_REPO_URL` only for a fork. Do not derive this repo from `GITHUB_REPOSITORY` in the installer—Actions sets that to the consuming repository.
- The installer ignores a directory under `.agents/skills/` that has no `SKILL.md`. Do not add a skill folder without that file.
- The copy excludes `.cache`, `.venv`, `.git`, and `__pycache__`. Do not commit those, and do not expect them after install.
- Cloud Agent skills for this repo go to `~/.cursor/skills-cursor`. `.cursor/install.sh` is the installer `.cursor/environment.json` runs. Do not document or implement `~/.cursor/skills` as that path.
- `.cursor/install.sh` takes no destination and only runs the root installer into `${HOME}/.cursor/skills-cursor`. Do not add a compiler, a package install, or a network fetch there. `.cursor/start.sh` stays a no-op.
- Do not put secrets, API keys, or key material in the repo, a skill, or the chat. Do not reimplement worker-key discovery with `ps`, `env`, or `pgrep`.
- `canvas-pdf` rebuilds a canvas as HTML. A canvas is not a localhost site. Do not print it with the visible-browser skill.
- The browser skill uses a dedicated profile under the skill `.cache/user-data`. Do not point it at a daily profile. Do not `killall` Chrome, Brave, or Edge. Do not use `chromium.launch()` from the browser skill. On `SESSION_DEAD` (exit 2), stop. Do not relaunch unless the user asks.
- Do not start another Cloud Agent environment build while a non-draft build is in progress, and do not call an environment ready before a non-draft default-branch build has succeeded. CI does not call that API and does not run the browser setup.
- Do not edit a historical `intent/` folder. A new change is a new folder.
- Do not add a CodeQL workflow. Do not add a `workflow_dispatch` trigger.
