---
name: build-practices
description: >-
  Load for implementing code and docs in pull requests and for reviewing
  build pull requests in any repo: writing rules, git workflow, merge gate,
  spec vs plan during build, Cursor Cloud install boundaries, layout, and
  repository admin limits. Also use during ai-native-sdlc build phases.
---

# Build practices

Rules for implementing code, updating docs in pull requests, and reviewing those changes. Each product repo keeps commands and product-specific review risks in root `AGENTS.md` and `REVIEW.md`.

## Writing (pull requests)

Rules 1 and 2 apply to every file the builder changes in a pull request. Rule 3 applies only to human-facing docs touched in that pull request.

1. **No self-references.** In prose about the repo itself, say "this repo" instead of hardcoding owner, name, or URL. Distribution entry points may hardcode a canonical location: a curl-to-sh one-liner, an installer's default source URL, or another repo's dependency that pulls shared skills from the skills distribution repo (optional fork override such as `LOCAL_SKILLS_REPO_URL` on the published root `install.sh`). References to other repos are fine. Never derive this repo's identity from `GITHUB_REPOSITORY` in scripts or workflows that other repos' CI may run—that variable names the consuming repository. Elsewhere in scripts and workflows, derive identity with `git remote` or the Actions `github.repository` context when appropriate.
2. **No values of variable config.** Do not copy the current value of a setting (for example who a signing certificate is issued to, or machine-specific paths) into docs, tests, or workflows. Refer to the setting by its name (the env var, secret, or config key). Tests check behavior against the configured value, not a literal.
3. **Do not state the obvious (human-facing docs only).** In README, user docs, and setup docs, drop notes a competent reader already knows, such as a parenthetical that success means exit 0. Builders tend to add these; reviewers should cut them. Do not apply this rule to agent-facing files: root `AGENTS.md`, `REVIEW.md`, skills, or intents written for agents. Those files keep explicit expectations such as "(healthy: exit 0)" because they help smaller models.

## Cursor Cloud environment install

A Project's `.cursor/install.sh` is only for setting up Cursor Cloud Agent environments. Do not reuse it in GitHub Actions, local developer setup, or other automation.

That script installs shared agent skills from `nikolaybotev/local-skills` (typically by piping the published root `install.sh` into a shell). It hardcodes that canonical source. It has no fork override and no env var that retargets the skills repo.

The published root `install.sh` in the skills repo is separate: a piped run defaults to the canonical clone URL and may honor `LOCAL_SKILLS_REPO_URL` for forks. Do not describe that override as applying to a Project's `.cursor/install.sh`.

## Spec and plan during build

- The **spec wins over the plan**. If implementation follows the plan but violates the spec, fix the code or change the spec first—do not treat the plan as authority over the spec.
- When implementation **departs from the plan**, record the departure in `plan.md` in the **same commit** as the code.

## Git and pull requests

