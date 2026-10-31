# intent.md — Config as code

| | |
|---|---|
| Author | Nikolay Botev |
| Captured | 2026-10-30 |
| Status | Draft |
| Stage | 1 · Plan |
| Feeds | [spec.md](spec.md) → [plan.md](plan.md) |
| Builds on | [intent/onboard](../onboard/intent.md) |

## Problem

The cloud-environments skill creates saved environments through the API. That path snapshots the config and does not follow the repo file. The skill does not say this is the inline-config route, that Config as code is the other route, or that a new repo should prefer launching a cloud agent or Project without naming an environment so Cursor creates one that follows a committed `.cursor/environment.json`.

## Proposed outcome

An agent that reads the skill can tell the two routes apart. It still uses the inline snapshot when that is what was asked for. For a new repo, it points at Config as code.

## Affected users and systems

- **Users:** agents asked to create or change a Cloud Agent environment, including for a new repo.
- **Systems:** the `cursor-cloud-environments` skill and its API reference. The handbook lines that name the active intent folder.

## Constraints and principles

- This draft records the change. It does not edit the skill. It is not merged in the session that opens it.
- Keep the skill generic. Do not name a person, a machine, or a model in the product docs.
- Do not invent API behavior that the skill, `references/api.md`, and the prompt do not support. Check the current skill text before a requirement would contradict it.
- `intent/onboard/` and any other existing intent folder are historical. Do not modify them.
- One implementation phase, one pull request. Squash-merge only after `shellcheck`, `install-smoke`, and `skill-frontmatter` have succeeded. No admin override. Do not add rulesets or required checks.
- Build with Composer 2.5. Keep that name out of the product docs.
- Signed commits, conventional commits, no force-push, no secrets. Do not run `install.sh` into a real home.

## Open questions (carried into spec.md)

None. The prompt and the current skill text settle the design. [spec.md](spec.md) records the decisions.

## Original prompt (verbatim)

> Update the cursor-cloud-environments skill to say that it covers inline-config environments created through the API (`POST /v1/environments`), which only snapshot the config and don't follow the repo file. The Config as code route is the other one. When a repo has a committed `.cursor/environment.json` and no saved environment, launching a cloud agent or Project on it without naming an environment makes Cursor create one that follows the file. The skill should point to that as the preferred path for new repos.
