# spec.md — Ship the release whole

| | |
|---|---|
| Derived from | [intent.md](intent.md) (2026-11-01) |
| Status | Finished |
| Stage | 2 · Design |

## 1. Summary

The ai-native-sdlc skill should tell a reader to ship one intent whole. A build should continue only while this release's goals and acceptance stay intact. A slice or a later tag on this spec should be a cut. A whole phase may land on its own. A job that publishes on merge should not publish until the remaining phases of that change have landed. Postponed work should point at the skill's existing new-intent sentence.

This revision does not edit the skill. [plan.md](plan.md) is the one build for that edit. It should not add a stage. The sentences in the intent are the direction. The requirements below are what the skill should tell a reader, in "should" and "should not".

Read on this branch from `.agents/skills/ai-native-sdlc/`. Those three files match `7e7c572`.

## 2. Goals and non-goals

**Goals**

- G1. An undecidable choice should continue only when this release's goals and acceptance stay intact, and only for a detail the spec does not decide. A slice, a best effort, a stub, a test skipped until an unscheduled follow-up, or a "future phase" sentence should be a cut. A goal change, including an unlocked choice of what a feature calculates or promises, or an owner gate, should be a stop. A wrong locked formula or locked sentence should be an amendment in the same commit.
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

- The choice is a detail the spec does not decide, and the goals and acceptance stay intact. The agent should note it in plan.md under the phase, and continue.
- The choice would ship a slice, leave a best effort or a stub, skip a test until an unscheduled follow-up, or add a "future phase" sentence. The agent should cut that part, record the cut, and continue only on the whole remainder.
- The choice would change the goals, including an unlocked choice of what the feature calculates or promises, or it is an owner gate. The agent should stop, and the phase should not merge until it is settled.
- A locked formula or locked sentence is wrong. The agent should amend it under FR5 in the same commit, not note it and continue.
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
- `README.md`, and within it only the ai-native-sdlc blurb
- `AGENTS.md`, and within it only the current-change line that says `The current change is documented`
- `intent/ship-whole/intent.md`, `intent/ship-whole/spec.md`, and `intent/ship-whole/plan.md`, for the three headers and this plan's landing note, in the same commit as that build

The Phase 0 diff, from the revision commit `docs: apply the ship-whole plan review` through the landing commit, should include every file above and no other path. A check of only the last commit is not enough. Read `README.md` and `AGENTS.md` before editing them. Only the current-change line in `AGENTS.md` should change. A historical mention of `intent/config-as-code/` on the architecture line should stay. The current-change line should name `intent/ship-whole/` as Finished. Only the ai-native-sdlc blurb in `README.md` should change.

FR2. Normative text this change adds or rewrites should use "should" and "should not". The three skill files should not contain the three words named in the intent's constraints. In `references/templates.md`, the placeholder under `## Constraints and principles` should be `What should stay true`. The placeholder under `## Open questions (carried into spec.md)` should say `spec should answer`. No other sentence should be rewritten only to soften its voice. AC9 does not forbid these edits.

FR3. These should stay, and this change should not add a second copy of them:

- The cycle summary's existing new-intent sentence.
- The section "The next change".
- "Do not ask questions."
- "The parent does not review the diff and does not merge those pull requests."
- "Skip it for a one-line fix or a typo."

The usage-limit exception should stay the one case the parent may merge. The clause `was green` should not remain. That sentence should say the parent merges once the checks the plan names have succeeded. `usage limit` should remain.

The description line that says `builds one pull request per phase` should say one pull request per phase when that phase is whole. It should not keep the shorter phrase as the only limit, and it should not grow a second procedure. This description sentence is part of FR3. AC9 should exempt it. The section "The next change" should keep its one sentence that begins `A new idea starts at`. The cycle summary's new-intent sentence is the one that contains `starts again at 1`, and the skill should keep that sentence once.

### Continue, cut, and stop

