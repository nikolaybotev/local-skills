# spec.md — Ship the release whole

| | |
|---|---|
| Derived from | [intent.md](intent.md) (2026-11-01) |
| Status | Draft 2 |
| Stage | 2 · Design |

## 1. Summary

The ai-native-sdlc skill should tell a reader to ship one intent whole. A build should continue only while this release's goals and acceptance stay intact. A slice or a later tag on this spec should be a cut. A whole phase may land on its own. A job that publishes on merge should not publish until the remaining phases of that change have landed. Postponed work should point at the skill's existing new-intent sentence.

This revision does not edit the skill. [plan.md](plan.md) is the one build for that edit. It should not add a stage. The sentences in the intent are the direction. The requirements below are what the skill should tell a reader, in "should" and "should not".

Read on this branch from `.agents/skills/ai-native-sdlc/`. Those three files match `7e7c572`.

## 2. Goals and non-goals

**Goals**

- G1. An undecidable choice should continue only when this release's goals and acceptance stay intact. A slice, a best effort, a stub, a test skipped until an unscheduled follow-up, or a "future phase" sentence should be a cut. A goal change, including what a feature calculates or promises, or an owner gate, should be a stop.
- G2. One build should be the plan's phases for the whole release. A whole phase should be its own pull request. A failed, cancelled, or still-running check should not merge and should not start the next phase.
- G3. The skill should stop teaching later tags on the same spec, and it should stop teaching that untagged requirements belong to this change. Staying on this intent should not exempt work from a recorded cut.
- G4. An amendment that keeps the goals should update the spec and the plan's coverage row in the same commit. The three headers should say Finished when the remaining phases have landed or a recorded cut closes the intent.
- G5. Text this change adds or rewrites should use "should" and "should not", and a reader should still be able to fail a partial ship.

**Non-goals**

- Adding a stage, or changing who merges a phase pull request.
- Restating the new-intent procedure.
- Editing any skill other than `ai-native-sdlc`, including build-practices.
- Editing `assets/AGENTS.md` or `assets/REVIEW.md`, the installers, or a historical `intent/` folder.
- Editing another repo's handbook, or another repo's description of an old phase rule. Those stay that repo's follow-up.
- Rewriting sentences this change does not need. A sweep of every "Do not" in the skill is a different change.
- Installing skills.

**Release phasing.** This spec is the whole change. The plan should cover that skill update in one build. This spec has no postponed work.

## 3. Principles

- P1. Normative text this change adds or rewrites should use "should" and "should not". The three words named in the intent's constraints should not appear in the three skill files.
- P2. A sentence this change does not need to touch should stay as it is.
- P3. New guidance should point at the skill's existing new-intent sentence. It should not restate that procedure.
- P4. "Should" is the voice. A partial ship should still be a missed definition of done.
- P5. The skill should stay generic. It should not name a person, a machine, or a setup.
- P6. The four stages stay the whole cycle.
- P7. The spec wins. An amendment that keeps the goals should be written into the spec in the same commit as the plan's coverage row.

## 4. Users and scenarios

- The choice is inside this release, and the goals and acceptance stay intact. The agent should note the conservative choice and continue.
- The choice would ship a slice, leave a best effort or a stub, skip a test until an unscheduled follow-up, or add a "future phase" sentence. The agent should cut that part, record the cut, and continue only on the whole remainder.
- The choice would change the goals, including what the feature calculates or promises, or it is an owner gate. The agent should stop, and the phase should not merge until it is settled.
- A check the plan names has failed, was cancelled, or is still running. The phase should not merge, the next phase should not start, and the check should be fixed and re-run. That is not an owner stop.
- A phase's steps and definition of done are met, the checks the plan names have succeeded, and it does not demote the rest. That phase should land as its own pull request. A job that publishes on merge should not publish until the remaining phases have landed.
- A release the plan already sequences, or an item it marks optional, stays on this intent unless it cannot ship whole. Then it is a cut. A finished control's non-goal stays a non-goal.
- The remaining phases have landed, or a recorded cut closes the intent. The three headers should say Finished.
- A shipped procedure is wrong and the spec is not contradicted. The plan should record the fix. The spec should not gain a new requirement from that fix.

## 5. Functional requirements

