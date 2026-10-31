# intent.md — Onboard

| | |
|---|---|
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

## Original prompt (redacted)

> Bootstrap a Cursor Project for github.com/nikolaybotev/local-skills. Onboard per the ai-native-sdlc skill: write `AGENTS.md`, `REVIEW.md`, and a README update if needed; add `.github/workflows/test.yml` with shellcheck, an install smoke test into a temporary `HOME`, and SKILL.md frontmatter validation; work through spec, plan, fresh-context review, then build one phase per pull request. Squash-merge only when checks are green. Keep skills and docs generic, not written for one machine.
>
> **Already done.** Commit d006fc6 added `.cursor/environment.json`, `.cursor/install.sh`, and `.cursor/start.sh`. The repo is public. Merge is squash only, with delete branch on merge. Protected `main` requires pull requests, squash merge, signed commits, and linear history.
>
> **First task after onboarding.** Update the cursor-cloud-environments skill to distinguish inline-config environments (`POST /v1/environments`, snapshot only) from Config as code (committed `.cursor/environment.json` followed on launch). Prefer Config as code for new repos.
>
> **Standing limits.** Do not handle secrets or key material. Do not create rulesets, add required checks, dispatch workflows, cancel runs, or list secrets from automation.
