# plan.md — Onboard

| | |
|---|---|
| Implements | [spec.md](spec.md) Draft 1 |
| Status | Draft 1 |
| Stage | 3 · Build |

Spec wins. Update this file in the same change whenever implementation departs from it.

This pull request is the draft: `intent/onboard/intent.md`, `spec.md`, and `plan.md` only. It is not a product phase. Do not add `AGENTS.md`, `REVIEW.md`, the README edit, or `.github/workflows/test.yml` here.

## Stops

None. The project display name is not a file in this repo. Required status checks are not a step of this plan (D7).

## Build gate

Do not start the build until this gate has passed. The first product phase is Phase 1.

1. A fresh-context reviewer reads `spec.md` against `intent.md` and reports unclear, missing, or conflicting points. It does not edit.
2. Apply the findings you agree with. Re-check any fact the review disputes.
3. A second fresh-context reviewer reads `plan.md` against `spec.md`. It does not edit.
4. Apply those findings the same way.
5. Build when that review says to build and nothing in it still needs the owner.

Review model: Grok 4.7 High (D12). Phase 0 and Phase 1 model: Composer 2.5. Do not substitute. If a named model cannot be launched, stop and ask.

## Every phase

- Branch in a new worktree from the base in Order. Phase 1 branches from current `main`. This draft and Phase 0 rebase onto `main` only after that workflow is on it. The primary checkout at `~/git/local-skills` stays on its current branch. Do not touch a dirty file there.
- Signed commits. Before the first commit of a phase, run `timeout 20 gpg --batch --local-user <key> --sign --output /dev/null` with the key `git config --get user.signingkey` returns. Never pass `--pinentry-mode error` or `--no-gpg-sign`. If the sign check fails, stop. Do not commit.
- One phase, one pull request, into `main`. The body lists the plan steps done and the definition-of-done evidence.
- Do not execute `install.sh` or `.cursor/install.sh` on the machine that builds the phase. Do not install skills onto a machine. The `install-smoke` job is the first run of those scripts, on the GitHub runner.
- Do not create rulesets, add required checks, dispatch workflows, cancel runs, or list secrets.
- Squash-merge only when `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded, never with an admin override (D8). Merging this draft, or a docs-only pull request, before that workflow is on the branch does not meet the rule. Delete-branch-on-merge is already on; do not force-push.
- Where this plan and the spec disagree, the spec wins. Record the discrepancy here. A phase that has not landed has no build notes.

## Order

Phase 1 is the first product pull request. It branches from current `main`. Squash-merge it only after `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded. No admin override.

Do not squash-merge this draft or Phase 0 until that workflow is on `main`. Rebase onto that `main` so the workflow is on the branch. Squash-merge only after those three jobs have succeeded on the rebased pull request. No admin override.

Phase 0 branches from the post-Phase-1 `main`. In Phase 1, if `AGENTS.md` is not on `main`, create it with only the Commands section (FR7). In Phase 0, fill FR1–FR6 around those command lines, and keep `.github/workflows/test.yml` in the README tree.

## Acceptance-criteria coverage

| AC | Check | Phase |
|---|---|---|
| AC1 | The three files in `intent/onboard/`. Diff against `origin/main` is only that folder. | This draft |
| AC2 | Phase 0 definition of done | 0 |
| AC3 | Phase 0 definition of done | 0 |
| AC4 | Phase 0 definition of done | 0 |
| AC5 | Phase 1 definition of done, and the three jobs green on that pull request | 1 |
| AC6 | `git diff --name-only origin/main -- .agents/skills` | 0 and 1 |
| AC7 | Review of the diff | 0 and 1 |

## Phase 0 — Root agent docs

Starts after Phase 1 is on `main`. Branch from that `main`.

Files: `AGENTS.md`, `REVIEW.md`, `README.md`

1. `AGENTS.md` on that `main` has only the Commands section (FR7). Fill FR1–FR6 around those command lines. Include every required phrase from FR5, including the Conventions merge sentence. Do not remove the FR7 command lines. Do not name a model, a host, or a person's home.
2. Write root `REVIEW.md` to FR8. Leave the asset template alone.
3. Edit `README.md` to FR10 and FR11. Do not rewrite the skill blurbs. Keep `.github/workflows/test.yml` in the README tree.
4. Do not modify `.agents/skills/**` or any `intent/` folder other than build notes in `intent/onboard/plan.md` if a departure must be recorded.

DoD:

