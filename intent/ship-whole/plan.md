# plan.md — Ship the release whole

| | |
|---|---|
| Implements | [spec.md](spec.md) Draft 3 |
| Status | Finished |
| Stage | 3 · Build |

Spec wins. An amendment that keeps the goals is written into [spec.md](spec.md) in the same commit, and the coverage row below moves in that commit. An amendment that drops a goal is a cut. A procedure fix that does not contradict the spec is recorded here only.

Phase 0 has landed. The steps below are history of that run, not orders.

## Stops

None. The open questions in [intent.md](intent.md) are closed. A failed, cancelled, or still-running check in Phase 0 is not a stop.

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

One commit. Splitting the three skill files would leave the old rule beside the new one. Read `README.md` and `AGENTS.md` before editing them.

1. Done. Edited `SKILL.md` to FR3–FR10 and FR13–FR14 per the spec.
2. Done. Edited `references/templates.md` to FR2, FR11, and FR15 per the spec.
3. Done. Edited `references/goldvalue.md` for the departures clause and item 9 history marks per the spec.
4. Done. Updated the ai-native-sdlc blurb in `README.md` to say `when that phase is whole`.
5. Done. Set Status to Finished on the three headers, updated the current-change line in `AGENTS.md`, rewrote this plan preamble, and marked these steps done.
6. Done. Ran the definition of done on the Phase 0 commit; it exited 0 with a clean worktree.
7. Done. Ran `shellcheck`, `install-smoke`, and `skill-frontmatter` locally; all exited 0. Merge waits on the same three jobs on the pull request.

### Build notes (Phase 0)

DoD met: ship-whole inspection below on the Phase 0 commit; `shellcheck`, `install-smoke`, and `skill-frontmatter` exit 0. Build review fix: history marks in parentheses, cut/stop/publish sentences, and extended inspection.

DoD: the inspection below, run from the repo root on the Phase 0 commit. It exits non-zero when any check fails.

```sh
python3 - << 'PY'
import difflib, pathlib, re, subprocess, sys
from collections import Counter

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

def show(rev, path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"], text=True)

def need(text, needle, where):
    if needle not in text:
        die(where + " missing: " + needle)

def ban(text, needle, where):
    if needle in text:
        die(where + " still has: " + needle)

def line_with(text, needle, where):
    hits = [ln for ln in text.splitlines() if needle in ln]
    if len(hits) != 1:
        die(where + " expected one line for: " + needle)
    return hits[0]

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
            die(path + " contains a word the intent constraints forbid")

for needle in (
    "Do not ask questions.",
    "The parent does not review the diff and does not merge those pull requests.",
    "Skip it for a one-line fix or a typo.",
    "The Phase 5 check for two scheduled runs is that cron, not the push",
    "The spec did that for multi-currency",
    "publishes nothing may land",
    "as its own release may publish",
    "the next phase should not start",
    "should not publish until the remaining phases",
    "how publishing waits",
    "already-shipped path",
    "non-goal should stay a non-goal",
    "same commit",
    "drops a goal",
    "no required check",
    "owner check",
    "Staying is not an exemption from a recorded cut",
    "acceptance will match exactly",
    "recorded in the plan only",
    "should split",
    "land with the surface that uses it",
    "settled cut",
    "set Status to Finished",
    "The subagent should still be the one that merges.",
    "its own intent",
    "A merge onto the branch that runs the publish job is a publish.",
    "holding that merge",
    "changing the job in the same change",
    "Accepting the automatic tag is not a wait.",
    "The spec wins over the plan.",
    "If the plan is the one that is right, change the spec first.",
):
    need(skill, needle, "SKILL.md")

if skill.count("starts again at 1") != 1:
    die("SKILL.md new-intent sentence should appear once")
if skill.count("A new idea starts at") != 1:
    die("SKILL.md next-change sentence should appear once")

fm = skill.split("\n---\n", 1)[0]
need(fm, "when that phase is whole", "description")
item4 = [ln for ln in skill.splitlines() if "**Build.**" in ln and "when that phase is whole" in ln]
if len(item4) != 1 or "no required check" not in item4[0] or "not a stop" not in item4[0]:
    die("summary item 4 does not carry the whole-phase rule")
if "when CI is green" in item4[0]:
    die("summary item 4 still merges when CI is green")

failed = [
    ln for ln in skill.splitlines()
    if all(s in ln for s in ("cancelled", "still-running", "not a stop", "the next phase should not start"))
]
if not failed:
    die("failed-check rule is not one sentence")

start = skill.find("The prompt it was given:")
end = skill.find("The parent does not review")
if start < 0 or end <= start:
    die("subagent prompt markers missing")
prompt = skill[start:end]
for needle in (
    "keeps the goals",
    "drops a goal",
    "mistaken cut",
    "the spec does not decide",
    "wrong locked formula",
    "under the phase, and continue",
    "Do not ask questions.",
    "should take precedence",
    "what closed",
    "should not be treated as done",
    "calculates or promises",
):
    need(prompt, needle, "subagent prompt")

for needle in (
    "future phase",
    "what closed",
    "should not be treated as done",
    "calculates or promises",
    "publishes nothing may land",
    "as its own release may publish",
    "this skill's rule",
):
    need(skill, needle, "SKILL.md")

exc = line_with(skill, "usage limit", "SKILL.md")
need(exc, "checks the plan names have succeeded", "usage-limit exception")
sched = line_with(skill, "The Phase 5 check for two scheduled runs is that cron, not the push", "SKILL.md")
need(sched, "(history of that run, not the rule)", "scheduled-runs line")
multi = line_with(skill, "The spec did that for multi-currency", "SKILL.md")
need(multi, "(history of that run, not the rule)", "multi-currency line")

for needle in (
    "If something is undecidable",
    "tag the later items",
    "The subagent merges it when CI is green",
    "was green",
    "waits for that run and checks production",
    "record plan departures in",
):
    ban(skill, needle, "SKILL.md")

for needle in (
    "What should stay true",
    "spec should answer",
    "| Status | Finished |",
    "no required check",
    "what closed",
    "new-intent sentence",
    "same commit",
    "drops a goal",
    "recorded in the plan only",
    "Staying is not an exemption from a recorded cut",
    "settled cut",
):
    need(templates, needle, "templates.md")
if templates.count("stay true") != 1:
    die("templates.md constraints placeholder was not the only stay-true line")
for needle in (
    "Later-release items tagged",
    "tagged as later",
    "untagged requirements belong",
    "Added only after the phase lands",
):
    ban(templates, needle, "templates.md")

notes_at = templates.find("### Build notes (Phase 0)")
if notes_at < 0:
    die("templates.md build notes heading missing")
fence = templates.find("```", notes_at)
if fence < 0:
    die("templates.md build notes fence missing")
