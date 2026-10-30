# spec.md — Onboard

| | |
|---|---|
| Derived from | [intent.md](intent.md) (2026-10-30) |
| Status | Draft 1 |
| Stage | 2 · Design |

## 1. Summary

Add the agent handbook and a small CI workflow for this skills repo. Root `AGENTS.md` states the four-stage cycle and the prohibitions that come from `install.sh`, `.cursor/install.sh`, and the four skills. Root `REVIEW.md` reviews those same risks. The README is updated because it currently sends Cloud Agents to the wrong directory. CI is three short jobs in `.github/workflows/test.yml`: shellcheck, an installer smoke test into a temporary `HOME`, and `SKILL.md` frontmatter validation. CodeQL is out. This draft does not add those product files. Two later pull requests do.

The project display name is not a file in this repo. These docs do not name a person, a machine, or a model.

## 2. Goals and non-goals

**Goals**

- G1. Root `AGENTS.md` includes the cycle: bootstrap, spec and plan, fresh-context review, build one pull request per phase. It lists this repo's real failure modes as prohibitions.
- G2. Root `REVIEW.md` uses the three review passes, with Bugs and Important aimed at those same risks.
- G3. The README matches the installer on where a Cloud Agent gets these skills.
- G4. `.github/workflows/test.yml` runs shellcheck, a temp-`HOME` install smoke test, and `SKILL.md` frontmatter validation, each with a short timeout.
- G5. Later work lands as one pull request per phase, squash-merged only when that pull request's checks are green, never with an admin override.

**Non-goals**

- Editing anything under `.agents/skills/`, including the cursor-cloud-environments follow-up in the prompt (inline `POST /v1/environments` versus config as code). That is a later intent folder.
- Filling in `.agents/skills/ai-native-sdlc/assets/AGENTS.md` or `assets/REVIEW.md`. Those stay templates for other repos.
- Creating rulesets, adding required status checks, adding `workflow_dispatch`, cancelling runs, or listing secrets.
- Running either installer against a real home, or installing skills onto a machine.
- CodeQL, extra linters, and a dependency beyond `actions/checkout` and distro `shellcheck`.
- Putting a model choice, a host name, or a home directory of a person into `AGENTS.md`, `REVIEW.md`, or `README.md`.

**Release phasing.** Untagged requirements belong to the first release of this change, split into the two phases in [plan.md](plan.md). There is no later-release tag. The cursor-cloud-environments follow-up is a different change, not a tagged item of this one.

## 3. Principles

- P1. Skills and docs stay generic. A rule that names one machine is not a rule of this repo.
- P2. Prohibitions are taken from the installer and the skills. Do not invent failure modes the files do not support.
- P3. The spec wins over the plan. A departure is written back into both in the same pull request.
- P4. Each phase is one pull request.
- P5. Historical intent folders are not edited. This folder is the current change.
- P6. CI must fail closed and finish quickly. A hung clone or a package install inside the product installer is a failed job, not a longer timeout.

## 4. Users and scenarios

- An agent asked to change a skill reads `AGENTS.md` before editing, and does not run the installer into the default home directory.
- A reviewer uses `REVIEW.md` on a pull request and flags a stale skipped install, a Cloud Agent path of `~/.cursor/skills`, a leaked worker key, or a browser skill pointed at a daily profile.
- CI on a pull request rejects a shell error, an installer that misses the checkout and tries to clone, a skill directory without `SKILL.md`, or frontmatter whose `name` is not the directory name.
- A later change starts a new `intent/<slug>/` and leaves `intent/onboard/` as the record of this one.

## 5. Functional requirements

### AGENTS.md

FR1. Create `AGENTS.md` at the repo root. Do not create `CLAUDE.md`. Do not modify the template at `.agents/skills/ai-native-sdlc/assets/AGENTS.md`.

FR2. The file is short enough to read at the start of a session. It has the template sections: what this repo is (and that the current change is `intent/onboard/`), Commands, Conventions, Architecture, and Things agents get wrong.

