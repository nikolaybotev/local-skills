# plan.md — Config as code

| | |
|---|---|
| Implements | [spec.md](spec.md) Draft 1 |
| Status | Draft 1 |
| Stage | 3 · Build |

Spec wins. Update this file in the same change whenever implementation departs from it.

This pull request is the draft: `intent/config-as-code/intent.md`, `spec.md`, and `plan.md` only. It is not a product phase. Do not edit the skill here.

## Stops

None. The session that opens this draft does not merge it and does not start Phase 0.

## Build gate

Do not start Phase 0 until this gate has passed.

1. A fresh-context reviewer reads `spec.md` against `intent.md` and reports unclear, missing, or conflicting points. It does not edit.
2. Apply the findings you agree with. Re-check any fact the review disputes.
3. A second fresh-context reviewer reads `plan.md` against `spec.md`. It does not edit.
4. Apply those findings the same way.
5. Squash-merge this draft only when `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded, never with an admin override. The workflow is already on `main` at `ecc0e2f`.
6. Build when that review says to build and nothing in it still needs the owner.

Phase 0 model: Composer 2.5. Do not substitute. If Composer 2.5 cannot be launched, stop and ask. Do not write that name into `SKILL.md`, `references/api.md`, `AGENTS.md`, `REVIEW.md`, or `README.md`.

## Every phase

- New worktree from current `main` after this draft is on `main`. The primary checkout stays on its current branch. Do not revive a branch named `cursor-cloud-environments`.
- Signed commits. Before the first commit, run `timeout 20 gpg --batch --local-user <key> --sign --output /dev/null` with the key `git config --get user.signingkey` returns. Never pass `--pinentry-mode error` or `--no-gpg-sign`. If the sign check fails, stop. Do not commit. Do not write the key id into the repo.
- Conventional commits. No force-push. No secrets.
- One phase, one pull request, into `main`. The body lists the plan steps done and the definition-of-done evidence.
- Do not run `install.sh` or `.cursor/install.sh` on the machine that builds the phase, and do not point either at a real home.
- Do not create rulesets, add required checks, dispatch workflows, cancel runs, or list secrets.
- Squash-merge only when `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded, never with an admin override (D15).
- Where this plan and the spec disagree, the spec wins. Record the discrepancy here.

## Acceptance-criteria coverage

| AC | Check | Phase |
|---|---|---|
| AC1 | The three files in `intent/config-as-code/`. Diff against `origin/main` is only that folder. | This draft |
| AC2 | Phase 0 definition of done | 0 |
| AC3 | Phase 0 definition of done | 0 |
| AC4 | Phase 0 definition of done | 0 |
| AC5 | `git diff --name-only origin/main` | 0 |
| AC6 | The three jobs green on the Phase 0 pull request, then squash-merge with no admin override | 0 |

## Phase 0 — Skill routes

The only implementation phase. One pull request. Branch from `main` after this draft is on it.

Files: `.agents/skills/cursor-cloud-environments/SKILL.md`, `.agents/skills/cursor-cloud-environments/references/api.md`, `AGENTS.md`, `REVIEW.md`, `README.md`

1. Edit `SKILL.md` to FR2 and FR4–FR7. Keep the folded description and `name: cursor-cloud-environments`. Do not reverse a D3 sentence.
2. Edit `references/api.md` to FR3 and FR8. Do not add a calls-table row, a field, or an endpoint.
3. Update the two `AGENTS.md` pointers (FR9) and the two `REVIEW.md` sentences (FR10). Leave every other sentence.
4. Add `config-as-code/` under `intent/` in the README tree. Leave `onboard/` there. Do not change the cursor-cloud-environments blurb (FR11).
5. Do not modify `scripts/environments.py`, any other skill, `intent/onboard/`, the installers, or `.github/workflows/test.yml`.
6. If a step departs from this plan, the spec wins. Write the departure into this file in the same commit.

DoD:

```sh
set -eu
cd "$(git rev-parse --show-toplevel)"
python3 - <<'PY'
from pathlib import Path
skill = Path(".agents/skills/cursor-cloud-environments/SKILL.md").read_text()
api = Path(".agents/skills/cursor-cloud-environments/references/api.md").read_text()
agents = Path("AGENTS.md").read_text()
review = Path("REVIEW.md").read_text()
readme = Path("README.md").read_text()
for s in [
    "name: cursor-cloud-environments",
    "inline-config",
    "POST /v1/environments",
    "snapshots the config and does not follow the repo file",
    "Config as code is the other route.",
    "without naming an environment",
    "preferred path for new repos",
    "This skill does not write that file and does not launch that agent or Project.",
    "No saved environment means no personal saved environment and no team saved environment.",
    "Do not call `create`.",
    "--owner team",
    "Do not treat a failed team list as empty.",
    "That is the inline-config snapshot.",
    "409 repo_file_environment_locked",
    "Do not use this to edit only a repo's .cursor/environment.json",
    "Do not create a new Cursor API key",
    "cursor-cloud MCP",
    "propose-environment-json",
    "A self-hosted run does not read",
    "Only Cursor-hosted agents use the saved environment.",
    "exit 127",
    "A personal environment overrides a committed",
    "does not set `repoFile`",
    "If any non-draft build is `IN_PROGRESS`, wait",
    "On HTTP 503 or 429, do not POST again",
    "Do not activate drafts",
    "`delete` refuses to run without `--yes`",
]:
    if s not in skill:
        raise SystemExit(f"SKILL.md missing: {s}")
for s in [
    "1. A personal saved environment",
    "2. A team saved environment",
    "for a single-repo cloud agent, when no saved environment matches",
    "`repoFile` stays unset.",
    "adopts a valid committed `.cursor/environment.json`",
    "409 repo_file_environment_locked",
    "Change the file and build that branch, or create a separate saved environment.",
    "is the inline-config route. It snapshots the config and does not follow the repo file.",
    "The other kind is Config as code.",
    "preferred path for new repos. It is not `POST /v1/environments`.",
    "neither a personal nor a team saved environment matched",
    "| `create` | `POST /v1/environments` |",
]:
    if s not in api:
        raise SystemExit(f"api.md missing: {s}")
if "The current change is documented in `intent/config-as-code/`." not in agents:
    raise SystemExit("AGENTS.md pointer missing")
if "intent/onboard/` is historical." not in agents:
    raise SystemExit("AGENTS.md historical note missing")
for s in [
    "intent/config-as-code/spec.md",
    "cursor-cloud-environments/SKILL.md",
    "references/api.md",
    "Bugs:",
    "Security:",
    "Compliance:",
    "skills-cursor",
    "SESSION_DEAD",
    "pgrep",
    "at most five nits",
    "verbatim prompt",
    "shellcheck",
    "install-smoke",
    "skill-frontmatter",
    "CodeQL",
    "workflow_dispatch",
]:
    if s not in review:
        raise SystemExit(f"REVIEW.md missing: {s}")
if "only allowed edit under" in review:
    raise SystemExit("REVIEW.md still has the onboarding skill-edit ban")
if "config-as-code/" not in readme or "onboard/" not in readme:
    raise SystemExit("README tree missing an intent folder")
blurb = "A new environment is not delivered until a non-draft default-branch build has succeeded."
if blurb not in readme:
    raise SystemExit("README blurb changed")
for forbidden in ["Composer", "Grok", "Roger", "Nikolay"]:
    for name, text in [
        ("SKILL.md", skill),
        ("api.md", api),
        ("AGENTS.md", agents),
        ("REVIEW.md", review),
        ("README.md", readme),
    ]:
        if forbidden in text:
            raise SystemExit(f"{name} contains {forbidden}")
PY
allowed='
.agents/skills/cursor-cloud-environments/SKILL.md
.agents/skills/cursor-cloud-environments/references/api.md
AGENTS.md
REVIEW.md
README.md
intent/config-as-code/plan.md
'
unexpected=$(
  git diff --name-only origin/main | while read -r path; do
    [ -n "$path" ] || continue
    printf '%s\n' "$allowed" | grep -qx "$path" || printf '%s\n' "$path"
  done
)
if [ -n "$unexpected" ]; then
  echo "$unexpected" >&2
  exit 1
fi
```

The pull request is done when this script exits 0 and `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded. Squash-merge then, with no admin override. Do not add rulesets or required checks.