FR4. The build bullet that now says to make the most conservative choice consistent with the spec, note it in `plan.md` under the phase, and continue, should be rewritten so the ship-whole rule is that same instruction. The old sentence that begins `If something is undecidable` should not remain. The location clause `under the phase, and continue` should remain. The rewrite should tell the reader:

- When the choice leaves this release's goals and acceptance intact, and the spec does not decide that detail, the agent should make the most conservative choice consistent with the spec, note it in `plan.md` under the phase, and continue.
- A wrong locked formula or locked sentence is an amendment under FR5 in the same commit, not a note and continue.
- A choice that would ship a slice, leave a best effort or a stub on this intent, skip a test until an unscheduled follow-up, or write a "future phase" sentence should be a cut. The agent should record the cut, close that part off, and continue only on the whole remainder.
- A choice that changes the goals, or an owner gate, should be a stop. Merge should wait until it is settled. An unlocked choice about what a feature calculates or promises should be that kind of stop, not a conservative choice.
- A phase that does one of those cut cases should not be treated as done.
- A failed, cancelled, or still-running check is not a stop. The phase should not merge, and the next phase should not start. The check should be fixed and re-run. `cancelled`, `still-running`, `not a stop`, and `the next phase should not start` should be on that same line.

FR5. An amendment that keeps the goals should be written into the spec in the same commit as the plan's acceptance-criteria coverage row. An amendment that drops a goal is a cut. Editing the spec should not make that drop look consistent. A wrong sentence the release still needs is an amendment, not a cut. Putting a mistaken cut back before the release tag should stay on this intent. After the tag, it should point at the existing new-intent sentence. Where the plan does not use a release tag, the Finished header is that boundary. A cut should be named in `plan.md` in that same commit. The note should say what closed. It should not be left as an empty placeholder. The existing sentences `The spec wins over the plan.` and `If the plan is the one that is right, change the spec first.` should stay. The clause `record plan departures in` should not remain.

The subagent prompt should carry this same-commit amendment and the three moves: an amendment that keeps the goals, an amendment that drops a goal, and putting a mistaken cut back before or after the release boundary. Those three moves should sit inside the prompt, between `The prompt it was given:` and `The parent does not review`, and the prompt should contain `keeps the goals`, `drops a goal`, and `mistaken cut`. The same span should contain `the spec does not decide`, `wrong locked formula`, and `under the phase, and continue`.

Text that acceptance will match exactly should enter the spec in that same commit.

### One build

FR6. Cycle summary item 4, the line with `**Build.**`, should say that a phase is its own pull request only when that phase is whole, and that the release waits until the remaining phases have landed. It should carry the no-required-check finish and the failed-check rule in FR4, on that same item line, including `no required check` and `not a stop`. It should not keep "merge when CI is green" as the only line. The sentence `The subagent merges it when CI is green` should not remain. The subagent should still be the one that merges. The parent should still launch the next chunk after a whole phase lands. Item 4 should not say the release ships at the first phase.

Where a repo's own handbook, such as `AGENTS.md` or the build-practices skill, states a shorter phase rule or a different departure procedure, this skill's rule that a phase lands when that phase is whole, the wait until the remaining phases have landed, and the three moves should take precedence. That sentence should be in the subagent prompt. This change should not edit build-practices or another repo's handbook.

FR7. The Build section should say what "whole" means. A phase is whole when its steps and its definition of done are met, the checks the plan names have succeeded, and it does not demote the rest. Demoting the rest includes leaving a best effort, a stub, or a smaller promise than the spec still claims, and leaving an already-shipped path unable to run until a later phase. A control this release does not offer should stay off the shipped surface, including a parameter, a dead flag, or a half-wired path.

The definition of done should be a command or inspection the phase can show at its commit, including when the repo names no required check. Required checks are the merge gate. A job the plan does not name as required is not part of done. The definition of done should exercise the acceptance. A test that only restates expected numbers should be a cut. Evidence the environment cannot collect should be recorded as an owner check, not marked done, and it should not by itself hold a phase whose other checks are met.

