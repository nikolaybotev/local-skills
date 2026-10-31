# spec.md — Config as code

| | |
|---|---|
| Derived from | [intent.md](intent.md) (2026-10-30) |
| Status | Draft 1 |
| Stage | 2 · Design |

## 1. Summary

Update `cursor-cloud-environments` so it names two routes. Inline-config is `POST /v1/environments`: it snapshots the config and does not follow the repo file. Config as code is the other route, and it is the preferred path for new repos. When a repo has a committed `.cursor/environment.json` and no saved environment, launching a cloud agent or Project on it without naming an environment makes Cursor create one that follows the file.

This draft does not edit the skill. Phase 0 does, in one pull request. The skill stays generic. No new API behavior is added.

## 2. Goals and non-goals

**Goals**

- G1. The skill says it covers inline-config environments created through `POST /v1/environments`, which snapshot the config and do not follow the repo file.
- G2. The skill says Config as code is the other route and points at it as the preferred path for new repos, using the prompt's condition.
- G3. The existing inline procedure and the sentences checked in D3 stay in force.
- G4. `references/api.md` uses the same route names without a new endpoint, field, or error.
- G5. The handbook's active-change pointer, the review sheet's skill-edit sentence, and the README tree name this folder.

**Non-goals**

- Editing `scripts/environments.py` or any skill besides `cursor-cloud-environments`.
- Adding an endpoint, a request field, a response field, or a script command for Config as code.
- Writing `.cursor/environment.json`, or launching a cloud agent or Project, from this skill.
- Rewriting the README skill blurb. It still describes the worker procedure, and that procedure remains.
- Rulesets, required status checks, `workflow_dispatch`, CodeQL, or a workflow edit.
- Running either installer against a real home.
- A person, a machine, a host, or a model name in the skill, `references/api.md`, `AGENTS.md`, `REVIEW.md`, or `README.md`.
- Editing `intent/onboard/` or any other historical intent folder.

**Release phasing.** Untagged requirements belong to Phase 0, the only phase. There is no later-release tag.

## 3. Principles

- P1. Do not invent API behavior. The sources are the current skill, `references/api.md`, and the prompt in [intent.md](intent.md).
- P2. The skill stays generic.
- P3. The spec wins over the plan. A departure is written back in the same pull request.
- P4. One implementation phase, one pull request.
- P5. Historical intent folders stay untouched.
- P6. Config as code is the default pointer for a new repo. An explicit request for a snapshot still uses the inline procedure.

## 4. Users and scenarios

- An agent setting up a new repo, with a committed `.cursor/environment.json` and no personal or team saved environment, points at Config as code and does not call `create`.
- The file is not committed yet. The agent still points at committing it and launching without a named environment. It does not write the file and does not call `create` unless the user asked for an inline snapshot.
- The user asked for an environment that will not follow later edits to the file. The agent uses the existing create procedure, including the primordial-build rules.
- A personal or team saved environment already matches. The agent does not describe an unnamed launch as creating a file-following environment.
- A self-hosted run still does not read `.cursor/environment.json`.

## 5. Functional requirements

### What stays

FR1. Phase 0 edits only these product files:

- `.agents/skills/cursor-cloud-environments/SKILL.md`
- `.agents/skills/cursor-cloud-environments/references/api.md`
- `AGENTS.md`
- `REVIEW.md`
- `README.md` (the intent tree only)

`intent/config-as-code/plan.md` may gain build notes in that same pull request if implementation departs from this spec. No other path changes. `intent/onboard/` does not change. `scripts/environments.py` does not change.

FR2. These `SKILL.md` strings stay, in substance:

```text
name: cursor-cloud-environments
Do not use this to edit only a repo's .cursor/environment.json
Do not create a new Cursor API key
cursor-cloud MCP
propose-environment-json
A self-hosted run does not read
Only Cursor-hosted agents use the saved environment.
exit 127
A personal environment overrides a committed
does not set `repoFile`
If any non-draft build is `IN_PROGRESS`, wait
On HTTP 503 or 429, do not POST again
Do not activate drafts
`delete` refuses to run without `--yes`
```