FR3. Conventions state the cycle in the form below, and no extra stage.

1. **Bootstrap.** `AGENTS.md`, `REVIEW.md`, `README.md`, and `intent/<change>/` with the verbatim prompt plus `spec.md` and `plan.md`.
2. **Spec and plan.** Iterate both. Corrections become decisions. Check a fact before it hardens. The spec wins.
3. **Fresh-context review.** One review reads the spec against the intent. Another reads the plan against the spec. Neither edits. Apply the findings. Build only when that review says to build.
4. **Build.** Each phase is one pull request. Squash-merge it only when it has no failing checks, never with an admin override. Then start the next phase.

The chain is `intent/<change>/intent.md` → `spec.md` → `plan.md`. Update `plan.md` in the same commit when implementation departs from it.

FR4. Conventions also state the merge rules of this repo: pull request, squash only, signed commits, linear history, delete branch on merge, no admin override. Once `.github/workflows/test.yml` is on the branch, the jobs `shellcheck`, `install-smoke`, and `skill-frontmatter` must have succeeded before merge.

FR5. Things agents get wrong is a prohibition list. Each item below is normative and appears in substance. The quoted phrases are required, so a later check can find them.

- Do not run `install.sh` or `.cursor/install.sh` against a real `$HOME`. Pass an explicit destination, or set `HOME` to a temporary directory. The default destination is `$HOME/.agents/skills`.
- `install.sh` leaves an existing skill directory untouched. A skip is not an update.
- A piped install clones `main` when the script is not a file beside `.agents/skills`. A checkout installs that checkout. Do not expect a pipe to carry a branch.
- The installer ignores a directory under `.agents/skills/` that has no `SKILL.md`. Do not add a skill folder without that file.
- The copy excludes `.cache`, `.venv`, `.git`, and `__pycache__`. Do not commit those, and do not expect them after install.
- Cloud Agent skills for this repo go to `~/.cursor/skills-cursor`. `.cursor/install.sh` is the installer `.cursor/environment.json` runs. Do not document or implement `~/.cursor/skills` as that path.
- `.cursor/install.sh` only runs the root installer into that directory. Do not add a compiler, a package install, or a network fetch there. `.cursor/start.sh` stays a no-op.
- Do not put secrets, API keys, or key material in the repo, a skill, or the chat. Do not reimplement worker-key discovery with `ps`, `env`, or `pgrep`.
- `canvas-pdf` rebuilds a canvas as HTML. A canvas is not a localhost site. Do not print it with the visible-browser skill or with `chromium.launch()`.
- The browser skill uses a dedicated profile under the skill `.cache/user-data`. Do not point it at a daily profile. Do not `killall` Chrome, Brave, or Edge. On `SESSION_DEAD` (exit 2), stop. Do not relaunch unless the user asks.
- Do not start another Cloud Agent environment build while a non-draft build is in progress, and do not call an environment ready before a non-draft default-branch build has succeeded. CI does not call that API and does not run the browser setup.
- Do not edit a historical `intent/` folder. A new change is a new folder. Do not create `CLAUDE.md` or `.claude/skills/` in this repo.
- Do not write a skill or a doc for one machine. No host name, no person's home directory, no model name.
- Do not add a CodeQL workflow. Do not add a `workflow_dispatch` trigger.

FR6. Commands, in Phase 0, document install from a checkout into an explicit destination:

```sh
./install.sh /path/to/empty-dest
```

Healthy output contains `installed <name> ->` lines and ends with `done: <n> installed, <skipped> skipped, destination <absolute>`. Say that the default destination is `$HOME/.agents/skills` and that automation must not use it. Say that lint and the smoke test arrive with `.github/workflows/test.yml` (Phase 1). Do not tell the reader to run either installer with a real home.

FR7. Phase 1 updates Commands in the same pull request as the workflow. Add:

- Lint: `shellcheck` on `install.sh`, `.cursor/install.sh`, `.cursor/start.sh`, and `.agents/skills/chromium-browser-automation/scripts/setup.sh`. Healthy: no findings. The first script is POSIX `sh`. The other three are bash. Shellcheck follows each shebang.
- Test: GitHub Actions jobs `shellcheck`, `install-smoke`, and `skill-frontmatter`. Healthy: all three succeeded. Do not document a local `install.sh` against a real home as the test.

### REVIEW.md

FR8. Create `REVIEW.md` at the repo root by filling the template. Do not modify `.agents/skills/ai-native-sdlc/assets/REVIEW.md`. The file contains, in substance, the following.

- **Bugs:** the installer writes into a real home, leaves an existing skill directory untouched so a skip looks like success, clones `main` when the review subject was a checkout, drops a directory that has no `SKILL.md`, or points a Cloud Agent at `~/.cursor/skills` instead of `~/.cursor/skills-cursor`. A skill change that relaunches a browser after `SESSION_DEAD`, starts a second environment build while a non-draft build is in progress, or treats a canvas as a localhost site.
- **Security:** secrets, API keys, or key material in the repo or in instructions that print them. Reimplementing worker-key discovery with `ps`, `env`, or `pgrep`. An install or smoke test whose destination is outside a temporary directory. A network fetch from the product installer or from CI beyond checking out the repo and installing `shellcheck`.
- **Compliance:** the change matches `intent/<change>/spec.md` and `plan.md`, and the conventions in `AGENTS.md`. A departure from the plan that is not written back into `plan.md` in the same change is a compliance finding. Skills and docs stay generic. Historical `intent/` folders stay untouched. This onboarding does not change skill behavior. The only allowed edit under `.agents/skills/` is a shellcheck fix in `chromium-browser-automation/scripts/setup.sh` if that job requires one. The workflow, once present, keeps the jobs `shellcheck`, `install-smoke`, and `skill-frontmatter`, does not add CodeQL, and does not add `workflow_dispatch`.
- **Important** means a broken installer contract, a leaked secret, the browser skill on a daily profile, or a change the spec forbids. Style and naming are nits.
- Report at most five nits per review; summarize the rest as a count.
- Do not report formatting CI already enforces, generated files the repo ignores (`.cache/`, `.venv/`, `__pycache__/`), or wording inside the verbatim prompt block of any `intent.md`.

The strings `Bugs:`, `Security:`, `Compliance:`, `skills-cursor`, `SESSION_DEAD`, `pgrep`, `at most five nits`, and `verbatim prompt` are required.

### README

FR9. A README update is required. Checked on 2026-10-30 at `d006fc6`: the README says a Cursor Cloud Agent reads `~/.cursor/skills` and that the environment install command is the curl line to that path. `.cursor/install.sh` installs this checkout into `${HOME}/.cursor/skills-cursor` and says the Cloud Agent Skills menu and runtime read that directory. `.cursor/environment.json` runs `bash .cursor/install.sh`. The prompt says the same directory. An agent who followed the README would install to the wrong place and would treat the curl line as the environment installer.

FR10. Change only the misleading parts.

- Keep the default destination `~/.agents/skills`, the sentence that a folder already there is skipped, the Pi and OpenCode path, the Claude Code path `~/.claude/skills`, and the sentence that Cursor on your machine reads both. Those match `install.sh` or are not contradicted by it.
- State that a Cursor Cloud Agent reads `~/.cursor/skills-cursor` and does not read `~/.agents/skills`.
- The manual curl example for a machine with no checkout uses `~/.cursor/skills-cursor`, not `~/.cursor/skills`.
- State that this repo's cloud environment does not use that curl line. `.cursor/environment.json` runs `bash .cursor/install.sh`, which installs this checkout into `~/.cursor/skills-cursor`.
- The structure tree gains `install.sh`, `AGENTS.md`, `REVIEW.md`, `intent/onboard/`, and `.cursor/` (`environment.json`, `install.sh`, `start.sh`). Show `scripts/` under `chromium-browser-automation/` so that skill is not the one whose scripts are hidden. Do not rewrite the skill blurbs.
- Phase 1 adds `.github/workflows/test.yml` to that tree and nothing else in the README.