A one-phase plan should be one pull request. A failed, cancelled, or still-running check the plan names should not merge and should not start the next phase.

FR8. A phase may land when it is whole and does not demote the rest. A job that publishes on merge, including a tag, a release, or a deploy of the surface the owner sees, should not publish until the remaining phases of that change have landed. A merge onto the branch that runs the publish job is a publish. Waiting means holding that merge, or changing the job in the same change, until the remaining phases have landed. Accepting the automatic tag is not a wait. The plan should say how publishing waits in that repo. A phase that publishes nothing may land. A release the plan sequences as its own release may publish. A contract or output that an already-shipped surface emits should land with the surface that uses it, not in an earlier phase that publishes the contract alone.

The scheduled-runs sentence, `The Phase 5 check for two scheduled runs is that cron, not the push`, should stay, and the same line should be marked `history of that run, not the rule`. The instruction that the subagent waits for that run and checks production should be replaced, so `waits for that run and checks production` does not remain as an order. The publish rule above is the order. `The spec did that for multi-currency.` should stay, and that same line should carry the history mark.

FR9. The skill should say that a chunk whole enough to ship by itself should be its own intent. That sentence should point at the existing new-intent sentence. It should not restate the procedure, and it should not mean that this build is one pull request. This is not the rejected alternative of one pull request for the whole build.

### Later work

FR10. The iterate section should no longer tell the reader to tag the later items on the same spec. The current sentence that says to split a first release from a later one and tag the later items should be replaced. "The spec did that for multi-currency" should stay and should be marked `history of that run, not the rule`. It should not remain a live example of tagging later items.

When two requirements contradict, the part this release will not ship should be a cut under FR4. It should not stay on this spec as a later tag. `tag the later items` should not remain. A release this same plan already sequences, and an item the plan already marks optional, should stay on this intent. Staying means it is not moved to a new intent. Staying is not an exemption from a recorded cut. If it cannot ship whole, it is a cut under FR4, which closes that part and points at the existing new-intent sentence. A finished control's non-goal should stay a non-goal. It should not become postponed work, and it should not start a new intent until someone asks. Postponed work should point at the existing new-intent sentence and should not be added to the closed intent. A settled cut should not stay in the open-questions list.

FR11. `references/templates.md` should no longer say "Later-release items tagged", "tagged as later", or "untagged requirements belong". The release-phasing placeholder should say that this release is what the plan still claims, that a sequenced release and an optional item stay on this intent, the sentence `Staying is not an exemption from a recorded cut`, and that postponed work points at the skill's new-intent sentence and is not tagged on this spec. It should not say that an optional item can be dropped without a new intent. The repeated phase block should stay. The open-questions placeholder should say a settled cut is not an open question.

FR12. In `references/goldvalue.md`, mark the departures clause, not the whole of item 8. The clause is `Departures are in that phase's build notes inside `plan.md``. The mark `history of that run, not the rule` should sit on that clause, after it and before the commands sentence. `Each phase was one PR with a definition of done` should stay the rule. ``AGENTS.md` gained the commands and the pitfalls in the same changes.` should stay the rule. Item 9, the line that says `from the same intent folder`, should carry that same history mark, and the same line should say that a release this same plan already sequences is not forbidden by the mark. The following item should stay, including `restarted the cycle`. The layout tree is not that sentence. The file should not restate the new-intent procedure.

### Closing, corrections, and the template

