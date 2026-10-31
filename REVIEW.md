# Review instructions

## Passes

Run three passes and tag each finding with its pass:

- **Bugs:** the installer writes into a real home, leaves an existing skill directory untouched so a skip looks like success, clones the default branch (today `main`) when the review subject was a checkout, drops a directory that has no `SKILL.md`, passes a destination to `.cursor/install.sh`, or points a Cloud Agent at `~/.cursor/skills` instead of `~/.cursor/skills-cursor`. A skill change that relaunches a browser after `SESSION_DEAD`, starts a second environment build while a non-draft build is in progress, prints a canvas with the visible-browser skill, or uses `chromium.launch()` from the browser skill.
- **Security:** secrets, API keys, or key material in the repo or in instructions that print them. Reimplementing worker-key discovery with `ps`, `env`, or `pgrep`. An install or smoke test whose destination is outside a temporary directory. A network fetch from the product installer or from CI beyond checking out the repo and installing `shellcheck`.
- **Compliance:** the change matches `intent/<change>/spec.md` and `plan.md`, and the conventions in `AGENTS.md`. A departure from the plan that is not written back into `plan.md` in the same change is a compliance finding. Skills and docs stay generic. Historical `intent/` folders stay untouched. Historical onboarding did not change skill behavior. This change may edit `.agents/skills/cursor-cloud-environments/SKILL.md` and `.agents/skills/cursor-cloud-environments/references/api.md` only, as `intent/config-as-code/spec.md` requires. No other path under `.agents/skills/` changes. The workflow, once present, keeps the jobs `shellcheck`, `install-smoke`, and `skill-frontmatter`, does not add CodeQL, and does not add `workflow_dispatch`.

Also apply [BUILD_PRACTICES.md](.agents/skills/ai-native-sdlc/BUILD_PRACTICES.md) from the installed ai-native-sdlc skill when reviewing build pull requests.

## What Important means here

Reserve **Important** for a broken installer contract, a leaked secret, the browser skill on a daily profile, or a change the spec forbids. Style and naming are nits.

## Cap the nits

Report at most five nits per review; summarize the rest as a count.

## Do not report

Formatting CI already enforces, generated files the repo ignores (`.cache/`, `.venv/`, `__pycache__/`), or wording inside the verbatim prompt block of any `intent.md`.