FR11. After the edit, `README.md` contains `~/.cursor/skills-cursor` and `.cursor/install.sh`, still contains `~/.agents/skills`, `already there is skipped`, and `~/.claude/skills`, and does not contain the path `~/.cursor/skills` except as the prefix of `~/.cursor/skills-cursor`.

### CI

FR12. Add `.github/workflows/test.yml` in Phase 1. Workflow triggers are `pull_request` and `push` to `main` only. No `workflow_dispatch`. No `paths` filter. No concurrency block that cancels runs. Permissions are `contents: read`. The only `uses:` action is `actions/checkout@v4`, once per job. The workflow does not read secrets.

FR13. Three jobs. The job `name` values are exactly `shellcheck`, `install-smoke`, and `skill-frontmatter`. Do not rename them.

| Job | `timeout-minutes` | What it does |
|---|---|---|
| `shellcheck` | 3 | Install distro `shellcheck`, then run it on the four tracked shell scripts. Follow shebangs. |
| `install-smoke` | 2 | Run the smoke script below under `timeout 30`. |
| `skill-frontmatter` | 2 | Run the frontmatter check below. |

Step `timeout-minutes`: checkout 1; the `shellcheck` job's package install 2; each remaining step 1. If the package install cannot finish inside the job timeout, that is a failed job. Do not raise the `install-smoke` or `skill-frontmatter` timeouts to compensate.

FR14. `shellcheck` covers exactly these tracked scripts:

- `install.sh` (`#!/bin/sh`)
- `.cursor/install.sh` (`#!/usr/bin/env bash`)
- `.cursor/start.sh` (`#!/usr/bin/env bash`)
- `.agents/skills/chromium-browser-automation/scripts/setup.sh` (`#!/usr/bin/env bash`)

`shellcheck` was not installed on the drafting machine, and this change must not install it there. If the job reports findings, fix those four scripts in the Phase 1 pull request. Do not waive a finding to go green. Do not execute `setup.sh` (it builds a virtualenv). Parsing it with shellcheck is the whole of its CI.

FR15. `install-smoke` does all of the following inside one `timeout 30` script. `HOME` is overridden on the command, not for the rest of the job. Every directory the script creates comes from `mktemp`.

1. Put a `git` executable earlier on `PATH` that exits 99. On a checkout, `install.sh` must not clone. A clone attempt fails the job.
2. `HOME` set to a temp directory, run `./install.sh "$dest"` with an explicit empty dest. Invoke it through the shebang (`./install.sh`), not `bash`. Every `.agents/skills/<name>/SKILL.md` in the checkout is installed at `$dest/<name>/SKILL.md`. At least one skill is installed.
3. Write a canary file inside an installed skill. Run `./install.sh "$dest"` again. The output includes `skip <name>` for each installed skill, and the canary is unchanged.
4. With `HOME` set to a different temp directory and no arguments, `./install.sh` installs into `$HOME/.agents/skills`.
5. With `HOME` set to a third temp directory, run `bash .cursor/install.sh`. Skills land in `$HOME/.cursor/skills-cursor/<name>/SKILL.md` and not in `$HOME/.agents/skills`.

The script prints nothing from a real home and does not use the runner's `HOME`. Installers are not run on the machine that authors the pull request. The runner is the first execution.

FR16. `skill-frontmatter` is Python 3, standard library only, no PyYAML. For each directory directly under `.agents/skills/`:

- The directory contains `SKILL.md`. A directory without it fails the job. That is stricter than `install.sh`, which skips such a directory, and it is intentional: a forgotten `SKILL.md` must not ship.
- The file starts with a `---` frontmatter fence and has a closing `---` fence.
- The `name` value equals the directory name. Accept an optional single pair of double quotes. The name is one line. Checked at `d006fc6`: `ai-native-sdlc`, `canvas-pdf`, `chromium-browser-automation`, and `cursor-cloud-environments` already match.
- `description` is present and non-empty. A folded value (`>-` or `|`) counts when the following indented block has non-whitespace text.