The frontmatter `name` stays the directory name. Keep the folded `>-` description. `skill-frontmatter` only checks that `name` matches the directory and that `description` is non-empty. Checked `.github/skill-frontmatter-check.py` on 2026-10-30 at `ecc0e2f`.

FR3. These `references/api.md` strings stay verbatim:

```text
1. A personal saved environment
2. A team saved environment
3. `.cursor/environment.json` in the repository, for a single-repo cloud agent, when no saved environment matches
Creating with this script makes a saved environment (a personal one, unless `--owner team`). That is a copy of the JSON. `repoFile` stays unset.
a cloud agent start on a single repo with no saved environment yet adopts a valid committed `.cursor/environment.json`
Patching `environmentJson` on that kind returns `409 repo_file_environment_locked`.
The environment reads `.cursor/environment.json` from its only repo. Change the file and build that branch, or create a separate saved environment.
| `create` | `POST /v1/environments` |
```

Do not add a calls-table row.

### Routes

FR4. The description states, in substance, that create through `POST /v1/environments` is the inline-config route, that it snapshots the config and does not follow the repo file, and that Config as code is the other route and the preferred path for new repos. These description strings stay in the description: `Do not use this to edit only a repo's .cursor/environment.json`, `Do not create a new Cursor API key`, `cursor-cloud MCP`, and `SUCCEEDED`. The other FR2 strings stay in the body. Do not move `exit 127` or the primordial-build rules into the description.

FR5. After the self-hosted paragraph and before `## Script`, add a `## Two routes` section that contains these sentences verbatim:

```markdown
This skill covers inline-config environments created through the API (`POST /v1/environments`). That call snapshots the config and does not follow the repo file. `scripts/environments.py` create is that call.

Config as code is the other route. When a repo has a committed `.cursor/environment.json` and no saved environment, launching a cloud agent or Project on it without naming an environment makes Cursor create one that follows the file. That is the preferred path for new repos. This skill does not write that file and does not launch that agent or Project.

No saved environment means no personal saved environment and no team saved environment. An empty personal list is not enough.
```

Do not add a third route. Do not explain a difference between "adopts a valid committed `.cursor/environment.json`" and "create one that follows the file." D10.

FR6. At the start of procedure step 3, add these sentences verbatim. Keep the existing "Create only when" sentence and steps 4–7.

```markdown
When the preferred path applies, stop before create and point at Config as code. Do not call `create`. The preferred path applies to a new repo when the user did not ask for an inline-config snapshot, `list --repo github.com/owner/name --owner personal` is empty, and `list --repo github.com/owner/name --owner team` is empty. If the committed `.cursor/environment.json` is not there yet, point at committing that file and launching a cloud agent or Project without naming an environment. Do not write the file. If the team list call fails, stop and report the error. Do not treat a failed team list as empty. If either list has an id, this is not the no-saved-environment case: say that a saved environment already matches, and do not describe an unnamed launch as creating a file-following environment.
```

`list`, `get`, `history`, and `active` still do not start a build. Step 2's personal-list rules stay: one personal id is kept, more than one personal id stops to ask, and an empty personal list is what allows create when the user asked for inline-config.

FR7. In the Report section, keep the personal-override sentence and the `repoFile` sentence. Add these sentences verbatim after them:

```markdown
That is the inline-config snapshot. A Config as code environment follows the file. Do not patch its `environmentJson`. Change the file and build that branch, or create a separate saved environment (`409 repo_file_environment_locked`).
```

Do not say a commit by itself starts a build. Do not say the script can set `repoFile`.

FR8. In `references/api.md`, immediately after the paragraph that contains `` `repoFile` stays unset ``, add these sentences verbatim:

```markdown
The script's create, `POST /v1/environments`, is the inline-config route. It snapshots the config and does not follow the repo file. The other kind is Config as code. When a repo has a committed `.cursor/environment.json` and no saved environment, launching a cloud agent or Project on it without naming an environment makes Cursor create one that follows the file. That is the preferred path for new repos. It is not `POST /v1/environments`. No saved environment here means neither a personal nor a team saved environment matched.
```

Do not otherwise rewrite that file. The adopt sentence and the `409` sentence stay beside the new sentences. They are the same route, not a third one.

### Handbook

