# plan.md — Ship the release whole

| | |
|---|---|
| Implements | [spec.md](spec.md) Draft 2 |
| Status | Draft 1 |
| Stage | 3 · Build |

Spec wins. An amendment that keeps the goals is written into [spec.md](spec.md) in the same commit, and the coverage row below moves in that commit. An amendment that drops a goal is a cut. A procedure fix that does not contradict the spec is recorded here only.

This commit is the revised spec and this plan. It is not Phase 0. Phase 0 is the whole remaining change: one commit that edits the skill text the spec names.

## Stops

None. The open questions in [intent.md](intent.md) are closed. A failed check in Phase 0 is not a stop.

## Publishing

`.github/workflows/test.yml` runs `shellcheck`, `install-smoke`, and `skill-frontmatter` on pull requests and on push to `main`. It does not tag, release, or deploy. Phase 0 publishes nothing. It should land when it is whole. The wait for this change is the Finished headers, not a held publish job.

## Acceptance-criteria coverage

| AC | Check | Phase |
|---|---|---|
| AC1 | Phase 0 definition of done | 0 |
| AC2 | Phase 0 definition of done | 0 |
| AC3 | Phase 0 definition of done | 0 |
| AC4 | Phase 0 definition of done | 0 |
| AC5 | Phase 0 definition of done | 0 |
| AC6 | Phase 0 definition of done | 0 |
| AC7 | Phase 0 definition of done | 0 |
| AC8 | Phase 0 definition of done | 0 |
| AC9 | Phase 0 definition of done | 0 |
| AC10 | This revision's `git diff --name-only` against its parent is only `intent/ship-whole/` | revision |

## Phase 0 — Skill text

Files: `.agents/skills/ai-native-sdlc/SKILL.md`, `.agents/skills/ai-native-sdlc/references/templates.md`, `.agents/skills/ai-native-sdlc/references/goldvalue.md`, `README.md`, `AGENTS.md`, `intent/ship-whole/intent.md`, `intent/ship-whole/spec.md`, `intent/ship-whole/plan.md`

One commit. Splitting the three skill files would leave the old rule beside the new one.

1. Edit `SKILL.md` to FR3–FR10 and FR13–FR14. Keep the sentences FR3 lists. The description should say `when that phase is whole`. Summary item 4 should not keep `The subagent merges it when CI is green`. The build bullet should not keep `under the phase, and continue`. The iterate section should not keep `tag the later items`. Mark the deploy paragraph, the scheduled-runs sentence, and the multi-currency sentence with `history of that run, not the rule`. The subagent prompt should carry the same-commit amendment and the three moves.
2. Edit `references/templates.md` to FR2, FR11, and FR15. The two placeholders should say "should". Show `| Status | Finished |` as the closed header, and keep Draft as the start. The named cut should include `what closed`. The copyable build-notes block should not contain `Added only after the phase lands`.
3. Edit `references/goldvalue.md` so item 8's plan-note pattern and item 9's same-folder second version are each marked `history of that run, not the rule`. Leave the new-folder item in place.
4. In `README.md`, change only the ai-native-sdlc blurb so it says `when that phase is whole` and does not say `when CI is green`.
5. In the same commit, set Status to `Finished` on `intent/ship-whole/intent.md`, `spec.md`, and `plan.md`. Leave the stage labels. Add a build note whose first line is `DoD met:` and name the inspection below. Update the two `AGENTS.md` sentences that call `intent/config-as-code/` the active change so they name `intent/ship-whole/` as Finished and do not call either folder the open current change. Leave `intent/onboard/` historical. Leave the rest of `AGENTS.md` and `README.md` as they are.
6. Run the definition of done on that commit. It should exit 0. The worktree should be clean.
7. Merge only after `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded. If one of those jobs has failed, was cancelled, or is still running, the phase should not merge and the next phase should not start. Fix and re-run. That is not an owner stop. The subagent should merge. The parent should not merge that pull request.

DoD: the inspection below, run from the repo root on the Phase 0 commit. It exits non-zero when any check fails.

```sh
python3 - << 'PY'
import pathlib, re, subprocess, sys

def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