### Files and voice

FR1. The build should edit these files, and no others:

- `.agents/skills/ai-native-sdlc/SKILL.md`
- `.agents/skills/ai-native-sdlc/references/templates.md`
- `.agents/skills/ai-native-sdlc/references/goldvalue.md`
- The ai-native-sdlc blurb in `README.md`
- The two active-change sentences in `AGENTS.md`
- The three headers in this folder, and this plan's landing note, in the same commit as that build

FR2. Normative text this change adds or rewrites should use "should" and "should not". The three skill files should not contain the three words named in the intent's constraints. In `references/templates.md`, the constraints placeholder and the open-questions placeholder should say "should". No other sentence should be rewritten only to soften its voice. AC9 does not forbid these edits.

FR3. These should stay, and this change should not add a second copy of them:

- The cycle summary's existing new-intent sentence.
- The section "The next change".
- "Do not ask questions."
- "The parent does not review the diff and does not merge those pull requests."
- The usage-limit exception in the Build section.
- "Skip it for a one-line fix or a typo."

The description should say one pull request per phase when that phase is whole. It should not keep the shorter phrase as the only limit, and it should not grow a second procedure.

### Continue, cut, and stop

FR4. The build bullet that now says to make the most conservative choice consistent with the spec, note it in `plan.md` under the phase, and continue, should be rewritten so the ship-whole rule is that same instruction. The old sentence should not remain. The rewrite should tell the reader:

- When the choice leaves this release's goals and acceptance intact, the agent should make the most conservative choice consistent with the spec, note it, and continue.
- A choice that would ship a slice, leave a best effort or a stub on this intent, skip a test until an unscheduled follow-up, or write a "future phase" sentence should be a cut. The agent should record the cut, close that part off, and continue only on the whole remainder.
- A choice that changes the goals, or an owner gate, should be a stop. Merge should wait until it is settled. A choice about what a feature calculates or promises should be that kind of stop, not a conservative choice.
- A phase that does one of those cut cases should not be treated as done.
- A failed, cancelled, or still-running check is not a stop. The phase should not merge, and the next phase should not start. The check should be fixed and re-run.

FR5. An amendment that keeps the goals should be written into the spec in the same commit as the plan's acceptance-criteria coverage row. An amendment that drops a goal is a cut. Editing the spec should not make that drop look consistent. A wrong sentence the release still needs is an amendment, not a cut. Putting a mistaken cut back before the release tag should stay on this intent. After the tag, it should point at the existing new-intent sentence. Where the plan does not use a release tag, the Finished header is that boundary. A cut should be named in `plan.md` in that same commit. The note should say what closed. It should not be left as an empty placeholder. The existing sentence that the spec wins, and that a right plan is written into the spec first, should stay.

The subagent prompt should carry this same-commit amendment and the three moves: an amendment that keeps the goals, an amendment that drops a goal, and putting a mistaken cut back before or after the release boundary.

Text that acceptance will match exactly should enter the spec in that same commit.

### One build

FR6. Cycle summary item 4 should say that a phase is its own pull request only when that phase is whole, and that the release waits until the remaining phases have landed. It should carry the no-required-check finish and the failed-check rule in FR4. It should not keep "merge when CI is green" as the only line. The sentence "The subagent merges it when CI is green" should not remain. The subagent should still be the one that merges. The parent should still launch the next chunk after a whole phase lands. Item 4 should not say the release ships at the first phase.

FR7. The Build section should say what "whole" means. A phase is whole when its steps and its definition of done are met, the checks the plan names have succeeded, and it does not demote the rest. Demoting the rest includes leaving a best effort, a stub, or a smaller promise than the spec still claims, and leaving an already-shipped path unable to run until a later phase. A control this release does not offer should stay off the shipped surface, including a parameter, a dead flag, or a half-wired path.

The definition of done should be a command or inspection the phase can show at its commit, including when the repo names no required check. Required checks are the merge gate. A job the plan does not name as required is not part of done. The definition of done should exercise the acceptance. A test that only restates expected numbers should be a cut. Evidence the environment cannot collect should be recorded as an owner check, not marked done, and it should not by itself hold a phase whose other checks are met.

