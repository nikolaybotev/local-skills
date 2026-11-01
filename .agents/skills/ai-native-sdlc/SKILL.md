---
name: ai-native-sdlc
description: >-
  Run the software cycle used to build goldvalue in Cursor: a raw prompt
  becomes a GitHub repo with AGENTS.md, REVIEW.md, and
  intent/<change>/{intent,spec,plan}.md, the spec and plan are iterated in
  the chat, a fresh-context subagent reviews each, then another subagent
  builds one pull request per phase when that phase is whole. Use when the user wants to start an app
  or a substantial feature, says intent.md, spec.md, plan.md, AI-native SDLC,
  the playbook, or restart the cycle, or asks to design before coding. Also
  use it when a repo is missing that chain, has only part of it, or already
  has it (as goldvalue does) and a new change should start a new intent
  folder. Skip it for a one-line fix or a typo.
---

# AI-native SDLC

A disciplined way for one person to build software with an agent. Each stage ends in a file the next stage reads. The four stages below are the whole cycle. Do not add stages.

[Goldvalue](https://github.com/nikolaybotev/goldvalue) is where this was proved, in GoldValue SDLC. That session followed [The AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) and kept the changes that worked. Follow that sequence.

1. **Bootstrap.** First commit: `AGENTS.md`, `REVIEW.md`, `README.md`, and `intent/<change>/` with the verbatim prompt plus draft `spec.md` and `plan.md`. Questions may still be open.
2. **Spec and plan.** Iterate both in the chat. Corrections become decisions and plan steps. Commit each draft. Check facts before they harden. Leave a question open until it is answered or shelved.
3. **Independent review, then the build gate.** A fresh-context subagent reads the spec against the intent, then another reads the plan against the spec. Apply the findings. The build starts when they say to build and nothing still needs them.
4. **Build.** A fresh-context subagent takes a chunk of phases. Each phase is one pull request when that phase is whole. The subagent should still be the one that merges. After its steps and definition of done are met and the checks the plan names have succeeded, including when the repo names no required check, it merges that pull request. A failed, cancelled, or still-running check is not a stop; the phase should not merge and the next phase should not start until the check is fixed and re-run. The release should not publish until the remaining phases of that change have landed; the plan should say how publishing waits in that repo. A phase that publishes nothing may land. A release the plan sequences as its own release may publish. The parent reports what landed and launches the next chunk.

A later idea starts again at 1 in a new `intent/<change>/`. The sections below are the detail for these four. Do not treat this list as a second procedure.

## Small intent

When an intent arrives already labeled `small intent`, every thread for that intent uses Composer 2.5 for spec, plan, build, and all review threads, unless the intent names a model. Otherwise the SDLC is unchanged. One process. Do not skip steps.

## Named model

When an intent names a model for some threads or for all of them, that choice wins over this skill's defaults, including [Small intent](#small-intent). If the thread's model cannot be launched—named in the intent or set by this skill—the thread stops and asks; do not fall back to another model.

Read [references/templates.md](references/templates.md) when writing the three files. Copy [assets/AGENTS.md](assets/AGENTS.md) and [assets/REVIEW.md](assets/REVIEW.md) only when those files are missing, then fill every placeholder from this repo. For build and build-review, load and follow the installed **build-practices** skill; do not paste its text into product repos. When the intent is labeled `small intent`, run every build and build-review thread on Composer 2.5 unless the intent names a model. Read [references/goldvalue.md](references/goldvalue.md) for the committed shape of that one run.

## File names to use

Write these from the first commit. Do not create `CLAUDE.md` or `.claude/skills/` and wait to be told to rename them. Goldvalue did that rename in a second commit because the first draft had followed the blog's names. That correction is already made here.

| Write this | Do not write the blog's name |
|---|---|
| `AGENTS.md` at the repo root | `CLAUDE.md` |
| `.agents/skills/` | `.claude/skills/` |
| `intent/<change>/intent.md`, `spec.md`, and `plan.md` together | a lone `intent.md` at the root |
| A committed `plan.md`, then a fresh-context subagent per phase | plan mode as the only plan |

`REVIEW.md` goes at the repo root too. If a repo you are adopting already has `CLAUDE.md`, fold anything unique into `AGENTS.md` and treat `AGENTS.md` as the file agents read.

## Starting point

Look at the repo before writing. Do the first step below that is not already done.

| What you find | What to do |
|---|---|
| No repo, or they asked for a new one | Create it, then start at [Prompt to first commit](#prompt-to-first-commit) |
| Code, and none of the files | Add the layout around the code. The intent describes the change they asked for, not a retelling of the existing product |
| Some of the files, scattered or stale | Keep what is useful. One chain for the current change. Move a loose `intent.md`, `spec.md`, or `plan.md` into `intent/<slug>/`. If `CLAUDE.md` and `AGENTS.md` both exist, fold unique facts into `AGENTS.md` |
| The chain is already there, as in goldvalue | Do not bootstrap again. A new idea is a new `intent/<slug>/` that links to the folder it builds on. v1.2 was that |

A chunk whole enough to ship by itself should be its own intent and should point at the existing new-intent sentence. A release this plan already sequences should stay on this intent.

A skill that ships with the product lives in `.agents/skills/<name>/`. If it should be available in this workspace, symlink it from the workspace `.agents/skills/`.

## Prompt to first commit

Goldvalue's product prompt mixed the idea with design questions and asked for four things at once: record the prompt in `intent.md`, draft `spec.md`, draft `plan.md`, and iterate the spec and the plan together because the prompt was already both. Then create the repo, put it on GitHub, commit the draft. When the intent is labeled `small intent`, run bootstrap drafting on Composer 2.5 unless the intent names a model.

1. Write `intent/<slug>/intent.md`. Their prompt goes under "Original prompt" verbatim. If the idea came from an earlier chat, paste that exchange under "Source transcript" and keep interpretation out of that section. goldvalue's v1.2 did this.
2. Draft `spec.md` and `plan.md` in the same session. Answer a design question when you can check it. Leave it open in the spec when you cannot. Number the answers you do make (`D1`, `D2`, …), with the reasoning, so a later phase does not re-litigate them.
3. Check a fact the design stands on before it hardens. In that session, CORS, the BIS quote direction, coverage dates, and a gzip size were wrong until they were probed or measured. Record what you checked.
4. If there is no repo: `github.com/<owner>/<name>/` in this workspace, owner from `gh api user --jq .login` unless they named one. Goldvalue was created public because they said public. If they have not said public or private, ask once. `git init`, `gh repo create`, push `main`.
5. The first commit uses the names in the table above. It holds `intent/<slug>/{intent,spec,plan}.md`, `AGENTS.md`, `REVIEW.md`, `README.md`, and any code they asked to move in. A skill that ships with the product goes in `.agents/skills/<name>/`. If it should also be available in this workspace, symlink it from the workspace `.agents/skills/`.
6. `AGENTS.md` is commands, conventions, architecture, and things agents get wrong, short enough to read at the start of a session. Specialize `REVIEW.md` to this product before the first pull request. Goldvalue's Bugs and Important lines name a wrong gold value and a broken CSV contract. Write the equivalent for this repo.

## Iterate in the chat

When the intent is labeled `small intent`, run every spec-and-plan thread on Composer 2.5 unless the intent names a model (see [Small intent](#small-intent) and [Named model](#named-model)).

They correct you in conversation. Write the correction into the spec or the plan and commit the draft. Goldvalue went through several numbered drafts this way (Preact, sheet-wide currency, the parity table, DEM, CSV) while an open question stayed open until it was answered.

If two requirements contradict, the part this release will not ship should be a cut, not a later tag on the same spec. A release this same plan already sequences, and an item the plan already marks optional, should stay on this intent. Staying is not an exemption from a recorded cut. Postponed work should point at the existing new-intent sentence.

The spec did that for multi-currency (history of that run, not the rule).

The spec wins over the plan. If the plan is the one that is right, change the spec first. During build, follow the installed **build-practices** skill. When a detail the spec does not decide and that leaves this release's goals and acceptance intact, note it under the phase and continue. A goal change, an owner gate, or an unlocked choice about what a feature calculates or promises should be a stop, and the phase should not merge until it is settled. An amendment that keeps the goals, including a wrong locked formula or acceptance match, should be written into the spec and the plan in the same commit, and the coverage row should move in that commit. A procedure fix that does not contradict the spec should be recorded in the plan only. Where a repo handbook states a shorter phase rule or a different departure procedure, this skill's whole-phase rule, release wait, and three moves should take precedence over build-practices' plan-only departure line.

## Last scrutiny, then the build

They asked "are we at the build gate?" The answer in that session was: the gate is their approval of `plan.md`.

They then asked for the last scrutiny before opening it, in this order. When the intent is labeled `small intent`, run every fresh-context subagent in this section on Composer 2.5 unless the intent names a model for that thread.

1. A fresh-context subagent reads `spec.md` against `intent.md` and flags what is unclear, missing, or in conflict. It does not edit.
2. You apply the findings you agree with, and you re-check any external fact the review disputes.
3. A fresh-context subagent does the same for `plan.md` against the spec.
4. You apply those findings the same way.
5. Stop only if something demands their attention. They said that in those words. The LBMA license was that stop: publishing the prices was not a decision to bury in a draft. It was written up as a gate in the plan, they resolved it, and the resolution was committed into the spec and the plan before Phase 0.
6. When they say to build, a fresh-context subagent implements the plan. Use the model the intent names for that thread when it does; otherwise when the intent is labeled `small intent`, use Composer 2.5; otherwise if they name a model in chat, use it (that session used Claude Sonnet).

Do not run a second session against the same files. Two writers edited `spec.md` at once in that chat, and one had to stand down.

## Build

Hand a fresh-context subagent a chunk of the plan, not the design chat. Goldvalue sent Phases 0–2 together, then 3a–3c, then 4a–5, then 6a–6c. Use the model the intent names for that thread when it does; otherwise when the intent is labeled `small intent`, use Composer 2.5; otherwise use the session's default model unless they name one in chat. They named Claude Sonnet for the build in that session, and the parent did not substitute another model when that launch failed. It stopped and asked.

The subagent works on its own. The prompt it was given:

- Read `AGENTS.md`, `REVIEW.md`, load and follow the **build-practices** skill, the spec, and the plan, including deviations already recorded in `plan.md`. Use this repo's `AGENTS.md` for commands and the required check names for merge.
- Do not ask questions. When the choice leaves this release's goals and acceptance intact and the spec does not decide that detail, make the most conservative choice consistent with the spec, note it in `plan.md` under the phase, and continue. A wrong locked formula or locked sentence is an amendment that keeps the goals in the same commit, not a note and continue.
- A choice that would ship a slice, leave a best effort or a stub on this intent, skip a test until an unscheduled follow-up, or write a "future phase" sentence should be a cut. The note should say what closed, that part should close, and the build should continue only on the whole remainder. A phase in one of those cases should not be treated as done. A sequenced release or an optional item that cannot ship whole should be the same cut, and the intent should close on what remains.
- A goal change, an owner gate, or an unlocked choice about what a feature calculates or promises should be a stop, and the phase should not merge until it is settled. It is not a conservative choice.
- An amendment that keeps the goals should be written into the spec and the plan in the same commit, and the coverage row should move in that commit. An amendment that drops a goal is a cut. Putting a mistaken cut back before the release boundary should stay on this intent, and after the release boundary it should point at the existing new-intent sentence. Where the plan uses no release tag, the Finished header is the release boundary.
- Where a repo's own handbook, such as `AGENTS.md` or the build-practices skill, states a shorter phase rule or a different departure procedure, this skill's rule that a phase lands when that phase is whole, the wait until the remaining phases have landed, and those three moves should take precedence over build-practices' plan-only departure line.
- Text that acceptance will match exactly should enter the spec in that same commit. A procedure fix that does not contradict the spec should be recorded in the plan only. A commit that mixes a fix with a new requirement, or with a rewrite of a settled claim, should split, and the new part should point at the existing new-intent sentence.
- When the remainder has landed, or when a cut leaves nothing to ship, set Status to Finished on `intent.md`, `spec.md`, and `plan.md`. A superseded step should stop reading as an order. The build note should name which definition of done was met. A session-start line naming the current change, such as in `AGENTS.md`, should be updated in that same change. A settled cut should not stay in the open-questions list.
- Each pull request body lists the plan steps done and the definition-of-done evidence.
- Update `AGENTS.md` as commands and conventions land.
- Reply with the merged pull request numbers, CI status, deviations recorded, and anything that needs the owner.

The parent does not review the diff and does not merge those pull requests. It launches the next chunk when the report comes back, and it tells the user what landed. It stops when something needs them: the LBMA license, the GitHub Pages setting, a model they named hitting its budget.

The one exception was a subagent that died on a usage limit with a pull request still open. The parent merged once the checks the plan names have succeeded, and launched the remaining phase.

A phase is whole when its steps and definition of done are met, the checks the plan names have passed, and it does not demote the rest. Demoting the rest includes leaving a best effort, a stub, or a smaller promise than the spec still claims, and leaving an already-shipped path unable to run until a later phase; cut that part and the remainder may ship. A test that only restates expected numbers should be a cut. A control this release does not offer should stay off the shipped surface, including a parameter, a dead flag, or a half-wired path. A phase that changes a surface the tree already describes, such as `README.md` or `AGENTS.md`, should update that description in the same change. A finished control's non-goal should stay a non-goal. A job that publishes on merge should not publish until the remaining phases of that change have landed. A merge onto the branch that runs the publish job is a publish. Waiting means holding that merge, or changing the job in the same change, until the remaining phases have landed. Accepting the automatic tag is not a wait. The plan should say how publishing waits in that repo. A phase that publishes nothing may land. A release the plan sequences as its own release may publish. A contract or output that an already-shipped surface emits should land with the surface that uses it when a phase would otherwise publish the contract alone. Evidence this environment cannot collect should be recorded as an owner check, not marked done, and it should not by itself hold a phase whose other checks are met.

Goldvalue's `deploy-pages` runs on push to `main` and on a daily schedule.

The Phase 5 check for two scheduled runs is that cron, not the push (history of that run, not the rule).

## The next change

A new idea starts at [Prompt to first commit](#prompt-to-first-commit) in a new `intent/<slug>/` that links to the folder it builds on. Do not rewrite an old intent so that it means the new idea.

## Commit

Commit each draft and each finished phase. Do not commit secrets, caches, or generated build output. Do not force-push. The artifacts describe the product. They do not narrate how the previous draft was edited.