FR9. In `AGENTS.md`, replace the two active-change pointers and leave the rest.

```text
The current change is documented in `intent/config-as-code/`.
- `intent/<change>/` — intent, spec, and plan for the active change (currently `intent/config-as-code/`). `intent/onboard/` is historical.
```

FR10. In `REVIEW.md`, replace only the two sentences that say this onboarding does not change skill behavior and that the only allowed skill edit is a shellcheck fix in `setup.sh`. The replacement is:

```markdown
Historical onboarding did not change skill behavior. This change may edit `.agents/skills/cursor-cloud-environments/SKILL.md` and `.agents/skills/cursor-cloud-environments/references/api.md` only, as `intent/config-as-code/spec.md` requires. No other path under `.agents/skills/` changes.
```

These strings stay: `Bugs:`, `Security:`, `Compliance:`, `skills-cursor`, `SESSION_DEAD`, `pgrep`, `at most five nits`, `verbatim prompt`, `shellcheck`, `install-smoke`, `skill-frontmatter`, `CodeQL`, `workflow_dispatch`.

FR11. In the README structure tree, `intent/` lists `config-as-code/` and `onboard/`. The cursor-cloud-environments blurb stays byte for byte, including `A new environment is not delivered until a non-draft default-branch build has succeeded.`

### Merge

FR12. Phase 0 is one pull request into `main`. Squash-merge it only when `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded, never with an admin override. Do not add a ruleset or a required status check. Do not add `workflow_dispatch` or CodeQL. Those jobs already exist on `main` at `ecc0e2f` (`.github/workflows/test.yml`). This draft is not that pull request.

## 6. Acceptance criteria

| ID | Criterion | Check |
|---|---|---|
| AC1 | `intent/config-as-code/intent.md` quotes the prompt verbatim under "Original prompt", beside `spec.md` and `plan.md`. No other intent folder is edited. | Review. `git diff --name-only origin/main` for the draft is only this folder. |
| AC2 | `SKILL.md` satisfies FR2 and FR4–FR7. | Phase 0 definition of done. |
| AC3 | `references/api.md` satisfies FR3 and FR8. The calls table is unchanged. | Phase 0 definition of done. |
| AC4 | `AGENTS.md`, `REVIEW.md`, and the README tree satisfy FR9–FR11. Product files name no person, machine, or model. | Phase 0 definition of done. |
| AC5 | The Phase 0 diff is only the FR1 paths. | `git diff --name-only origin/main` |
| AC6 | Squash-merge of Phase 0 happens only after `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded. No admin override. No ruleset or required-check edit. | The three checks on that pull request. |

## 7. Design decisions

**D1 — Slug `config-as-code`.** The folder is `intent/config-as-code/`. Checked 2026-10-30 after `git fetch origin main`: `origin/main` is `ecc0e2f2229eb1573c66785629b6d90bc6c323cc`. `git ls-tree -r --name-only origin/main intent/` lists only `intent/onboard/`. `git branch -a` had no `cursor-cloud-environments` branch and no `config-as-code` ref. The slug is free. This draft does not modify `intent/onboard/`.

**D2 — This pull request is the draft only.** It adds the three files in this folder. It does not edit the skill. The session that opens it does not merge it and does not start Phase 0.

**D3 — What the skill already says, checked before any new requirement.** Read on 2026-10-30 at `ecc0e2f`. `SKILL.md` frontmatter: do not use this skill to edit only a repo's `.cursor/environment.json`, and do not use it for cursor-cloud MCP setup on a hosted run that already has a linked environment. Body: a saved environment is created and changed with the Cloud Agents API from a self-hosted My Machines worker; `propose-environment-json` is not how to create that dashboard environment; a self-hosted run does not read `.cursor/environment.json`; only Cursor-hosted agents use the saved environment. Procedure step 3 creates only when the user asked and the personal list was empty, or they asked for a distinct one. The primordial-build rules, the 503/429 stop, draft builds, and `delete` without `--yes` are already there. The report says a personal environment overrides a committed `.cursor/environment.json` for that user, and that the API stores a copy and does not set `repoFile`, so later edits to the file in git do not change this environment. None of those sentences is reversed.

