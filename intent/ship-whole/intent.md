# intent.md — Ship the release whole

| | |
|---|---|
| Captured | 2026-11-01 |
| Status | Draft |
| Stage | 1 · Plan |
| Feeds | [spec.md](spec.md) → [plan.md](plan.md) |

## Problem

A build can keep going when a choice is hard. The skill tells the build agent to make the most conservative choice consistent with the spec, note it, and continue. The skill also tells the spec to tag later work on the same change. A feature can ship in part, and work that no longer fits can stay attached to an intent that is otherwise finished.

## Proposed outcome

One change should be one intent, one spec, one plan, and one build. The plan should cover the whole release. It should not describe only part of the release.

Scope may be narrowed until the release. The cut should be recorded in plan.md. What remains should ship whole.

Narrowing should close the intent. Postponed work should not be left half-built, and it should not be added to the closed intent. The skill already has a new-intent sentence. New guidance should point at that sentence, and should not say it a second time.

A build should not ship part of a feature. Work that would ship only in part should be cut and recorded as postponed.

The sentences above are the direction. They are not the wording to paste into the skill. The spec should write the guidance as "should" and "should not".

## Affected users and systems

- **Users:** People who run this cycle, and the agents that read the skill.
- **Systems:** The ai-native-sdlc skill. This change does not add a stage.

## Constraints and principles

- New guidance should be written as "should" and "should not", not as an absolute.
- The final skill text should not contain MUST, NEVER, or ALWAYS.
- Sentences this change does not need to touch should stay as they are. A sentence that is rewritten because of this intent should use "should" and "should not".
- The skill should stay generic. It should not name a person, a machine, or anyone's own setup.
- The skill already has a new-intent sentence. Build on that sentence. The new text should not restate it.
- The four stages stay the whole cycle.

## Decisions

These close the three open questions. They are the direction for [spec.md](spec.md). They are not wording to paste into the skill.

1. **Conservative choice.** Continue should apply only when the choice leaves this release's goals and acceptance intact. The agent should make the most conservative choice consistent with the spec, note it, and continue. A choice that would ship a slice, leave a best effort or a stub on this intent, skip a test until an unscheduled follow-up, or write a "future phase" sentence should be a cut. The cut should be recorded, that part should be closed off, and the agent should continue only on the whole remainder. A choice that changes the goals, or an owner gate, should be a stop, and merge should wait until it is settled. The build bullet that says to make the most conservative choice and continue should be rewritten so this is one rule. It should not stay as a harder instruction beside the new one.
2. **One build.** One build should be the plan's phases for the whole release. It should not be one pull request for the whole release. Each phase should land as its own pull request when that phase is whole: its steps and its definition of done are met, its checks are green or have finished successfully, and it does not demote the rest. A failed check, or a check that is still running, should be a stop. The release should wait until all remaining phases have landed. A one-phase plan should be one pull request. A contract or output that an already-shipped surface emits should land with the surface that uses it. Anything that publishes on merge should be gated so a phase does not release a slice. A chunk whole enough to ship by itself should be its own intent. Who merges should stay as the skill already has it.
3. **Later items.** The skill should stop saying to tag later items on the same spec, and it should stop saying that untagged requirements belong to this change. Postponed work should point at the skill's existing new-intent sentence. The new text should not restate that procedure. The template's later-release tag line should change. The same-folder second version in `references/goldvalue.md` should be marked as history of that run, not as the rule. A release this same plan already sequences, and an item the plan already marks optional, should stay part of this release and should not need a new intent.

## Further changes

- A departure that contradicts the spec should amend the spec in the same change, not only be noted in the plan. A cut should be recorded in `plan.md` in the same change.
- When the remaining phases land, the intent, spec, and plan headers should be marked finished. Gate sentences should be updated. Superseded steps should no longer read as orders. Later decisions should become build notes.
- Fixing a shipped procedure in place, with the record, should be allowed. A new requirement, or a rewrite of the stored prompt, should start a new intent, pointing at the existing new-intent sentence and not restating it.
- A phase's definition of done should be meetable when that phase lands. Finished should mean that definition of done, so a repo with no required check can still finish.
- Normative text this change adds or rewrites should use "should" and "should not". The two intent-template placeholders that are stronger than "should" should say "should". The ship-whole rule should stay checkable, so that voice is not read as optional.

## Open questions (carried into spec.md)

None. The three questions are closed by the decisions above. [spec.md](spec.md) writes the guidance.

## Original prompt (verbatim)

The public copy leaves out the originator's name and the lines about who reviews this change. Those lines are how this change is reviewed. They are not part of the skill.

> The idea, rules for how Projects run the SDLC:
> 1. One intent, one spec, one plan, one build. No partial plans.
> 2. If something proves infeasible, scope may be narrowed right up to release. The cut is recorded in plan.md, and the release ships whole for what remains.
> 3. Narrowing closes the intent. Postponed work is never left half-built or tacked onto the closed intent. It starts again at stage 1 under one or more new intents.
> 4. Build agents never ship part of a feature. Anything that would be partial is cut and recorded as postponed. Today the skill says to 'make the most conservative choice and continue', so check how that interacts with this rule.
> Note: today's skill already says a later idea starts at 1 in a new intent folder. Build on that and don't duplicate it.

> Style guidance for this skill update: write the new guidance as 'should' and 'should not', not as absolutes. Don't use MUST, NEVER or ALWAYS in the final skill text. The rules listed earlier (no partial plans, narrowing closes the intent, build agents not shipping partial features) are the intent's direction, not literal wording. Put this in the intent so the reviewers check it too.