Zero skill directories fails the job.

FR17. Do not add CodeQL. See D6.

## 6. Acceptance criteria

| ID | Criterion | Check |
|---|---|---|
| AC1 | `intent/onboard/intent.md` quotes the prompt verbatim under "Original prompt", beside `spec.md` and `plan.md`. No other intent folder is edited. | Review the three files. `git diff --name-only origin/main` is only this folder for the draft pull request. |
| AC2 | Root `AGENTS.md` states the cycle in FR3 and the prohibitions in FR5, including the required phrases. | Phase 0 definition of done. |
| AC3 | Root `REVIEW.md` matches FR8, including the required phrases. | Phase 0 definition of done. |
| AC4 | README matches FR10 and FR11. | Phase 0 definition of done. |
| AC5 | The workflow matches FR12–FR17. The three jobs succeed on the Phase 1 pull request. | Phase 1 definition of done, plus the green checks. |
| AC6 | Phase 0 and Phase 1 do not modify `.agents/skills/**` except the shellcheck fixes FR14 allows inside `setup.sh` only. No other skill file changes. | `git diff --name-only origin/main -- .agents/skills` |
| AC7 | New docs and the workflow contain no secrets, key material, host names, or model names. | Review, and the Security pass. |

## 7. Design decisions

**D1 — Slug `onboard`.** The new folder is `intent/onboard/`. Checked 2026-10-30: `~/git/local-skills` is `/Users/nikolay/git/local-skills`, branch `main`, clean, same commit as `origin/main` after `git fetch origin main`. That commit is `d006fc6` (`d006fc6a91543ca2ff1e47b834503cc68d37fa20`). `git ls-files` has no `intent/**`, no root `AGENTS.md`, no root `REVIEW.md`, and no `.github/**`. History contains `AGENTS.md` and `REVIEW.md` only as the skill templates under `.agents/skills/ai-native-sdlc/assets/`. The slug is free. Those asset templates are not this change's historical intent, and they are not edited.

**D2 — This pull request is the draft only.** It adds `intent/onboard/intent.md`, `spec.md`, and `plan.md`. It does not add `AGENTS.md`, `REVIEW.md`, the README edit, or the workflow. The prompt for this session said not to implement the product files yet. Phase 0 and Phase 1 do that after review.

**D3 — README update is required.** The cloud-agent paragraph and the "environment install command" sentence are wrong. Evidence is in FR9. The rest of the install section matches `install.sh` (default `$HOME/.agents/skills`, skip when the destination exists, a checkout installs itself, a pipe clones). Leave those sentences. Rejected alternative: rewrite the README. The skill blurbs are not wrong.

**D4 — Prohibitions stay generic.** FR5 is taken from `install.sh` (default dest, skip, clone-when-piped, `SKILL.md` gate, tar excludes), `.cursor/install.sh` and `.cursor/environment.json` (`skills-cursor`, no package install), `.cursor/start.sh` (no-op), and the four `SKILL.md` files (canvas versus the visible browser, dedicated profile, `SESSION_DEAD`, worker key, no second build). Checked those files on 2026-10-30. No host name and no model name goes into the product docs. The build-model decision (D12) stays in the plan.

**D5 — Three jobs, those names, those timeouts.** One job would hide which check failed and would make the later check name a single blob. Three jobs match the three checks in the prompt. Names are the job `name` fields: `shellcheck`, `install-smoke`, `skill-frontmatter`. No path filters, so a skill-only pull request still runs all three. No third-party shellcheck action: the only action is `actions/checkout@v4`, and `shellcheck` comes from the distro package. No `workflow_dispatch`, because this plan must not grow a workflow someone is then told to dispatch. No cancel-in-progress concurrency.

**D6 — Skip CodeQL.** No `.github` directory exists at `d006fc6`. The repo is markdown, two installers, a no-op start script, and skill scripts. The failures that matter are the install contract, shell syntax, and frontmatter. CodeQL does not analyze shell, and it would not catch a wrong destination, a skipped skill, or a bad `name`. The Python in the skills is not a service this CI is trying to harden. A CodeQL job would also fight the aggressive timeouts. Do not add one.