A one-phase plan should be one pull request. A failed, cancelled, or still-running check the plan names should not merge and should not start the next phase.

FR8. A phase may land when it is whole and does not demote the rest. A job that publishes on merge, including a tag, a release, or a deploy of the surface the owner sees, should not publish until the remaining phases of that change have landed. The plan should say how publishing waits in that repo. A phase that publishes nothing may land. A release the plan sequences as its own release may publish. A contract or output that an already-shipped surface emits should land with the surface that uses it, not in an earlier phase that publishes the contract alone.

The deploy paragraph, including "The Phase 5 check for two scheduled runs is that cron, not the push", should stay and should be marked `history of that run, not the rule`. It should not read as an order for a later phase. The publish rule above is the order.

FR9. The skill should say that a chunk whole enough to ship by itself should be its own intent. That sentence should point at the existing new-intent sentence. It should not restate the procedure, and it should not mean that this build is one pull request. This is not the rejected alternative of one pull request for the whole build.

### Later work

FR10. The iterate section should no longer tell the reader to tag the later items on the same spec. The current sentence that says to split a first release from a later one and tag the later items should be replaced. "The spec did that for multi-currency" should stay and should be marked `history of that run, not the rule`. It should not remain a live example of tagging later items.

When two requirements contradict, the part this release will not ship should be a cut under FR4. It should not stay on this spec as a later tag. A release this same plan already sequences, and an item the plan already marks optional, should stay on this intent. Staying means it is not moved to a new intent. It is not an exemption from a recorded cut. If it cannot ship whole, it is a cut under FR4, which closes that part and points at the existing new-intent sentence. A finished control's non-goal should stay a non-goal. It should not become postponed work, and it should not start a new intent until someone asks. Postponed work should point at the existing new-intent sentence and should not be added to the closed intent. A settled cut should not stay in the open-questions list.

FR11. `references/templates.md` should no longer say "Later-release items tagged", "tagged as later", or "untagged requirements belong". The release-phasing placeholder should say that this release is what the plan still claims, that a sequenced release and an optional item stay on this intent, that staying is not an exemption from a recorded cut, and that postponed work points at the skill's new-intent sentence and is not tagged on this spec. It should not say that an optional item can be dropped without a new intent. The repeated phase block should stay. The open-questions placeholder should say a settled cut is not an open question.

FR12. In `references/goldvalue.md`, the plan-note pattern in item 8 and the same-folder second version in item 9 should each be marked `history of that run, not the rule`. The following item, a later change in a new folder, should stay. The file should not restate the new-intent procedure. The history mark on item 9 should not forbid a later release this same plan already sequences. That case is FR10.

### Closing, corrections, and the template

FR13. The skill should tell the reader to set Status to Finished on `intent.md`, `spec.md`, and `plan.md` when the remaining phases have landed, or when a recorded cut closes the intent. The stage labels should stay `1 · Plan`, `2 · Design`, and `3 · Build`. When a gate passes, a sentence that still says the build is closed until that gate should be updated in that change. A superseded step should not still read as an order. A decision made during the build should be a build note. The note for a landed phase should say which definition of done was met. A session-start line that names this intent as the current change, such as a line in `AGENTS.md`, should be updated in that same change.

A phase that changes something the tree already describes, such as `README.md` or `AGENTS.md`, should update that description in the same change.

FR14. A procedure fix that does not contradict the spec should be recorded in the plan only. The one-line fix and typo skip in FR3 should stay. A fix should not add a requirement. A commit that mixes a fix with a new requirement, or with a rewrite of a settled claim, should split, and the new part should point at the existing new-intent sentence. A contradicting departure that keeps the goals should follow FR5.

FR15. The plan block in `references/templates.md` should change as follows, and the starting status should stay Draft.

- The departure line should carry the spec-amendment sentence: an amendment that keeps the goals is written into the spec in the same commit, and the coverage row moves in that commit. An amendment that drops a goal is a cut. A procedure fix that does not contradict the spec is recorded in the plan only.
- The definition-of-done line should allow the no-required-check case: a command or inspection shown at the commit that exits non-zero when unmet.
- The template should show a Finished header as the closed value, with Draft remaining the start.
- It should show a named-cut example that says what closed and points at the existing new-intent sentence.
- The build-notes block inside the copyable fence should not contain a sentence that can be committed as the note. The instruction that a phase which is not yet built has no build notes should stay outside that fence. When the phase lands, the note should name which definition of done was met.

