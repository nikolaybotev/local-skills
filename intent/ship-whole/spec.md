# spec.md — Ship the release whole

| | |
|---|---|
| Derived from | [intent.md](intent.md) (2026-11-01) |
| Status | Draft 1 |
| Stage | 2 · Design |

## 1. Summary

The ai-native-sdlc skill should tell a reader to ship one intent whole. A build should continue only while this release's goals and acceptance stay intact. A slice, a leftover, or a later tag on this spec should be a cut. Phases of one plan may land separately when each phase is whole, and the release should wait until the remaining phases have landed. Postponed work should point at the skill's existing new-intent sentence.

This draft does not edit the skill. The build should edit the three files in FR1. It should not add a stage. The sentences in the intent are the direction. The requirements below are what the skill should tell a reader, in "should" and "should not".

Read on this branch from `.agents/skills/ai-native-sdlc/`. Those three files match `7e7c572`.

## 2. Goals and non-goals

**Goals**

- G1. An undecidable choice should continue only when this release's goals and acceptance stay intact. A slice, a best effort, a stub, a test skipped until an unscheduled follow-up, or a "future phase" sentence should be a cut. A goal change or an owner gate should be a stop.
- G2. One build should be the plan's phases for the whole release. A whole phase should be its own pull request. The release should wait until the remaining phases have landed.
- G3. The skill should stop teaching later tags on the same spec, and it should stop teaching that untagged requirements belong to this change. Postponed work should point at the existing new-intent sentence.
- G4. A contradicting departure should amend the spec in the same change. A cut should be recorded in `plan.md` in the same change. When the remaining phases land, the three headers should say Finished.
- G5. Text this change adds or rewrites should use "should" and "should not", and a reader should still be able to fail a partial ship.

**Non-goals**

- Adding a stage, or changing who merges a phase pull request.
- Restating the new-intent procedure.
- Editing any skill other than `ai-native-sdlc`, including build-practices.
- Editing `assets/AGENTS.md`, `assets/REVIEW.md`, the installers, or a historical `intent/` folder.
- Editing another repo's handbook that copied the phase rule.
- Rewriting sentences this change does not need. A sweep of every "Do not" in the skill is a different change.
- Installing skills, or writing `plan.md` in this draft.

**Release phasing.** This spec is the whole change. The plan should cover that skill update. This spec has no postponed work.

## 3. Principles

- P1. Normative text this change adds or rewrites should use "should" and "should not". The three words named in the intent's constraints should not appear in the three files.
- P2. A sentence this change does not need to touch should stay as it is.
- P3. New guidance should point at the skill's existing new-intent sentence. It should not restate that procedure.
- P4. "Should" is the voice. A partial ship should still be a missed definition of done.
- P5. The skill should stay generic. It should not name a person, a machine, or a setup.
- P6. The four stages stay the whole cycle.
- P7. The spec wins. A departure that contradicts the spec should be written into the spec in the same change.

## 4. Users and scenarios

- The choice is inside this release, and the goals and acceptance stay intact. The agent should note the conservative choice and continue.
- The choice would ship a slice, leave a best effort or a stub, skip a test until an unscheduled follow-up, or add a "future phase" sentence. The agent should cut that part, record the cut, and continue only on the whole remainder.
- The choice would change the goals, or it is an owner gate. The agent should stop, and the phase should not merge until it is settled.
- A phase's steps and definition of done are met, its checks are green or have finished successfully, and it does not demote the rest. That phase should land as its own pull request. The release should wait for the remaining phases.
- A merge would publish, or it would change a contract an already-shipped surface emits. The phase should not release a slice.
- Two requirements contradict. The postponed part should leave this spec. A release the plan already sequences, or an item the plan already marks optional, should stay.
- The remaining phases have landed. The three headers should say Finished, and a superseded step should not still read as an order.
- A shipped procedure is wrong. The fix should stay on this intent, with the record. A new requirement, or a rewrite of the stored prompt, should point at the existing new-intent sentence.

## 5. Functional requirements

### Files and voice

FR1. The build should edit only these skill files:

- `.agents/skills/ai-native-sdlc/SKILL.md`
- `.agents/skills/ai-native-sdlc/references/templates.md`
- `.agents/skills/ai-native-sdlc/references/goldvalue.md`

`intent/ship-whole/plan.md` may gain build notes in that change if implementation departs from this spec. No other path should change.

FR2. Normative text this change adds or rewrites should use "should" and "should not". The three files should not contain the three words named in the intent's constraints. In `references/templates.md`, the constraints placeholder and the open-questions placeholder should say "should". No other sentence should be rewritten only to soften its voice.

FR3. These should stay, and this change should not add a second copy of them:

