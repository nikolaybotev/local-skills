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

- <What must stay true. A principle the originator stated is a principle, even if it sounds optional.>

## Open questions (carried into spec.md)

1. <Question the spec must answer or explicitly defer.>

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

**Release phasing.** <If some goals are later: what ships first, what is tagged as later, and that untagged requirements belong to the first release.>

## 3. Principles

- P1.

## 4. Users and scenarios

## 5. Functional requirements

<Numbered, testable. Later-release items tagged.>

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

Spec wins. Update this file in the same change whenever implementation departs from it.

## Stops

<None, or one hard-to-undo choice, the options, and the resolution once made. This is not an approval role. Most plans have no stops.>

## Acceptance-criteria coverage

| AC | Check | Phase |
|---|---|---|
| AC1 | <command or test> | 0 |

## Phase 0 — <name>

Files: `<paths>`

1. <step>

DoD: <command that exits non-zero on failure>

### Build notes (Phase 0)

<Added only after the phase lands. What was decided or what departed, and the consequence for later phases.>
```

Repeat the phase block. A phase that is not yet built has no build notes.

## AGENTS.md and REVIEW.md

Copy [../assets/AGENTS.md](../assets/AGENTS.md) and [../assets/REVIEW.md](../assets/REVIEW.md). Replace every placeholder before committing. Specialize the review file's Bugs and Important lines to this product. When a command or a pitfall changes, edit `AGENTS.md` in the same change as the code.