## 6. Acceptance criteria

| ID | Criterion | Check |
|---|---|---|
| AC1 | FR4 is true. The old unconditional continue sentence is absent. "Do not ask questions." is still there. A failed, cancelled, or still-running check is not called a stop. | Read the Build bullet and summary item 4. Search `SKILL.md` for `under the phase, and continue`. It is absent. |
| AC2 | FR5 is true, including the three moves in the subagent prompt, the same commit for the spec and the coverage row, and exact-match text entering the spec in that commit. | Read the Build prompt and the iterate section. |
| AC3 | FR6 and FR7 are true. `The subagent merges it when CI is green` is absent. Who merges is unchanged: the subagent merges, and the parent sentence and the usage-limit exception in FR3 are unchanged. | Read summary item 4 and the Build section. Diff the parent sentence against `7e7c572`. |
| AC4 | FR8 and FR9 are true. The scheduled-runs sentence remains and is marked `history of that run, not the rule`. The description says `when that phase is whole`. | Read the description, the Build section, and the deploy paragraph. |
| AC5 | FR10 is true, including that staying is not an exemption from a cut, that a non-goal stays a non-goal, and that a settled cut is not an open question. `tag the later items` is absent. The multi-currency sentence is marked `history of that run, not the rule`. The new-intent sentence and "The next change" are unchanged. | Search `SKILL.md`. Diff those two spots against `7e7c572`. |
| AC6 | FR2, FR11, and FR15 are true. The two placeholders say "should". The later-tag phrases are absent. The plan template has the departure sentence, the no-required-check definition of done, a Finished header, a named cut, and no committable build-note sentence. | Search `references/templates.md`. |
| AC7 | FR12 is true. Items 8 and 9 are marked `history of that run, not the rule`. The new-folder item remains. | Read `references/goldvalue.md`. |
| AC8 | FR13 and FR14 are true. Finished applies when the remaining phases have landed or a recorded cut closes the intent. The one-line skip remains. No new stage name appears. | Read `SKILL.md`. |
| AC9 | The three skill files do not contain the three words named in the intent's constraints, in any case. A sentence not covered by FR2 or FR4–FR15 is unchanged from `7e7c572`. The FR2 placeholders and the template lines FR11 and FR15 name are exempt from that unchanged-sentence check. | Search the three files. Diff against `7e7c572`. |
| AC10 | This revision does not edit the three skill files. The build in [plan.md](plan.md) does. | `git diff --name-only` against the parent of this revision is only `intent/ship-whole/`. |

## 7. Design decisions

**D1 — Continue only on an intact release.** Decision 1 in [intent.md](intent.md). A conservative choice that leaves the goals and acceptance intact should be noted and the build should continue. After a cut, continue should apply to the whole remainder. Rejected: continue through a slice. Rejected: stop on every undecidable detail.

**D2 — A goal change stops.** A choice that changes the goals, or an owner gate, should be a stop, and merge should wait. A choice about what a feature calculates or promises is that stop. A detail inside a formula the spec already locks can still be noted and continued. Rejected: picking an unlocked formula, merging it, and calling that conservative.

**D3 — One build is the plan's phases.** Decision 2. A whole phase should still be its own pull request, and the parent should still start the next chunk. The release should wait until the remaining phases have landed. Rejected: one pull request for the whole build. That rejected alternative is not kept. FR9 is a different rule: a chunk whole enough to ship by itself should be its own intent, and it should not mean this build is one pull request.

**D4 — Who merges stays.** The summary may change when a phase is allowed to merge. It should not change the actor. The parent sentence and the usage-limit exception should stay. Rejected: settling, in this change, whether a parent or a subagent merges.

**D5 — Publish is one sentence.** A phase may land when it is whole and does not demote the rest. A job that publishes on merge should not publish until the remaining phases of that change have landed, and the plan should say how publishing waits. A phase that publishes nothing may land. A release the plan already sequences as its own release may publish. Rejected: the word "gated" with no applicable sentence. Rejected: holding every phase until the last one. Rejected: landing a contract in an earlier phase than the surface that uses it. The old deploy-on-every-merge paragraph is history of that run, not this sentence.