- The cycle summary's existing new-intent sentence.
- The section "The next change".
- "Do not ask questions."
- "The parent does not review the diff and does not merge those pull requests."
- The usage-limit exception in the Build section.
- The description's "one pull request per phase". It should not say that a partial phase lands, and it should not grow a second procedure.

### Continue, cut, and stop

FR4. The build bullet that now says to make the most conservative choice consistent with the spec, note it in `plan.md` under the phase, and continue, should be rewritten so the ship-whole rule is that same instruction. The old sentence should not remain. The rewrite should say:

- When the choice leaves this release's goals and acceptance intact, the agent should make the most conservative choice consistent with the spec, note it, and continue.
- A choice that would ship a slice, leave a best effort or a stub on this intent, skip a test until an unscheduled follow-up, or write a "future phase" sentence should be a cut. The agent should record the cut, close that part off, and continue only on the whole remainder.
- A choice that changes the goals, or an owner gate, should be a stop. Merge should wait until it is settled.
- A phase that does one of those cut cases should not be treated as done.

FR5. A cut should be recorded in `plan.md` in the same change. The note should name what closed. It should not be left as an empty placeholder. A departure that contradicts the spec should amend the spec in that same change, not only be noted in the plan. The existing sentence that the spec wins, and that a right plan is written into the spec first, should stay.

### One build

FR6. Cycle summary item 4 should say that a phase is its own pull request only when that phase is whole, and that the release waits until the remaining phases have landed. The subagent should still be the one that merges. The parent should still launch the next chunk after a whole phase lands. Item 4 should not say to merge while a check has failed or is still running, and it should not say the release ships at the first phase.

FR7. The Build section should say what "whole" means. A phase is whole when its steps and its definition of done are met, its checks are green or have finished successfully, and it does not demote the rest. Demoting the rest means leaving a best effort, a stub, or a smaller promise than the spec still claims. A failed check, or a check that is still running, should be a stop. When the plan names no required check, finished should mean the definition of done, so that phase can still finish. A one-phase plan should be one pull request.

FR8. A contract or output that an already-shipped surface emits should land with the surface that uses it. Those two should not land in an earlier phase that publishes the contract alone. Anything that publishes on merge should be gated so a phase does not release a slice. A phase that does not publish may land when it is whole and does not demote the rest. The existing deploy paragraph, including the scheduled-runs sentence, should stay as history of that run. A definition of done should be meetable when the phase lands. It should not wait on a later observation.

FR9. The skill should say that a chunk whole enough to ship by itself should be its own intent. That sentence should point at the existing new-intent sentence. It should not restate the procedure, and it should not mean that this build is one pull request.

### Later work

FR10. The iterate section should no longer tell the reader to tag the later items on the same spec. The current sentence that says to split a first release from a later one and tag the later items should be replaced. When two requirements contradict, the part this release will not ship should be a cut under FR4. It should not stay on this spec as a later tag. A release this same plan already sequences, and an item the plan already marks optional, should stay part of this release and should not need a new intent. Postponed work should point at the existing new-intent sentence and should not be added to the closed intent.

FR11. `references/templates.md` should no longer say "Later-release items tagged", "tagged as later", or "untagged requirements belong". The release-phasing placeholder should say that this release is what the plan still claims, that a release the plan already sequences stays, that an item the plan already marks optional can be dropped without a new intent, and that postponed work points at the skill's new-intent sentence and is not tagged on this spec. The repeated phase block should stay.

FR12. In `references/goldvalue.md`, the item that says a later version shipped from the same intent folder should stay as what that run did, and it should say that this is history of that run, not the rule. The following item, a later change in a new folder, should stay. The file should not restate the new-intent procedure.

### Closing, and corrections

FR13. The skill should tell the reader to set Status to Finished on `intent.md`, `spec.md`, and `plan.md` when the remaining phases have landed. The stage labels should stay `1 · Plan`, `2 · Design`, and `3 · Build`. When a gate passes, a sentence that still says the build is closed until that gate should be updated in that change. A superseded step should not still read as an order. A decision made during the build should be a build note.

FR14. Fixing a shipped procedure in place should be allowed when the spec and the plan record it in that change. A new requirement, or a rewrite of the stored prompt, should not be added to the closed intent. It should point at the existing new-intent sentence and should not restate that procedure.

## 6. Acceptance criteria