block_lines = [ln.strip() for ln in templates[notes_at:fence].splitlines() if ln.strip()]
if block_lines != ["### Build notes (Phase 0)", "<name which definition of done was met>"]:
    die("templates.md build notes fence should hold the heading and the named placeholder")
if "A phase that is not yet built has no build notes." not in templates[fence:]:
    die("templates.md moved the not-yet-built line inside the fence")

g8 = line_with(gold, "Each phase was one PR with a definition of done", "goldvalue.md")
depart = g8.find("Departures are in that phase's build notes inside `plan.md`")
commands = g8.find("gained the commands and the pitfalls in the same changes.")
mark = g8.find("history of that run, not the rule")
if depart < 0 or commands < 0 or not (depart < mark < commands):
    die("item 8 history mark is not on the departures clause")
g9 = line_with(gold, "from the same intent folder", "goldvalue.md")
need(g9, "history of that run, not the rule", "item 9")
need(g9, "already sequences", "item 9")
need(gold, "restarted the cycle", "goldvalue.md")

base_skill = show("7e7c572", ".agents/skills/ai-native-sdlc/SKILL.md")
base_templates = show("7e7c572", ".agents/skills/ai-native-sdlc/references/templates.md")
base_gold = show("7e7c572", ".agents/skills/ai-native-sdlc/references/goldvalue.md")

def skill_editable(text):
    idx = set()
    needles = (
        "builds one pull request per phase",
        "The subagent merges it when CI is green",
        "tag the later items",
        "If something is undecidable",
        "was green",
        "waits for that run and checks production",
        "record plan departures in",
    )
    for i, ln in enumerate(text.splitlines()):
        if any(needle in ln for needle in needles):
            idx.add(i)
    return idx

def following_line(lines, header):
    for i, ln in enumerate(lines):
        if ln.strip() == header:
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    return j
    return None

def templates_editable(text):
    lines = text.splitlines()
    idx = set()
    for header in ("## Constraints and principles", "## Open questions (carried into spec.md)"):
        j = following_line(lines, header)
        if j is None:
            die("templates baseline missing " + header)
        idx.add(j)
    needles = (
        "tagged as later",
        "untagged requirements belong",
        "Later-release items tagged",
        "whenever implementation departs",
        "exits non-zero on failure",
        "Added only after the phase lands",
    )
    for i, ln in enumerate(lines):
        if any(needle in ln for needle in needles):
            idx.add(i)
    return idx