FR13. The skill should tell the reader to set Status to Finished on `intent.md`, `spec.md`, and `plan.md` when the remaining phases have landed, or when a recorded cut closes the intent. That teaching should contain `set Status to Finished`. The stage labels should stay `1 · Plan`, `2 · Design`, and `3 · Build`. When a gate passes, a sentence that still says the build is closed until that gate should be updated in that change. A superseded step should not still read as an order. A decision made during the build should be a build note. The note for a landed phase should say which definition of done was met. The landing note in this plan should have `DoD met:` as its first line. In that same Phase 0 commit, the preamble, the text before `## Stops`, should no longer say `It is not Phase 0`, and it should say the steps are `history of that run, not orders`. The numbered steps between `## Phase 0` and the line that starts with `DoD: the inspection` should each contain `Done.`. Each of the lines `1.` through `7.` should still start with its number and should contain `Done.` after it, as in `1. Done.`. A session-start line that names this intent as the current change, such as the line in `AGENTS.md` that says `The current change is documented`, should be updated in that same change so it names `intent/ship-whole/` as Finished. `intent/onboard/` should stay the historical note.

A phase that changes something the tree already describes, such as `README.md` or `AGENTS.md`, should update that description in the same change.

FR14. A procedure fix that does not contradict the spec should be recorded in the plan only. The one-line fix and typo skip in FR3 should stay. A fix should not add a requirement. A commit that mixes a fix with a new requirement, or with a rewrite of a settled claim, should split, and the new part should point at the existing new-intent sentence. A contradicting departure that keeps the goals should follow FR5.

FR15. The plan block in `references/templates.md` should change as follows, and the starting status should stay Draft.

- The departure line should carry the spec-amendment sentence: an amendment that keeps the goals is written into the spec in the same commit, and the coverage row moves in that commit. An amendment that drops a goal is a cut. A procedure fix that does not contradict the spec is recorded in the plan only.
- The definition-of-done line should allow the no-required-check case: a command or inspection shown at the commit that exits non-zero when unmet.
- The template should show `| Status | Finished |` as the closed value, with Draft remaining the start. The line that exits non-zero on failure is the definition-of-done line this change rewrites. The departure line that says `whenever implementation departs` is the line this change rewrites.
- It should show a named-cut example that says what closed and points at the existing new-intent sentence.
- The build-notes block inside the copyable fence should hold the heading `### Build notes (Phase 0)` and the placeholder `<name which definition of done was met>`, and no other sentence. It should not contain `Added only after the phase lands`. The instruction `A phase that is not yet built has no build notes.` should stay outside that fence. When the phase lands, the note should name which definition of done was met.

## 6. Acceptance criteria

| ID | Criterion | Check |
|---|---|---|
| AC1 | FR4 is true. The old sentence that begins `If something is undecidable` is absent. `under the phase, and continue` remains for a detail the spec does not decide. "Do not ask questions." is still there. A failed, cancelled, or still-running check is not a stop, on that same line. | Read the Build bullet and summary item 4. |
| AC2 | FR5 is true, including the three moves inside the subagent prompt, the same commit for the spec and the coverage row, and exact-match text entering the spec in that commit. | Read the prompt between `The prompt it was given:` and `The parent does not review`. |
| AC3 | FR3, FR6, and FR7 are true. The description says `when that phase is whole`. `The subagent merges it when CI is green` is absent. Who merges is unchanged: the subagent merges, and the parent sentence is unchanged. The usage-limit exception stays, and `was green` is rewritten to the checks the plan names have succeeded. | Read the description, summary item 4, and the Build section. Diff the parent sentence against `7e7c572`. |
| AC4 | FR8 and FR9 are true. The scheduled-runs sentence remains and that line is marked `history of that run, not the rule`. `waits for that run and checks production` does not remain. | Read the Build section and the deploy paragraph. |
| AC5 | FR10 is true, including `Staying is not an exemption from a recorded cut`, that a non-goal stays a non-goal, and that a settled cut is not an open question. `tag the later items` is absent. The multi-currency sentence is marked `history of that run, not the rule` on that line. The new-intent sentence and "The next change" each stay once. | Search `SKILL.md`. Diff those two spots against `7e7c572`. |
| AC6 | FR2, FR11, and FR15 are true. The placeholders are `What should stay true` and `spec should answer`. The later-tag phrases are absent. The plan template has the departure sentence, the no-required-check definition of done, a Finished header, a named cut, and a build-notes fence that holds `<name which definition of done was met>`. | Search `references/templates.md`. |
| AC7 | FR12 is true. The departures clause and item 9 are marked `history of that run, not the rule`. The one-PR sentence and the commands sentence stay the rule. `restarted the cycle` remains. | Read `references/goldvalue.md`. |
| AC8 | FR13 and FR14 are true. Finished applies when the remaining phases have landed or a recorded cut closes the intent. The one-line skip remains. No new stage name appears. | Read `SKILL.md`. |
| AC9 | The three skill files do not contain the three words named in the intent's constraints, in any case. A sentence not covered by FR2, the FR3 description line, the FR3 usage-limit rewrite, or FR4–FR15 is unchanged from `7e7c572`. The check is line by line. The FR2 placeholders, the FR3 description line, the usage-limit line, and the template lines FR11 and FR15 name are exempt from that unchanged-sentence check. | Search the three files. Diff each untouched line against `7e7c572`. |
| AC10 | This revision does not edit the three skill files. The build in [plan.md](plan.md) does. | `git diff --name-only` against the parent of this revision is only `intent/ship-whole/`. |