| ID | Criterion | Check |
|---|---|---|
| AC1 | FR4 is true in the Build section, and the old unconditional continue sentence is absent. "Do not ask questions." is still there. | Read the Build bullet. Search `SKILL.md` for `under the phase, and continue`. |
| AC2 | FR5 is true. A contradicting departure amends the spec in the same change. A cut in `plan.md` names what closed. | Read the iterate section and the Build section. |
| AC3 | FR6 and FR7 are true in summary item 4 and the Build section. Who merges is unchanged: the subagent merges, and the parent sentence and the usage-limit exception in FR3 are unchanged. | Read those sections. Diff them against `7e7c572`. |
| AC4 | FR8 and FR9 are true. The scheduled-runs sentence remains. The description still says one pull request per phase and does not say a partial phase lands. | Read the Build section and the description. |
| AC5 | FR10 is true. `SKILL.md` does not contain `tag the later items`. The new-intent sentence and "The next change" are unchanged. | Search `SKILL.md`. Diff those two spots against `7e7c572`. |
| AC6 | FR11 is true. `references/templates.md` does not contain `Later-release items tagged`, `tagged as later`, or `untagged requirements belong`. The two placeholders say "should". The phase block remains. | Search that file. |
| AC7 | FR12 is true. The same-folder second version is marked history, not the rule, and the new-folder item remains. | Read `references/goldvalue.md`. |
| AC8 | FR13 and FR14 are true. Status Finished is the close. No new stage name appears. | Read `SKILL.md`. |
| AC9 | The three files do not contain the three words named in the intent's constraints. A sentence not covered by FR4–FR14 is unchanged from `7e7c572`. | Search the three files. Diff against `7e7c572`. |
| AC10 | This draft does not edit the three skill files. The build does. | `git diff --name-only` against the parent of this draft is only `intent/ship-whole/`. |

## 7. Design decisions

**D1 — Continue only on an intact release.** Decision 1 in [intent.md](intent.md). A conservative choice that leaves the goals and acceptance intact should be noted and the build should continue. After a cut, continue should apply to the whole remainder and should not apply to the cut. Rejected: continue through a slice. Rejected: stop on every undecidable detail.

**D2 — A goal change stops.** A choice that changes the goals, or an owner gate, should be a stop, and merge should wait. The skill already stops for an owner gate. This decision puts a goal change in that same class. Rejected: burying a goal change in a plan note and merging.

**D3 — One build is the plan's phases.** Decision 2. A whole phase should still be its own pull request, and the parent should still start the next chunk. The release should wait until the remaining phases have landed. Rejected: one pull request for the whole build. The rejected alternative is kept only as FR9: a chunk whole enough to ship by itself should be its own intent.

**D4 — Who merges stays.** The summary may change when a phase is allowed to merge. It should not change the actor. The parent sentence and the usage-limit exception should stay. Rejected: settling, in this change, whether a parent or a subagent merges.

**D5 — Publish and contracts.** A phase that publishes on merge should not release a slice. A contract an already-shipped surface emits should land with that surface. A phase that does not publish may land when it is whole. Rejected: holding every phase until the last one. Rejected: landing the contract in an earlier phase than the surface that uses it.

**D6 — Later tags retire.** Decision 3. "Tag the later items" and "untagged requirements belong" should go. A release the plan already sequences, and an item it already marks optional, should stay on this intent. Rejected: leaving a later tag on the closed spec. Rejected: opening a new intent for an optional item the plan already marked, or for a release the plan already sequenced.

**D7 — Point without restating.** Postponed work and a chunk that should be its own intent should point at the existing new-intent sentence. FR3 names the sentence and the section that should stay. Rejected: a second copy of that procedure in the skill, the template, or `references/goldvalue.md`.

**D8 — Same change for the spec and the plan.** The skill already says the spec wins and that departures go in `plan.md`. Builds have left the spec wrong, and have left cut placeholders empty. A contradicting departure should amend the spec in the same change, and a cut should be named in the plan in that same change. Rejected: a plan-only note.

**D9 — Finished is a status, not a stage.** The intent says this change does not add a stage. Status should become Finished on the three files when the remaining phases have landed. The stage labels should stay. Gate sentences and superseded steps should be updated so they do not still read as orders. Later decisions should be build notes, which the template already places after a phase lands. Rejected: a fifth stage.

**D10 — A procedure fix is not a new intent.** Fixing a shipped procedure, with the spec and the plan updated in that change, should stay on this intent. A new requirement or a rewrite of the stored prompt should not. Rejected: treating every follow-up edit as a failure to cut. Rejected: adding the new requirement to the closed intent.

**D11 — The definition of done can be met at landing.** A check that cannot be met when the phase lands should not be the definition of done. A repo with no required check should still be able to finish when the definition of done is met. The scheduled-runs sentence should stay as history of that run. Rejected: blocking finish on a check the plan does not require. Rejected: merging while a named check has failed or is still running.

**D12 — Voice, and the template placeholders.** The continue bullet is in scope because leaving it unchanged would outrank the new line. The two intent-template placeholders that are stronger than "should" are in scope. Other "Do not" sentences are not. The ship-whole rule should stay checkable through FR4's "should not be treated as done". Rejected: a sweep of the skill. Rejected: treating "should" as a way to skip a cut.

**D13 — This draft is not the build.** This spec does not edit the three skill files. AC10 checks that. The plan comes next and should cover the whole update in FR1.

## 8. Open questions

None.