- Land work through pull requests only; do not push commits directly to the default branch.
- Squash-merge unless the repo's written policy explicitly allows another merge method.
- Delete the branch after merge when the host offers it.
- Keep linear history on the default branch; do not force-push the default branch.
- One topic per pull request. Use conventional commit prefixes (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`).
- Do not rewrite published history or force-push to hide mistakes without explicit owner approval.

## Merge gate

- Merge only when every required check for that pull request has **succeeded**. A cancelled check has not succeeded. An admin override merge is not a green merge.
- Record the exact required job or check names in each repo's `AGENTS.md`; do not merge while any required check is missing, pending, failed, or cancelled.
- Update the branch from the default branch when it has fallen behind before expecting a green run.

## Build execution

- Before build, fresh-context review of the spec against the intent and of the plan against the spec has already happened; apply agreed findings before opening build pull requests.
- Build in fresh context with the repo's `AGENTS.md`, `REVIEW.md`, this skill, the spec, and the plan (including deviations already recorded in `plan.md`).
- One plan phase is one branch and one pull request unless the plan explicitly groups phases.
- Update `AGENTS.md` in the same change when commands or recurring mistakes change.
- Do not commit secrets, API keys, private keys, or other key material, or caches and generated output the repo ignores.
- When the repo requires signed commits, sign them; do not bypass signing.
- One writer per intent file at a time during design; do not run two sessions editing the same `spec.md` or `plan.md` concurrently.

## Passing secrets to processes

Weakest to strongest:

1. **Command-line arguments.** Weakest option. On macOS and Linux, any user on the machine can read another process's arguments with `ps`. Arguments also land in shell history, crash reports, and process monitoring. This is CWE-214. Do not accept a secret only as an argument. Example, as of 2026-10-31: the Cursor self-hosted agent worker takes its API key as `--api-key`, which is visible in `ps`.
2. **Environment variables and owner-only (0600) credential files.** Same tier, not two different strengths. Only the owning user or root can read them. On Linux, `/proc/<pid>/environ` is owner-only. On macOS, `ps -E` exposes the environment only for your own processes. Acceptable and common, including twelve-factor apps. Environment variables are inherited by child processes and can appear in crash dumps. Examples: credential files used by the gcloud and AWS CLIs.
3. **OS keychain or secret store.** Strongest option. Encrypted at rest; access scoped per application. Example: pinentry-mac storing a GPG key passphrase in the macOS login keychain.

Prefer a keychain or secret store. Otherwise read the secret from an environment variable or a 0600 file path. Never require it on the command line. If a CLI flag must exist for compatibility, also accept the environment variable or the file.

## Testing

Four kinds of check:

- **Unit.** One piece in isolation, everything around it faked. Covers one function or module's logic.
- **Integration.** Real pieces working together in a real process, with the far end faked (for example a fake webhook receiver). Covers how components fit together.
- **End-to-end.** The whole feature through its real interfaces as deployed, nothing faked between the two ends.
- **Live check.** A quick check of one real installed deployment in place, by hand or from a routine. It is not a test suite.

| Type | What it is | What it covers | Hot-reload example |
| --- | --- | --- | --- |
| Unit | One piece in isolation, everything around it faked | The logic of a single function or module | A config-reload unit test calls the config library directly and checks that a valid change applies and a bad one is rejected |
| Integration | Real pieces working together, the far end faked | How components fit together inside a real process | A script runs the real watcher service, swaps in an invalid config, then a group-readable (0644) one, then a valid one for a second folder, and checks notifications at a fake webhook receiver |
| End-to-end | The whole system as a user meets it, nothing faked between the two ends | The feature through its real interfaces, as deployed | With the signed service installed and running under launchd, edit the real config with a real change, then check its log for the reload line and that the process ID didn't change |
| Live check | A quick check of the real installed system in place | That this deployment works right now | On a live deployment, set the config to mode 0610, see the rejection logged with the same process ID, then set it back to 0600 |

If anything between the two ends is faked, it is integration, not end-to-end.

End-to-end is a convention, not a precise term. Whenever a test, pull request, or review calls something end-to-end, state its two ends. A good default for the ends is wherever a real user or outside system touches the feature: in through the real interface, out to the real effect. Scope the ends to the feature under test. For example, for a config hot-reload feature the ends are a real config edit and the installed service logging the reload with the same process ID, not what the service does afterwards.

Keep many unit tests, fewer integration tests, and only a few end-to-end ones, because bigger tests are slower, more fragile, and harder to pin down when they fail.

Reviewers should flag a test mislabeled as end-to-end when it fakes something between its ends.

## Layout

- Use root `AGENTS.md`, not `CLAUDE.md`. Use `.agents/skills/`, not `.claude/skills/`.
- Product skills belong in `.agents/skills/<name>/` inside the product repo. Install shared skills from the skills repo; do not copy whole skill trees into each product repo.

## Repository admin

- Agents do not create or change GitHub rulesets, branch protection, required checks, or other repository admin settings unless a human owner handles that outside agent automation.
- Do not dispatch workflows, cancel runs, or list secrets from agent automation unless the active spec assigns that work and the owner expects it.