**D7 — Required status checks stay outside this plan.** Checked 2026-10-30 with `gh api repos/nikolaybotev/local-skills/rulesets/26247122` and `gh repo view nikolaybotev/local-skills`. Ruleset name `main branch protection`, enforcement `active`, `bypass_actors` empty, includes `~DEFAULT_BRANCH`. Rules present: `deletion`, `non_fast_forward`, `required_linear_history`, `required_signatures`, `pull_request` with `allowed_merge_methods: ["squash"]` and `required_approving_review_count: 0`. No `required_status_checks` rule. Repo is public. Squash merge is allowed. Merge commits and rebase are not. Delete branch on merge is on. This plan does not create rulesets, add required checks, dispatch workflows, cancel runs, or list secrets. The job names in D5 are the names of the jobs. They stay stable so they are not renamed out from under a later admin step that is not part of this plan.

**D8 — Green means no failing checks.** Squash-merge a product pull request only when every check on it succeeded, never with an admin override. This draft, and Phase 0, land before the workflow exists, so they have no checks from this repo. Absence of checks is not a failing check, and it is not a reason to add a required check early. Phase 1 is the workflow: merge it only when `shellcheck`, `install-smoke`, and `skill-frontmatter` are green on that pull request.

**D9 — Frontmatter rules.** `name` equals the directory because the installer publishes the directory name and the skill's own `name` is what an agent matches. All four already match (checked by reading the `name:` line of each `SKILL.md`). Description uses a folded `>-` block in every current skill, so the checker accepts that shape without PyYAML. A directory with no `SKILL.md` fails CI even though the installer would skip it (installer loop: skip non-directories and directories without `SKILL.md`). Rejected alternative: shell out to a YAML package. Nothing in the repo depends on one today.

**D10 — Smoke test shape.** The five steps in FR15 lock the behaviors read from the scripts: shebang install, skip-plus-canary, default dest under `HOME/.agents/skills`, and `.cursor/install.sh` under `HOME/.cursor/skills-cursor`. The failing `git` on `PATH` is there because a checkout and a fresh clone of `main` can contain the same skill bytes on a docs-only pull request, so a content compare would not catch a broken checkout detector. The installers were not executed while drafting this spec. The prompt forbade running them. Behavior is from reading `install.sh` and `.cursor/install.sh`.

**D11 — Shellcheck scope is the four tracked scripts.** `git ls-files '*.sh'` returns only those four. `command -v shellcheck` was empty. Do not install shellcheck on the drafting machine. Phase 1's job is the first run. Fixes, if any, stay inside those scripts and inside that pull request.

**D12 — Review and build models.** Fresh-context review uses Grok 4.7 High. Phase 0 and Phase 1 use Composer 2.5. The prompt named those models. Do not substitute. If the named model cannot be launched, stop and ask. These names do not appear in `AGENTS.md`, `REVIEW.md`, or `README.md` (D4).

**D13 — The environment-skill follow-up is not this change.** Checked `cursor-cloud-environments`: `SKILL.md` already says a personal environment overrides a committed `.cursor/environment.json` and that the API stores a copy and does not set `repoFile`. `references/api.md` already says `repoFile` stays unset on create, and that a cloud agent start with no saved environment adopts a committed `.cursor/environment.json`. The prompt's follow-up is to make the skill say that plainly and to prefer the file for new repos. It gets its own intent folder after this one. This change does not edit that skill.

**D14 — Signing.** Commits on this repo are signed. `commit.gpgsign` is true and `user.signingkey` is set. The sign check is `timeout 20 gpg --batch --local-user <key> --sign --output /dev/null` with that configured key, before the first commit. Never pass `--pinentry-mode error` or `--no-gpg-sign`. The key id is not written into the repo. If the sign check fails, stop. Do not commit.

## 8. Open questions

None.