root = pathlib.Path(".")
skill = (root / ".agents/skills/ai-native-sdlc/SKILL.md").read_text()
templates = (root / ".agents/skills/ai-native-sdlc/references/templates.md").read_text()
gold = (root / ".agents/skills/ai-native-sdlc/references/goldvalue.md").read_text()
readme = (root / "README.md").read_text()
agents = (root / "AGENTS.md").read_text()
intent = (root / "intent/ship-whole/intent.md").read_text()
spec = (root / "intent/ship-whole/spec.md").read_text()
plan = (root / "intent/ship-whole/plan.md").read_text()

intent_src = intent
m = re.search(r"should not contain ([A-Z]{3,}), ([A-Z]{3,}), or ([A-Z]{3,})", intent_src)
if not m:
    die("intent constraint line missing")
for path, text in (
    ("SKILL.md", skill),
    ("templates.md", templates),
    ("goldvalue.md", gold),
):
    for word in m.groups():
        if re.search(r"\b" + word + r"\b", text, re.I):
            die(f"{path} contains a word the intent constraints forbid")

need_skill = [
    "Do not ask questions.",
    "The parent does not review the diff and does not merge those pull requests.",
    "Skip it for a one-line fix or a typo.",
    "The Phase 5 check for two scheduled runs is that cron, not the push",
    "multi-currency",
    "the next phase should not start",
    "should not publish until the remaining phases",
    "how publishing waits",
    "already-shipped path",
    "non-goal should stay a non-goal",
    "same commit",
    "drops a goal",
    "no required check",
    "owner check",
    "A later idea starts again at 1 in a new `intent/<change>/`.",
    "A new idea starts at [Prompt to first commit](#prompt-to-first-commit) in a new `intent/<slug>/` that links to the folder it builds on.",
]
for s in need_skill:
    if s not in skill:
        die(f"SKILL.md missing: {s}")
if skill.count("when that phase is whole") < 2:
    die("SKILL.md should say when that phase is whole in the description and the summary")
if skill.count("history of that run, not the rule") < 2:
    die("SKILL.md history mark missing on the deploy paragraph or the multi-currency sentence")
for s in (
    "under the phase, and continue",
    "tag the later items",
    "The subagent merges it when CI is green",
):
    if s in skill:
        die(f"SKILL.md still has: {s}")

for s in (
    "What should stay true",
    "spec should answer",
    "| Status | Finished |",
    "no required check",
    "what closed",
    "same commit",
    "drops a goal",
):
    if s not in templates:
        die(f"templates.md missing: {s}")
if templates.count("stay true") != 1:
    die("templates.md constraints placeholder was not the only stay-true line")
for s in (
    "Later-release items tagged",
    "tagged as later",
    "untagged requirements belong",
    "Added only after the phase lands",
):
    if s in templates:
        die(f"templates.md still has: {s}")

if gold.count("history of that run, not the rule") < 2:
    die("goldvalue.md should mark item 8 and item 9")
if "smoothed-gold" not in gold:
    die("goldvalue.md new-folder item missing")

blurb = next((line for line in readme.splitlines() if "ai-native-sdlc" in line and line.strip().startswith("-")), "")
if "when that phase is whole" not in blurb or "when CI is green" in blurb:
    die("README blurb does not match the whole-phase rule")

if "intent/config-as-code/" in agents:
    die("AGENTS.md still names config-as-code as a path")
if "intent/ship-whole/" not in agents or "Finished" not in agents:
    die("AGENTS.md does not name this intent as Finished")
if "intent/onboard/" not in agents:
    die("AGENTS.md dropped the onboard history note")

for label, text in (("intent.md", intent), ("spec.md", spec), ("plan.md", plan)):
    if "| Status | Finished |" not in text:
        die(f"{label} status is not Finished")
if not any(line.startswith("DoD met:") for line in plan.splitlines()):
    die("plan.md has no DoD met line")

status = subprocess.check_output(["git", "status", "--porcelain"], text=True)
if status.strip():
    die("worktree is not clean")
names = subprocess.check_output(
    ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
    text=True,
).split()
allowed = {
    ".agents/skills/ai-native-sdlc/SKILL.md",
    ".agents/skills/ai-native-sdlc/references/templates.md",
    ".agents/skills/ai-native-sdlc/references/goldvalue.md",
    "README.md",
    "AGENTS.md",
    "intent/ship-whole/intent.md",
    "intent/ship-whole/spec.md",
    "intent/ship-whole/plan.md",
}
extra = sorted(set(names) - allowed)
if extra:
    die("unexpected paths: " + ", ".join(extra))
if not names:
    die("HEAD commit has no files")
print("ship-whole inspection ok")
PY
```
