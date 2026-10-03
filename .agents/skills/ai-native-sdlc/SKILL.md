---
name: ai-native-sdlc
description: >-
  Run the software cycle used to build goldvalue in Cursor: a raw prompt
  becomes a GitHub repo with AGENTS.md, REVIEW.md, and
  intent/<change>/{intent,spec,plan}.md, the spec and plan are iterated in
  the chat, a fresh-context subagent reviews each, then another subagent
  builds one pull request per phase. Use when the user wants to start an app
  or a substantial feature, says intent.md, spec.md, plan.md, AI-native SDLC,
  the playbook, or restart the cycle, or asks to design before coding. Also
  use it when a repo is missing that chain, has only part of it, or already
  has it (as goldvalue does) and a new change should start a new intent
  folder. Skip it for a one-line fix or a typo.
---

# AI-native SDLC

A disciplined way for one person to build software with an agent. Each stage ends in a file the next stage reads. The four stages below are the whole cycle. Do not add stages.

[Goldvalue](https://github.com/nikolaybotev/goldvalue) is where this was proved, in [GoldValue SDLC](15bf70a9-b9c7-4696-b127-3fb1bfb0231e). That session followed [The AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) and kept the changes that worked. Follow that sequence.

1. **Bootstrap.** First commit: `AGENTS.md`, `REVIEW.md`, `README.md`, and `intent/<change>/` with the verbatim prompt plus draft `spec.md` and `plan.md`. Questions may still be open.
2. **Spec and plan.** Iterate both in the chat. Corrections become decisions and plan steps. Commit each draft. Check facts before they harden. Leave a question open until it is answered or shelved.
3. **Independent review, then the build gate.** A fresh-context subagent reads the spec against the intent, then another reads the plan against the spec. Apply the findings. The build starts when they say to build and nothing still needs them.
4. **Build.** A fresh-context subagent takes a chunk of phases. Each phase is one pull request. The subagent merges it when CI is green, then starts the next phase. The parent reports what landed and launches the next chunk.

A later idea starts again at 1 in a new `intent/<change>/`. The sections below are the detail for these four. Do not treat this list as a second procedure.

Read [references/templates.md](references/templates.md) when writing the three files. Copy [assets/AGENTS.md](assets/AGENTS.md) and [assets/REVIEW.md](assets/REVIEW.md) only when those files are missing, then fill every placeholder from this repo. Read [references/goldvalue.md](references/goldvalue.md) for the committed shape of that one run.

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

A skill that ships with the product lives in `.agents/skills/<name>/`. If it should be available in this workspace, symlink it from the workspace `.agents/skills/`.

## Prompt to first commit

Goldvalue's product prompt mixed the idea with design questions and asked for four things at once: record the prompt in `intent.md`, draft `spec.md`, draft `plan.md`, and iterate the spec and the plan together because the prompt was already both. Then create the repo, put it on GitHub, commit the draft.

1. Write `intent/<slug>/intent.md`. Their prompt goes under "Original prompt" verbatim. If the idea came from an earlier chat, paste that exchange under "Source transcript" and keep interpretation out of that section. v1.2 did this with the Duffy Way chat.
2. Draft `spec.md` and `plan.md` in the same session. Answer a design question when you can check it. Leave it open in the spec when you cannot. Number the answers you do make (`D1`, `D2`, …), with the reasoning, so a later phase does not re-litigate them.
3. Check a fact the design stands on before it hardens. In that session, CORS, the BIS quote direction, coverage dates, and a gzip size were wrong until they were probed or measured. Record what you checked.
4. If there is no repo: `github.com/<owner>/<name>/` in this workspace, owner from `gh api user --jq .login` unless they named one. Goldvalue was created public because they said public. If they have not said public or private, ask once. `git init`, `gh repo create`, push `main`.
5. The first commit uses the names in the table above. It holds `intent/<slug>/{intent,spec,plan}.md`, `AGENTS.md`, `REVIEW.md`, `README.md`, and any code they asked to move in. A skill that ships with the product goes in `.agents/skills/<name>/`. If it should also be available in this workspace, symlink it from the workspace `.agents/skills/`.
6. `AGENTS.md` is commands, conventions, architecture, and things agents get wrong, short enough to read at the start of a session. Specialize `REVIEW.md` to this product before the first pull request. Goldvalue's Bugs and Important lines name a wrong gold value and a broken CSV contract. Write the equivalent for this repo.

## Iterate in the chat

They correct you in conversation. Write the correction into the spec or the plan and commit the draft. Goldvalue went through several numbered drafts this way (Preact, sheet-wide currency, the parity table, DEM, CSV) while an open question stayed open until it was answered.

If two requirements contradict, split a first release from a later one and tag the later items. The spec did that for multi-currency.

The spec wins over the plan. If the plan is the one that is right, change the spec first.

## Last scrutiny, then the build

They asked "are we at the build gate?" The answer in that session was: the gate is their approval of `plan.md`.

They then asked for the last scrutiny before opening it, in this order:

1. A fresh-context subagent reads `spec.md` against `intent.md` and flags what is unclear, missing, or in conflict. It does not edit.
2. You apply the findings you agree with, and you re-check any external fact the review disputes.
3. A fresh-context subagent does the same for `plan.md` against the spec.
4. You apply those findings the same way.
5. Stop only if something demands their attention. They said that in those words. The LBMA license was that stop: publishing the prices was not a decision to bury in a draft. It was written up as a gate in the plan, they resolved it, and the resolution was committed into the spec and the plan before Phase 0.
6. When they say to build, a fresh-context subagent implements the plan. They named the model (Claude Sonnet). If they name one, use it.

Do not run a second session against the same files. Two writers edited `spec.md` at once in that chat, and one had to stand down.

## Build

Hand a fresh-context subagent a chunk of the plan, not the design chat. Goldvalue sent Phases 0–2 together, then 3a–3c, then 4a–5, then 6a–6c. Use the session's default model unless they name one. They named Claude Sonnet for the build, and the parent did not substitute another model when that launch failed. It stopped and asked.

The subagent works on its own. The prompt it was given:

- Read `AGENTS.md`, `REVIEW.md`, the spec, and the plan, including deviations already recorded.
- Where the plan and the spec disagree, the spec wins. Record the discrepancy in `plan.md`.
- Do not ask questions. If something is undecidable, make the most conservative choice consistent with the spec, note it in `plan.md` under the phase, and continue.
- Each phase is its own branch and its own pull request. The body lists the plan steps done and the definition-of-done evidence.
- Merge only when CI is green, squash, delete the branch, then update `main` before the next phase. Do not merge red. Fix and push until green.
- Update `AGENTS.md` as commands and conventions land.
- Reply with the merged pull request numbers, CI status, deviations recorded, and anything that needs the owner.

The parent does not review the diff and does not merge those pull requests. It launches the next chunk when the report comes back, and it tells the user what landed. It stops when something needs them: the LBMA license, the GitHub Pages setting, a model they named hitting its budget.

The one exception was a subagent that died on a usage limit with a pull request still open. The parent checked that it was green, merged it, and launched the remaining phase.

Deploy is the workflow already in the repo. After a merge to `main`, the subagent waits for that run and checks production. The parent checks production again before it reports the release. Goldvalue's `deploy-pages` runs on push to `main` and on a daily schedule. The Phase 5 check for two scheduled runs is that cron, not the push.

## The next change

A new idea starts at [Prompt to first commit](#prompt-to-first-commit) in a new `intent/<slug>/` that links to the folder it builds on. Do not rewrite an old intent so that it means the new idea.

## Commit

Commit each draft and each finished phase. Do not commit secrets, caches, or generated build output. Do not force-push. The artifacts describe the product. They do not narrate how the previous draft was edited.
