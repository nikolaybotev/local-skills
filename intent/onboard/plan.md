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

Do not start Phase 0 until this gate has passed.

1. A fresh-context reviewer reads `spec.md` against `intent.md` and reports unclear, missing, or conflicting points. It does not edit.
2. Apply the findings you agree with. Re-check any fact the review disputes.
3. A second fresh-context reviewer reads `plan.md` against `spec.md`. It does not edit.
4. Apply those findings the same way.
5. Build when that review says to build and nothing in it still needs the owner.

Review model: Grok 4.7 High (D12). Phase 0 and Phase 1 model: Composer 2.5. Do not substitute. If a named model cannot be launched, stop and ask.

## Every phase

- Branch from current `main` in a new worktree. The primary checkout at `~/git/local-skills` stays on its current branch. Do not touch a dirty file there.
- Signed commits. Before the first commit of a phase, run `timeout 20 gpg --batch --local-user <key> --sign --output /dev/null` with the key `git config --get user.signingkey` returns. Never pass `--pinentry-mode error` or `--no-gpg-sign`. If the sign check fails, stop. Do not commit.
- One phase, one pull request, into `main`. The body lists the plan steps done and the definition-of-done evidence.
- Do not execute `install.sh` or `.cursor/install.sh` on the machine that builds the phase. Do not install skills onto a machine. The `install-smoke` job is the first run of those scripts, on the GitHub runner.
- Do not create rulesets, add required checks, dispatch workflows, cancel runs, or list secrets.
- Squash-merge only when the pull request has no failing checks, never with an admin override (D8). Delete-branch-on-merge is already on; do not force-push.
- Where this plan and the spec disagree, the spec wins. Record the discrepancy here. A phase that has not landed has no build notes.

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

Files: `AGENTS.md`, `REVIEW.md`, `README.md`

1. Write root `AGENTS.md` to FR1–FR6. Include every required phrase from FR5. Commands stop at the explicit-destination install. Point lint and smoke at the workflow that Phase 1 adds. Do not name a model, a host, or a person's home.
2. Write root `REVIEW.md` to FR8. Leave the asset template alone.
3. Edit `README.md` to FR10 and FR11. Do not rewrite the skill blurbs. Do not add `.github/` to the tree yet.
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
for s in ["~/.cursor/skills-cursor", ".cursor/install.sh", "~/.agents/skills", "already there is skipped", "~/.claude/skills"]:
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

Files: `.github/workflows/test.yml`, `AGENTS.md` (Commands only), `README.md` (structure tree only), and `setup.sh` only if shellcheck reports a finding there.

1. Add `.github/workflows/test.yml` to FR12–FR16. Job names and timeouts are D5. The smoke script is FR15, including the failing `git` on `PATH` and `timeout 30`. The frontmatter script is FR16. Do not add CodeQL. Do not add `workflow_dispatch`.
2. If `shellcheck` reports findings, fix them in the four scripts from FR14 in this same pull request. Do not waive findings. Do not run `setup.sh`.
3. Update `AGENTS.md` Commands to FR7.
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
    "timeout-minutes: 3",
    "timeout-minutes: 2",
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

The pull request is done when that script exits 0 and the three jobs on the pull request are green. Merge only then (D8).

After this phase is on `main`, required status checks are still not part of this plan (D7).