def gold_editable(text):
    idx = set()
    for i, ln in enumerate(text.splitlines()):
        if (
            "Departures are in that phase's build notes inside `plan.md`" in ln
            or "from the same intent folder" in ln
        ):
            idx.add(i)
    return idx

def assert_untouched(base, new, editable, where):
    bl = base.splitlines()
    kept = Counter(bl[i] for i in range(len(bl)) if i not in editable and bl[i].strip())
    got = Counter(ln for ln in new.splitlines() if ln.strip())
    for ln, count in kept.items():
        if got[ln] != count:
            die(where + " untouched line changed: " + ln[:140])

skill_idx = skill_editable(base_skill)
template_idx = templates_editable(base_templates)
gold_idx = gold_editable(base_gold)
if len(skill_idx) < 7 or len(template_idx) < 7 or len(gold_idx) != 2:
    die("baseline edit lines not found")
assert_untouched(base_skill, skill, skill_idx, "SKILL.md")
assert_untouched(base_templates, templates, template_idx, "templates.md")
assert_untouched(base_gold, gold, gold_idx, "goldvalue.md")

log = subprocess.check_output(["git", "log", "--format=%H%x09%s"], text=True)
rev = ""
for row in log.splitlines():
    sha, subject = row.split("\t", 1)
    if subject == "docs: apply the ship-whole plan review":
        rev = sha
        break
if not rev:
    die("plan revision commit not found")

def line_changes(old, new):
    removed, added = [], []
    for row in difflib.ndiff(old.splitlines(), new.splitlines()):
        if row.startswith("- "):
            removed.append(row[2:])
        elif row.startswith("+ "):
            added.append(row[2:])
    return removed, added

readme_removed, readme_added = line_changes(show(rev, "README.md"), readme)
if len(readme_removed) != 1 or len(readme_added) != 1:
    die("README.md changed more than the skill blurb")
if "ai-native-sdlc" not in readme_removed[0] or "when CI is green" not in readme_removed[0]:
    die("README.md changed a different line")
if (
    "ai-native-sdlc" not in readme_added[0]
    or "when that phase is whole" not in readme_added[0]
    or "when CI is green" in readme_added[0]
):
    die("README blurb does not match the whole-phase rule")

agents_removed, agents_added = line_changes(show(rev, "AGENTS.md"), agents)
if len(agents_removed) != 1 or len(agents_added) != 1:
    die("AGENTS.md changed more than the current-change line")
if "The current change is documented" not in agents_removed[0]:
    die("AGENTS.md changed a different line")
if "intent/ship-whole/" not in agents_added[0] or "Finished" not in agents_added[0]:
    die("current-change line does not name this intent as Finished")
need(agents, "intent/onboard/", "AGENTS.md")

for label, text in (("intent.md", intent), ("spec.md", spec), ("plan.md", plan)):
    status = re.search(r"(?m)^\| Status \| ([^|]+) \|", text)
    if not status or status.group(1).strip() != "Finished":
        die(label + " status row is not Finished")
if not any(line.startswith("DoD met:") for line in plan.splitlines()):
    die("plan.md has no DoD met line")

preamble = plan.split("## Stops", 1)[0]
if "It is not Phase 0" in preamble:
    die("preamble still says this commit is not Phase 0")
need(preamble, "history of that run, not orders", "plan preamble")
steps = plan.split("## Phase 0", 1)[1].split("DoD: the inspection", 1)[0]
for n in range(1, 8):
    hits = [ln for ln in steps.splitlines() if re.match(r"^" + str(n) + r"\. ", ln)]
    if len(hits) != 1 or "Done." not in hits[0]:
        die("step " + str(n) + " still reads as an order")

status = subprocess.check_output(["git", "status", "--porcelain"], text=True)
if status.strip():
    die("worktree is not clean")

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
commits = subprocess.check_output(["git", "rev-list", rev + "..HEAD"], text=True).split()
if not commits:
    die("no Phase 0 commit")
seen = set()
for commit in commits:
    names = subprocess.check_output(
        ["git", "diff", "--name-only", commit + "^", commit],
        text=True,
    ).split()
    extra = sorted(set(names) - allowed)
    if extra:
        die("unexpected paths: " + ", ".join(extra))
    seen.update(names)
missing = sorted(allowed - seen)
if missing:
    die("Phase 0 change missing: " + ", ".join(missing))
print("ship-whole inspection ok")
PY
```
