# intent.md — Onboard

| | |
|---|---|
| Author | Nikolay Botev |
| Captured | 2026-10-30 |
| Status | Draft |
| Stage | 1 · Plan |
| Feeds | [spec.md](spec.md) → [plan.md](plan.md) |

## Problem

This repo holds shared agent skills and the installer that copies them onto a machine. A broken skill or a broken installer breaks every repo that installs them. The repo has no root `AGENTS.md` or `REVIEW.md`, no CI, and a README that does not match the cloud-environment installer. Agents are about to change it through pull requests, with no written cycle and no list of the ways this repo actually fails.

## Proposed outcome

An agent opening the repo can read the cycle, the prohibitions that come from this installer and these skills, and a review sheet aimed at those same risks. The README agrees with the installer about where a Cloud Agent gets the skills. A small CI workflow fails fast when the shell is wrong, when the installer cannot copy the skills into a temporary home, or when a skill's frontmatter is invalid. The work is specified and planned before any product file is added, then built one phase per pull request.

## Affected users and systems

- **Users:** agents that install or edit these skills, and the owner of the repo.
- **Systems:** this git repo, the root `install.sh`, `.cursor/install.sh`, and GitHub Actions on pull requests and on `main`.

## Constraints and principles

- Follow the ai-native-sdlc cycle already in this repo: bootstrap, spec and plan, fresh-context review, then build, one phase per pull request.
- Existing intent, spec, and plan files are historical records. Do not modify them. This change is a new folder.
- Skills and docs stay generic. Do not write them for any one machine.
- Squash-merge only when checks are green, never with an admin override.
- Skip CodeQL unless it is actually useful here.
- CI timeouts stay aggressive. The example is shellcheck, an `install.sh` smoke test into a temporary `HOME`, and `SKILL.md` frontmatter validation.
- Do not create rulesets, add required checks, dispatch workflows, cancel runs, or list secrets.
- Do not handle secrets or key material.
- Do not run the root `install.sh` or `.cursor/install.sh` against a real home, and do not install skills onto a machine, as part of this change.
- The cursor-cloud-environments follow-up (inline API environments versus config as code) comes after onboarding. It is not this change.

## Open questions (carried into spec.md)

None. The repo and the prompt settle the design. [spec.md](spec.md) records the decisions.

## Original prompt (verbatim)

> Welcome. You're the new Cursor Project for github.com/nikolaybotev/local-skills, which Nikolay Botev owns. I'm Roger, the assistant that bootstraps his repos and relays between his Projects.
>
> **What this repo is.** Shared agent skills in `.agents/skills/` (ai-native-sdlc, canvas-pdf, chromium-browser-automation, cursor-cloud-environments), plus a root `install.sh`. Cloud agent environments run that installer to put the skills into `~/.cursor/skills-cursor`. Nikolay's agents depend on these skills, so a broken skill or installer breaks every repo that installs them.
>
> **Already done.** Commit d006fc6 added `.cursor/environment.json`, `.cursor/install.sh` (installs this checkout's own skills) and `.cursor/start.sh`. The repo is public. Merge is squash only, with delete branch on merge. The `main branch protection` ruleset requires a PR, squash only, signed commits and linear history, with no bypass. All changes go through PRs from here on.
>
> **First, pick a name.** Choose a capitalized one-word name for yourself and tell me. I'll rename the Project.
>
> **Then onboard, per the ai-native-sdlc skill in this repo.** Write AGENTS.md (include the cycle, and list this repo's failure modes as prohibitions), REVIEW.md tuned to those same risks, and a README update if one is needed. Add a small CI, `.github/workflows/test.yml`, with aggressive timeouts (for example, shellcheck plus an install.sh smoke test into a temp HOME, and SKILL.md frontmatter validation). Skip CodeQL unless it's actually useful here. Work in spec and plan, then a fresh-context review, then build, one phase per PR. Squash-merge only when checks are green, never with an admin override. Existing intent, spec and plan files are historical records, so don't touch them. Keep skills and docs generic, not written for any one machine.
>
> **Your first real task, after onboarding.** Update the cursor-cloud-environments skill to say that it covers inline-config environments created through the API (`POST /v1/environments`), which only snapshot the config and don't follow the repo file. The Config as code route is the other one. When a repo has a committed `.cursor/environment.json` and no saved environment, launching a cloud agent or Project on it without naming an environment makes Cursor create one that follows the file. The skill should point to that as the preferred path for new repos.
>
> **Admin changes.** Your token can't create rulesets, add required checks, run `workflow_dispatch`, cancel runs or list secrets. By default, start a thread on Nikolay's self-hosted worker (Roger's `~/git` workspace), which has `gh` as Nikolay, and have it report the settings back as the API reads them. Once your CI merges, do that to add its job names as required status checks (strict). If the first start asks for access approval, that's Nikolay's click. Tell me and I'll let him know. His fallback is the GitHub UI.
>
> **Deploying to Roger.** A merged skill change takes effect on Roger only after `git pull` plus the root `install.sh` in `~/git/local-skills`. Never run that, or install anything else on Nikolay's machines, without his approval, which I'll relay. Ask me first.
>
> **Standing limits.**
> - Use only Cursor's own models: Grok 4.7 High for coordination, spec, plan and review, and Composer 2.5 for build.
> - Never handle secrets or key material.
> - Commits made on Roger are signed with Nikolay's GPG key. Test signing with `timeout 20 gpg --batch --local-user <key> --sign --output /dev/null <<< "sign-check"`. Never use `--pinentry-mode error` or `--no-gpg-sign`. If signing fails, stop and ask.
> - Report milestones and merged PRs to me briefly.