**D6 — Later tags retire, and staying is not an exemption.** Decision 3. "Tag the later items" and "untagged requirements belong" should go. A sequenced release and an optional item stay on this intent, which means they are not moved to a new intent. If one cannot ship whole, it is a cut under FR4. Rejected: FR11 saying an optional item can be dropped without a new intent. Rejected: leaving a later tag on the closed spec. Rejected: opening a new intent for a finished control's non-goal.

**D7 — Point without restating.** Postponed work and a chunk that should be its own intent should point at the existing new-intent sentence. FR3 names the sentence and the section that should stay. Rejected: a second copy of that procedure in the skill, the template, or `references/goldvalue.md`.

**D8 — Same commit for the spec and the coverage row.** An amendment that keeps the goals moves the spec and the plan's coverage row in one commit. An amendment that drops a goal is the cut, and editing the spec does not make the drop consistent. A wrong sentence the release still needs is an amendment. Putting a mistaken cut back before the release boundary stays on this intent; after that boundary it points at the new-intent sentence. Rejected: a plan-only note when the spec is wrong. Rejected: a quiet spec edit that drops a goal. Empty cut placeholders are the failure this rejects. A contradicting formula left in the spec while the plan said otherwise is the same failure.

**D9 — Finished is a status, not a stage.** Status should become Finished when the remaining phases have landed or a recorded cut closes the intent. The stage labels should stay. A session-start line that still names the intent as the current change should be updated in that change. A landed phase's build note should say which definition of done was met. Rejected: a fifth stage. Rejected: headers left at Draft because the last phase was cut and nothing new landed. Shipped intents whose headers still say Draft are the case.

**D10 — A procedure fix is a plan record.** A fix that does not contradict the spec is recorded in the plan only. The one-line and typo skip stays. A fix should not add a requirement. A mixed commit splits. Rejected: a spec edit for every procedure fix. Rejected: a new requirement riding along in the fix commit. A repair written only into a handbook, and not into the plan, is the case for recording it in the plan.

**D11 — The definition of done is shown at the commit.** It is a command or inspection, including when the repo names no required check. Required checks are the merge gate. A job the plan does not name is not part of done. A test that only restates expected numbers is a cut. Evidence this environment cannot collect is an owner check, not marked done, and it does not by itself hold the phase. Rejected: setting done to a remote job the plan does not require. Rejected: merging while a named check has failed, was cancelled, or is still running. A cancelled check is in that class. It is not an owner stop. Rejected: calling that wait a stop, which would freeze a fix the phase can re-run.

**D12 — Voice, and the template placeholders.** The continue bullet is in scope because leaving it unchanged would outrank the new line. The two intent-template placeholders that are stronger than "should" are in scope. AC9 exempts those lines and the other template edits. Other "Do not" sentences are not in scope. The ship-whole rule should stay checkable through FR4's "should not be treated as done". Rejected: a sweep of the skill. Rejected: an acceptance check that fails the placeholder edit it also requires.

**D13 — History is not an order.** The scheduled-runs sentence, the deploy paragraph around it, goldvalue item 8's plan-note pattern, goldvalue item 9's same-folder second version, and the multi-currency sentence should be marked `history of that run, not the rule`. Item 9's mark should not forbid a release this plan already sequences. Rejected: leaving the scheduled-runs sentence as the concrete order beside the new rule. Rejected: deleting the historical fact.

**D14 — Demotion includes a broken shipped path.** Leaving an already-shipped path unable to run until a later phase demotes the rest, even when the spec of that phase allowed the break. A control this release does not offer stays off the shipped surface. Rejected: calling that phase whole because its own steps passed.

**D15 — Described surfaces move in the same change.** A phase that changes something `README.md` or `AGENTS.md` already describes should update that description then. This repo's skill blurb and active-change lines are that case for the build. Another repo's copy of the old phase rule is not this change.

**D16 — This revision is not the build.** This spec does not edit the three skill files. AC10 checks that. [plan.md](plan.md) is the one build and should cover FR1 through FR15.

## 8. Open questions

None. A settled cut is not an open question.