## 7. Design decisions

**D1 — Continue only on an intact release.** Decision 1 in [intent.md](intent.md). A conservative choice that leaves the goals and acceptance intact, and that the spec does not decide, should be noted in plan.md under the phase, and the build should continue. After a cut, continue should apply to the whole remainder. Rejected: continue through a slice. Rejected: stop on every undecidable detail. Rejected: noting a wrong locked formula and continuing.

**D2 — A goal change stops.** A choice that changes the goals, or an owner gate, should be a stop, and merge should wait. An unlocked choice about what a feature calculates or promises is that stop. Note and continue applies only to a detail the spec does not decide. A wrong locked formula or locked sentence is an FR5 amendment in the same commit, not a conservative continue. Rejected: picking an unlocked formula, merging it, and calling that conservative. Rejected: noting a wrong locked formula and continuing.

**D3 — One build is the plan's phases.** Decision 2. A whole phase should still be its own pull request, and the parent should still start the next chunk. The release should wait until the remaining phases have landed. Rejected: one pull request for the whole build. That rejected alternative is not kept. FR9 is a different rule: a chunk whole enough to ship by itself should be its own intent, and it should not mean this build is one pull request.

**D4 — Who merges stays.** The summary may change when a phase is allowed to merge. It should not change the actor. The parent sentence should stay. The usage-limit exception should stay the one case the parent may merge, and its `was green` clause should be rewritten so the parent merges once the checks the plan names have succeeded. Rejected: settling, in this change, whether a parent or a subagent merges.

**D5 — Publish is one sentence.** A phase may land when it is whole and does not demote the rest. A job that publishes on merge should not publish until the remaining phases of that change have landed, and the plan should say how publishing waits. A merge onto the branch that runs the publish job is a publish. Waiting means holding that merge, or changing the job in the same change, until the remaining phases have landed. Accepting the automatic tag is not a wait. A phase that publishes nothing may land. A release the plan already sequences as its own release may publish. Rejected: the word "gated" with no applicable sentence. Rejected: holding every phase until the last one. Rejected: landing a contract in an earlier phase than the surface that uses it. Rejected: accepting the automatic tag and calling that a wait. The old deploy-on-every-merge instruction is replaced. It is history of that run, not this sentence.

**D6 — Later tags retire, and staying is not an exemption.** Decision 3. "Tag the later items" and "untagged requirements belong" should go. A sequenced release and an optional item stay on this intent, which means they are not moved to a new intent. If one cannot ship whole, it is a cut under FR4. Rejected: FR11 saying an optional item can be dropped without a new intent. Rejected: leaving a later tag on the closed spec. Rejected: opening a new intent for a finished control's non-goal.

**D7 — Point without restating.** Postponed work and a chunk that should be its own intent should point at the existing new-intent sentence. FR3 names the sentence and the section that should stay. Rejected: a second copy of that procedure in the skill, the template, or `references/goldvalue.md`.

