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

Narrowing should close the intent. Postponed work should not be left half-built, and it should not be added to the closed intent. It should start again at stage 1 as one or more new intents. The skill already says a later idea starts at stage 1 in a new intent folder. New guidance should use that, and should not say it a second time.

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
- The skill already says a later idea starts at stage 1 in a new intent folder. Build on that sentence.
- The four stages stay the whole cycle.

## Open questions (carried into spec.md)

1. The build section says that when something is undecidable, the agent should make the most conservative choice consistent with the spec, note it in plan.md, and continue. This intent's direction is that a build should not ship part of a feature. The spec should say how those two meet. A conservative choice inside the release can still be noted and carried on. A choice that would ship a slice, and leave the rest on this intent, should be a cut instead. The spec should say whether "continue" still applies once the cut is recorded and what remains is whole.
2. The cycle summary says each phase is one pull request, and the parent starts the next chunk after one lands. This intent's direction is one build, and a plan for the whole release. The spec should say whether one build is one pull request, or one plan whose phases may still land separately when each phase is whole and the release waits until the remaining scope has landed.
3. The iterate section says that when two requirements contradict, split a first release from a later one and tag the later items on the same spec. This intent's direction is that postponed work should not be added to the closed intent. The spec should reconcile those, using the existing new-intent section rather than restating it.

## Original prompt (verbatim)

The public copy leaves out the originator's name and the lines about who reviews this change. Those lines are how this change is reviewed. They are not part of the skill.

> The idea, rules for how Projects run the SDLC:
> 1. One intent, one spec, one plan, one build. No partial plans.
> 2. If something proves infeasible, scope may be narrowed right up to release. The cut is recorded in plan.md, and the release ships whole for what remains.
> 3. Narrowing closes the intent. Postponed work is never left half-built or tacked onto the closed intent. It starts again at stage 1 under one or more new intents.
> 4. Build agents never ship part of a feature. Anything that would be partial is cut and recorded as postponed. Today the skill says to 'make the most conservative choice and continue', so check how that interacts with this rule.
> Note: today's skill already says a later idea starts at 1 in a new intent folder. Build on that and don't duplicate it.

> Style guidance for this skill update: write the new guidance as 'should' and 'should not', not as absolutes. Don't use MUST, NEVER or ALWAYS in the final skill text. The rules listed earlier (no partial plans, narrowing closes the intent, build agents not shipping partial features) are the intent's direction, not literal wording. Put this in the intent so the reviewers check it too.
