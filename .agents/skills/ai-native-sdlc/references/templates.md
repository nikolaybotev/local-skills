# Artifact templates

Use these shapes. Replace the bracketed text. Keep the header table. Relative links between the three files stay valid because they live in the same folder.

## intent/<slug>/intent.md

```markdown
# intent.md — <short name>

| | |
|---|---|
| Author | <name> |
| Captured | <YYYY-MM-DD> |
| Status | Draft |
| Stage | 1 · Plan |
| Feeds | [spec.md](spec.md) → [plan.md](plan.md) |
| Builds on | <link to a prior intent folder, or omit this row> |

## Problem

<What cannot be done today, in the originator's terms.>

## Proposed outcome

<What better looks like. No implementation plan here.>

## Affected users and systems

- **Users:**
- **Systems:**

## Constraints and principles

- <What should stay true. A principle the originator stated is a principle, even if it sounds optional.>

## Open questions (carried into spec.md)

1. <spec should answer or explicitly defer. A settled cut is not an open question.>

## Original prompt (verbatim)

> <The user's message, unchanged.>

## Source transcript (verbatim)

<Omit this section when the idea did not come from an earlier conversation.
When it did: cite the chat, then paste the exchange. No interpretation in this section.>
```

## intent/<slug>/spec.md

```markdown
# spec.md — <short name>

| | |
|---|---|
| Derived from | [intent.md](intent.md) (<date>) |
| Status | Draft 1 |
| Stage | 2 · Design |

## 1. Summary

## 2. Goals and non-goals

**Goals**

- G1.

**Non-goals**

-

**Release phasing.** This release is what the plan still claims. A sequenced release and an optional item stay on this intent. Staying is not an exemption from a recorded cut. Postponed work points at the skill's new-intent sentence and is not tagged on this spec.

## 3. Principles

- P1.

## 4. Users and scenarios

## 5. Functional requirements

<Numbered, testable requirements for this release.>

## 6. Acceptance criteria

<Each one names how it will be checked.>

## 7. Design decisions

**D1 — <title>.** <Choice. Why. What was rejected, if a later phase would otherwise reopen it. What was verified, and when.>

## 8. Open questions

<None, or the list still waiting on the human. Do not delete this section to look finished.>
```

Add sections the product needs (data sources, security, non-functional requirements). Do not add sections to mirror a previous product.

## intent/<slug>/plan.md

```markdown
# plan.md — <short name>

| | |
|---|---|
| Implements | [spec.md](spec.md) Draft <N> |
| Status | Draft 1 |
| Stage | 3 · Build |

Spec wins. An amendment that keeps the goals is written into the spec in the same commit, and the coverage row moves in that commit. An amendment that drops a goal is a cut. A procedure fix that does not contradict the spec is recorded in the plan only. A closed plan shows | Status | Finished | in the header table.

## Stops

<None, or one hard-to-undo choice, the options, and the resolution once made. This is not an approval role. Most plans have no stops.>

Example named cut: what closed; points at the new-intent sentence.

## Acceptance-criteria coverage

| AC | Check | Phase |
|---|---|---|
| AC1 | <command or test> | 0 |

## Phase 0 — <name>

Files: `<paths>`

1. <step>

DoD: <command or inspection shown at the commit that exits non-zero when unmet, including when the repo names no required check>

### Build notes (Phase 0)

<name which definition of done was met>
```

Repeat the phase block. A phase that is not yet built has no build notes.

## AGENTS.md and REVIEW.md

Copy [../assets/AGENTS.md](../assets/AGENTS.md) and [../assets/REVIEW.md](../assets/REVIEW.md). Replace every placeholder before committing. Specialize the review file's Bugs and Important lines to this product. When a command or a pitfall changes, edit `AGENTS.md` in the same change as the code.
