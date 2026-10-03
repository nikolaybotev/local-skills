# Worked example: goldvalue

Public repo: `github.com/nikolaybotev/goldvalue`.
Built in Cursor, chat [GoldValue SDLC](15bf70a9-b9c7-4696-b127-3fb1bfb0231e), starting 2026-09-28.
A later use of the skill (chat [Duffy Way goldbacks](600b6d01-b9cc-4204-a8cc-630eb188224c)) became the v1.2 intent. That intent stores the exchange verbatim and points at the skewed reading; the spec holds the design.

Do not copy goldvalue's domain rules into another repo. Copy the sequence.

## What the cycle actually did

1. A skill and a reference script came first (`.agents/skills/gold-value-normalizer/`). The product repo was created around them, and the workspace skill path became a symlink into the repo.
2. The opening product prompt mixed a raw idea with design questions and asked for `intent.md`, `spec.md`, and `plan.md` together. The intent stores that prompt verbatim. The spec answers the questions as D1–D15. The plan is phased.
3. The user then required the playbook's layout, agent-agnostic: `AGENTS.md` instead of `CLAUDE.md`, `.agents/skills/` instead of `.claude/skills/`, `REVIEW.md` at the root, and `intent/companion-app/` holding the three files.
4. Drafts moved while the user answered (Preact, sheet-wide currency, parity table, DEM, CSV snapshot). Open questions stayed open until answered. Q7 stayed open until the snapshot format was chosen.
5. Load-bearing claims were checked against live sources. Early drafts had the wrong BIS quote direction (currency per USD, so series are inverted), the wrong start dates, a DEM series that does not exist, and a gzip size that was estimated at ~200 KB and measured at ~77 KB.
6. Before the build gate, a fresh-context reviewer read the spec against the intent, then another read the plan. Findings were applied by the parent. Two sessions editing `spec.md` at once collided; one stood down.
7. Owner gate G0 stopped the build: publishing LBMA prices would redistribute licensed data. The user chose option A. The spec records D15 and the plan records the gate as resolved. Build started only after that.
8. Each phase was one PR with a definition of done. Departures are in that phase's build notes inside `plan.md` (month-to-date decided by `today`, batch number formatting, the `usd` header rule). `AGENTS.md` gained the commands and the pitfalls in the same changes.
9. v1.0.0 shipped at the end of Phase 5, v1.1.0 after the FX phases, from the same intent folder.
10. v1.2 restarted the cycle in `intent/v1.2-smoothed-gold/`, linked to `companion-app`. Its plan is two PRs with deviations written back, not a rewrite of the v1 plan.

## Layout that resulted

```
goldvalue/
├── AGENTS.md
├── REVIEW.md
├── README.md
├── intent/
│   ├── companion-app/{intent,spec,plan}.md
│   └── v1.2-smoothed-gold/{intent,spec,plan}.md
└── .agents/skills/gold-value-normalizer/
```

`AGENTS.md` states the chain in one line: `intent/<change>/intent.md` → `spec.md` → `plan.md`, and says to update `plan.md` in the same commit when implementation departs from it.