**D4 — Inline-config is the existing create call.** `references/api.md` maps `create` to `POST /v1/environments` and says `repoFile` stays unset. `scripts/environments.py` `cmd_create` sends `owner`, `name`, `repos`, and `environmentJson`. It does not send `repoFile`. Checked 2026-10-30 at `ecc0e2f`. The new text names that call inline-config and says it snapshots the config and does not follow the repo file. That matches the report sentence in D3. Config as code is not a new command. The skill points at it.

**D5 — "No saved environment" includes team.** `references/api.md` resolution order is personal, then team, then the file for a single-repo cloud agent. Step 2 of the skill lists `--owner personal` only, and it says a team environment is not that environment. An empty personal list is therefore not "no saved environment." The script accepts `--owner team` (`choices` are `personal` and `team`). The gate runs both lists. Neither the skill nor `references/api.md` states what `list` returns when `--owner` is omitted, so the skill must not rely on an unfiltered list. If the team list call fails, stop. Do not treat the failure as an empty list.

**D6 — The self-hosted sentence stays.** The preferred path is launching a cloud agent or Project. It is not a self-hosted run reading `.cursor/environment.json`. The sentence in D3 stays. The skill does not perform that launch.

**D7 — The skill still does not edit the file.** The frontmatter ban on using this skill only to edit `.cursor/environment.json` stays. Pointing at Config as code is not a procedure that writes the file.

**D8 — Preference is not a ban on snapshots.** The prompt says the skill covers the inline route and points at Config as code as preferred. When the user asks for an inline-config snapshot, the existing create procedure remains, including primordial build, history, drafts, 503/429, and delete. A new repo does not take that path unless they asked for the snapshot.

**D9 — "Follows the file" uses the existing 409 guidance.** `references/api.md` says the repo-file environment reads `.cursor/environment.json` from its only repo, and that the change is to edit the file and build that branch, or to create a separate saved environment. Patching `environmentJson` returns `409 repo_file_environment_locked`. The skill repeats that. It does not say a commit alone starts a build. It does not add `repoFile` to the create body.

**D10 — One other route.** The prompt's "create one that follows the file" and the reference's "adopts a valid committed `.cursor/environment.json`" are Config as code, not two mechanisms. The single-repo adopt sentence stays. The prompt's sentence is one repo, one committed file, no saved environment, cloud agent or Project, no environment named. Do not add a multi-repo rule. Do not add a Project endpoint. Do not delete the single-repo sentence.

**D11 — Phase 0 file list.** D4 is stated in `SKILL.md` and, so the reference the skill points at does not contradict it, in `references/api.md` with the FR8 sentences only. No script change.

**D12 — Handbook lines that would contradict Phase 0.** `AGENTS.md` says the current change is `intent/onboard/`. `REVIEW.md` says the only allowed edit under `.agents/skills/` is a shellcheck fix in `chromium-browser-automation/scripts/setup.sh`. Left in place, those sentences forbid this change. Phase 0 updates those sentences as FR9 and FR10 and does not rewrite the rest. The README blurb stays. The structure tree gains `config-as-code/` so the new folder is visible. `onboard/` stays in the tree.

**D13 — Generic product docs.** No person, machine, host, home directory, or model name is added to `SKILL.md`, `references/api.md`, `AGENTS.md`, `REVIEW.md`, or `README.md`.

**D14 — Build model.** Phase 0 uses Composer 2.5. Do not substitute. If that model cannot be launched, stop and ask. The name stays out of the product docs in D13. It is named here and in [plan.md](plan.md) so the build has it.

**D15 — One phase, one pull request, existing checks.** Squash-merge only after `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded. No admin override. Do not add rulesets or required checks. Checked `.github/workflows/test.yml` at `ecc0e2f`: those three job names, `pull_request` and `push` to `main`, no `workflow_dispatch`.

**D16 — Signing.** Commits are signed. Before the first commit, run `timeout 20 gpg --batch --local-user <key> --sign --output /dev/null` with the key `git config --get user.signingkey` returns. Never pass `--pinentry-mode error` or `--no-gpg-sign`. If the sign check fails, stop. Do not commit. Do not write the key id into the repo.

## 8. Open questions

None.
