---
name: build-practices
description: >-
  Shared rules for implementing code and docs in pull requests and for
  reviewing build pull requests in any repo: writing rules, git workflow,
  merge gate, spec vs plan during build, Cursor Cloud install script, layout,
  and repository admin limits. Load and follow this skill during SDLC build
  phases and when reviewing changes that land through pull requests.
---

# Build practices

Rules for implementing code, updating docs in pull requests, and reviewing those changes. Each product repo keeps commands and product-specific review risks in root `AGENTS.md` and `REVIEW.md`.

## Writing (pull requests)

Rules 1 and 2 apply to every file the builder changes in a pull request. Rule 3 applies only to human-facing docs touched in that pull request.

1. **No self-references.** In prose about the repo itself, say "this repo" instead of hardcoding owner, name, or URL. Distribution entry points may hardcode a canonical location: a curl-to-sh one-liner, an installer's default source URL, or another repo's dependency that pulls skills from here (optional fork override such as `LOCAL_SKILLS_REPO_URL`). References to other repos are fine. Never derive this repo's identity from `GITHUB_REPOSITORY` in scripts or workflows that other repos' CI may run—that variable names the consuming repository. Elsewhere in scripts and workflows, derive identity with `git remote` or the Actions `github.repository` context when appropriate.
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

## Layout

- Use root `AGENTS.md`, not `CLAUDE.md`. Use `.agents/skills/`, not `.claude/skills/`.
- Product skills belong in `.agents/skills/<name>/` inside the product repo. Install shared skills from the skills repo; do not copy whole skill trees into each product repo.

## Repository admin

- Agents do not create or change GitHub rulesets, branch protection, required checks, or other repository admin settings unless a human owner handles that outside agent automation.
- Do not dispatch workflows, cancel runs, or list secrets from agent automation unless the active spec assigns that work and the owner expects it.