```sh
set -eu
cd "$(git rev-parse --show-toplevel)"
test -f AGENTS.md
test -f REVIEW.md
python3 - <<'PY'
import re
from pathlib import Path
agents = Path("AGENTS.md").read_text()
review = Path("REVIEW.md").read_text()
readme = Path("README.md").read_text()
for s in [
    "Bootstrap",
    "Spec and plan",
    "fresh-context",
    "Each phase is one pull request",
    "intent/<change>/intent.md",
    "spec wins",
    "skills-cursor",
    "leaves an existing skill directory untouched",
    "SESSION_DEAD",
    "CLAUDE.md",
    "admin override",
    "intent/onboard/",
    "pgrep",
    "CodeQL",
    "workflow_dispatch",
    "docs-only",
    "shellcheck",
    "install-smoke",
    "skill-frontmatter",
]:
    if s not in agents:
        raise SystemExit(f"AGENTS.md missing: {s}")
for s in [
    "Bugs:",
    "Security:",
    "Compliance:",
    "skills-cursor",
    "SESSION_DEAD",
    "pgrep",
    "at most five nits",
    "verbatim prompt",
]:
    if s not in review:
        raise SystemExit(f"REVIEW.md missing: {s}")
bad = re.findall(r"~/\.cursor/skills(?!-cursor)", readme)
if bad:
    raise SystemExit("README still points at ~/.cursor/skills")
for s in ["~/.cursor/skills-cursor", ".cursor/install.sh", "~/.agents/skills", "already there is skipped", "~/.claude/skills", ".github/workflows/test.yml"]:
    if s not in readme:
        raise SystemExit(f"README missing: {s}")
for forbidden in ["Grok", "Composer", "Roger"]:
    for name, text in [("AGENTS.md", agents), ("REVIEW.md", review), ("README.md", readme)]:
        if forbidden in text:
            raise SystemExit(f"{name} contains {forbidden}")
PY
if git diff --name-only origin/main -- .agents/skills | grep -q .; then
  echo "skills tree changed" >&2
  exit 1
fi
```

## Phase 1 — CI

First product pull request. Branch from current `main`, before Phase 0.

Files: `.github/workflows/test.yml`, `AGENTS.md` (Commands only), `README.md` (structure tree only), and `setup.sh` only if shellcheck reports a finding there.

1. Add `.github/workflows/test.yml` so it matches FR12–FR17. Job names, and the bans on `workflow_dispatch` and on cancelling runs, are D5. Timeouts are the FR13 table. The smoke script is FR15, including the failing `git` on `PATH` and `timeout 30`. The frontmatter script is FR16. Do not add CodeQL.
2. If `shellcheck` reports findings, fix them in the four scripts from FR14 in this same pull request. Do not waive findings. Do not run `setup.sh`.
3. If `AGENTS.md` is not on `main`, create it with only the Commands section (FR7). Do not write FR1–FR6 in this phase.
4. Add `.github/workflows/test.yml` to the README structure tree. No other README edit.
5. Do not modify skill markdown, Python, or `install.sh` except for a shellcheck fix required by step 2.

DoD:

```sh
set -eu
cd "$(git rev-parse --show-toplevel)"
python3 - <<'PY'
import re
from pathlib import Path
text = Path(".github/workflows/test.yml").read_text()
for s in [
    "name: shellcheck",
    "name: install-smoke",
    "name: skill-frontmatter",
    "timeout 30",
    "actions/checkout@v4",
    "contents: read",
]:
    if s not in text:
        raise SystemExit(f"workflow missing: {s}")
if "workflow_dispatch" in text or re.search(r"(?i)codeql", text):
    raise SystemExit("workflow has workflow_dispatch or CodeQL")
uses = re.findall(r"uses:\s*(\S+)", text)
if uses != ["actions/checkout@v4"] * 3:
    raise SystemExit(f"unexpected actions: {uses}")
if "secrets." in text:
    raise SystemExit("workflow references secrets")
agents = Path("AGENTS.md").read_text()
for s in [
    "shellcheck",
    "install-smoke",
    "skill-frontmatter",
    "install.sh",
    ".cursor/install.sh",
    ".cursor/start.sh",
    "chromium-browser-automation/scripts/setup.sh",
]:
    if s not in agents:
        raise SystemExit(f"AGENTS.md commands missing: {s}")
readme = Path("README.md").read_text()
if ".github/workflows/test.yml" not in readme:
    raise SystemExit("README tree missing the workflow")
PY
if git diff --name-only origin/main -- .agents/skills | grep -v 'chromium-browser-automation/scripts/setup.sh' | grep -q .; then
  echo "unexpected skill diff" >&2
  exit 1
fi
```

The pull request is done when the workflow matches FR12–FR17, the check script exits 0, and `shellcheck`, `install-smoke`, and `skill-frontmatter` are green. The script must not treat a stray `timeout-minutes` string as proof the whole workflow matches. Squash-merge this phase first, only then, with no admin override (D8).

After this phase is on `main`, required status checks are still not part of this plan (D7).

### Phase 1 build notes

- **Helper scripts under `.github/`.** FR15 and FR16 define the smoke and frontmatter checks; the plan file list names only `.github/workflows/test.yml`. Implementation adds `.github/install-smoke.sh` and `.github/skill-frontmatter-check.py` because inline `run:` heredocs in the workflow file are invalid once YAML step indentation is applied (heredoc delimiters must be column-zero). The workflow still invokes `timeout 30` on the smoke script (FR15) and runs the frontmatter logic unchanged (FR16). Spec wins on behavior; this note records the extra tracked paths.