**D8 — Same commit for the spec and the coverage row.** An amendment that keeps the goals moves the spec and the plan's coverage row in one commit. An amendment that drops a goal is the cut, and editing the spec does not make the drop consistent. A wrong locked formula or locked sentence is this amendment, not a note and continue. Putting a mistaken cut back before the release boundary stays on this intent; after that boundary it points at the new-intent sentence. Rejected: a plan-only note when the spec is wrong. Rejected: a quiet spec edit that drops a goal. Empty cut placeholders are the failure this rejects. A contradicting formula left in the spec while the plan said otherwise is the same failure.

**D9 — Finished is a status, not a stage.** Status should become Finished when the remaining phases have landed or a recorded cut closes the intent. The stage labels should stay. A session-start line that still names the intent as the current change should be updated in that change. A landed phase's build note should say which definition of done was met. Rejected: a fifth stage. Rejected: headers left at Draft because the last phase was cut and nothing new landed. Shipped intents whose headers still say Draft are the case.

**D10 — A procedure fix is a plan record.** A fix that does not contradict the spec is recorded in the plan only. The one-line and typo skip stays. A fix should not add a requirement. A mixed commit splits. Rejected: a spec edit for every procedure fix. Rejected: a new requirement riding along in the fix commit. A repair written only into a handbook, and not into the plan, is the case for recording it in the plan.

**D11 — The definition of done is shown at the commit.** It is a command or inspection, including when the repo names no required check. Required checks are the merge gate. A job the plan does not name is not part of done. A test that only restates expected numbers is a cut. Evidence this environment cannot collect is an owner check, not marked done, and it does not by itself hold the phase. Rejected: setting done to a remote job the plan does not require. Rejected: merging while a named check has failed, was cancelled, or is still running. A cancelled check is in that class. It is not an owner stop. Rejected: calling that wait a stop, which would freeze a fix the phase can re-run.

**D12 — Voice, and the template placeholders.** The continue bullet is in scope because leaving it unchanged would outrank the new line. The two intent-template placeholders that are stronger than "should" are in scope, and they should become `What should stay true` and `spec should answer`. AC9 exempts those lines, the FR3 description line, the usage-limit rewrite, and the other template edits. Other "Do not" sentences are not in scope. The ship-whole rule should stay checkable through FR4's "should not be treated as done". Rejected: a sweep of the skill. Rejected: an acceptance check that fails the placeholder edit it also requires.

**D13 — History is not an order.** The scheduled-runs sentence and the multi-currency sentence should each be marked `history of that run, not the rule` on that same line. The deploy instruction `waits for that run and checks production` should be replaced, not left beside the mark. Goldvalue item 8's mark should sit on the departures clause only. Item 9's mark should sit on the line that says `from the same intent folder`, and it should not forbid a release this plan already sequences. Rejected: leaving the scheduled-runs sentence as the concrete order beside the new rule. Rejected: marking the whole of item 8, including the one-PR fact and the commands fact. Rejected: deleting the historical fact.

**D14 — Demotion includes a broken shipped path.** Leaving an already-shipped path unable to run until a later phase demotes the rest, even when the spec of that phase allowed the break. A control this release does not offer stays off the shipped surface. Rejected: calling that phase whole because its own steps passed.

**D15 — Described surfaces move in the same change.** A phase that changes something `README.md` or `AGENTS.md` already describes should update that description then. This repo's skill blurb and the current-change line are that case for the build. The architecture line should stay. Another repo's copy of the old phase rule is not this change.

**D16 — This revision is not the build.** This spec does not edit the three skill files. AC10 checks that. [plan.md](plan.md) is the one build and should cover FR1 through FR15. The plan's inspection should find the revision commit by the subject `docs: apply the ship-whole plan review` and should diff the Phase 0 range after that commit. It should include every FR1 path and no other path. Untouched lines in the three skill files should match `7e7c572`.

## 8. Open questions

None. A settled cut is not an open question.
