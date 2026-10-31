---
name: cursor-cloud-environments
description: >-
  Manage saved Cursor Cloud Agent environments from a self-hosted My Machines
  worker: list, create, update, delete, history, and builds. Use when the
  user asks to create or change a Cloud Agent environment, an environment
  build, or the dashboard environment for a repository, from a Cursor
  self-hosted worker. This skill covers inline-config environments created
  through the API (POST /v1/environments), which snapshots the config and
  does not follow the repo file. Config as code is the other route and the
  preferred path for new repos. A new environment is not delivered until a
  non-draft default-branch build has SUCCEEDED. Start that build only when
  one is not already in progress. Uses the worker's existing API key. Do not create a new Cursor API key. Do not use this to edit only a repo's .cursor/environment.json, or for cursor-cloud MCP setup on a hosted run
  that already has a linked environment.
---

# Cursor Cloud Agent environments

A saved environment is the dashboard object Cursor-hosted agents run in. From a self-hosted My Machines worker, create and change it with the Cloud Agents API. The `cursor-agent-worker` extension already minted a user API key and passed it to `agent worker start --api-key`. Use that key. Do not mint another one, do not open Cursor secret storage, and do not put the key in a shell command, a file, a commit, or the chat.

`cursor-cloud` MCP tools such as `trigger-environment-build` and `propose-environment-json` apply to this run's linked environment. A self-hosted run usually has none, and that override cannot express a Dockerfile. Do not use them to create the dashboard environment.

A self-hosted run does not read `.cursor/environment.json`. Only Cursor-hosted agents use the saved environment.

## Two routes

This skill covers inline-config environments created through the API (`POST /v1/environments`). That call snapshots the config and does not follow the repo file. `scripts/environments.py` create is that call.

Config as code is the other route. When a repo has a committed `.cursor/environment.json` and no saved environment, launching a cloud agent or Project on it without naming an environment makes Cursor create one that follows the file. That is the preferred path for new repos. This skill does not write that file and does not launch that agent or Project.

No saved environment means neither a personal nor a team saved environment matched this repo. An empty personal list is not enough.

A cloud agent start on a single repo with no saved environment yet adopts a valid committed `.cursor/environment.json`.

A custom image has to include `curl` and `ca-certificates`. The build installs the exec daemon with `curl`, and a missing `curl` fails that step with exit 127. Include `tar` and `gzip` as well so that download can be unpacked. `git` and `sudo` are required too.

## Script

`SKILL_DIR` is the directory that contains this `SKILL.md`. Run the script. Do not reimplement key discovery in the shell. Its stdout is JSON. The key never appears there.

```bash
python3 "$SKILL_DIR/scripts/environments.py" me
```

If `me` fails, stop. Tell the user the worker key is not available. Do not create a key. Do not run `ps`, `env`, or `pgrep`, and do not quote a process listing. The worker command line contains the key, and copying it puts the key in the transcript.

`me` returns `data.apiKeyName`. It looks like `cursor-agent-worker-ext-<hostname>-<pid>-<timestamp>` and matches a row on the Cursor API Keys page. Report that name when you use the key.

## Procedure

1. Run `me`.
2. Before creating a personal environment, run `list --repo github.com/owner/name --owner personal`. A team environment is not that environment. If `data.items` has one id, keep it and do not create another. Continue at step 5 with that id. If it has more than one id, stop and ask which one. Do not create and do not start a build. If it is empty, go to step 3. `list`, `get`, `history`, and `active` do not start a build.
3. When the preferred path applies, stop before create and point at Config as code. Do not call `create`. The preferred path applies when `list --repo github.com/owner/name --owner personal` is empty, `list --repo github.com/owner/name --owner team` is empty, and the user did not ask for an environment that will not follow later edits. If the committed `.cursor/environment.json` is not there yet, point at committing that file and launching a cloud agent or Project without naming an environment. Do not write the file. If the team list call fails, stop and report the error. Do not treat a failed team list as empty. If either list has an id, this is not the no-saved-environment case: say that a saved environment already matches, and do not describe an unnamed launch as creating a file-following environment. When the preferred path does not apply, create only when the user asked to create the environment and the list was empty, or they asked for a distinct one. The script requires `--name`, `--repo`, and `--environment-json`. `--owner` defaults to `personal`. Repeat `--repo` for each repository. The JSON file uses the same schema as `.cursor/environment.json`.
4. After create, run `history <id>`. Trust the history event with `"current": true` for the saved configuration. `get` can return `"environmentJson": null` even when that event holds the JSON. Do not deliver the environment yet. If `data.nextCursor` is set and no item has `"current": true`, run `history <id> --cursor <nextCursor>` before trusting the config.
5. Primordial build. This applies only when the user asked to create the environment, or asked for a build. A new environment is not ready until a non-draft default-branch build has `SUCCEEDED`. Saving configuration may already have started that build, so `create` does not mean you should POST another one.
   - Run `builds <id>` before any `build` POST, including immediately after create. Use `data.items[].status`, `data.items[].draft`, and `data.items[].completedAt`. `data.truncated` means the list is incomplete. Ignore `draft: true` for this check. `draft: false` is the default-branch build. If `data.truncated` is true, stop and say the build list is incomplete. Do not start a build from that page.
   - If any non-draft build is `IN_PROGRESS`, wait on the newest one. Do not POST another. Do not deliver an older `SUCCEEDED` build while that one is still running.
   - Otherwise, if any non-draft build is `SUCCEEDED`, that is the primordial build. Do not POST another. Deliver it.
   - Otherwise, if there is no non-draft build, or every non-draft build is `FAILED`, `CANCELLED`, or `SKIPPED`, POST `build <id>` with no flags. That is the required trigger. A long install is normal.
   - On HTTP 503 or 429, do not POST again. Run `builds` again. If a non-draft `IN_PROGRESS` is there, wait on it. If none appeared, stop and report that. Do not keep retrying.
   - Poll `build-get` while `data.status` is `IN_PROGRESS`, about 45–60 seconds apart. Exit code 1 is expected. A 404 on the first reads is expected: retry that GET at most 3 times. If it is still 404, stop and report the build id. Do not POST again. `SUCCEEDED` is the only status that lets you deliver. `FAILED`, `CANCELLED`, and `SKIPPED` are finished and not ready: report `data.failure.type` and `data.failure.code`, leave the environment, and do not start another build unless the user asks.
   - `ok: true` and the top-level `status` are the HTTP call. An in-progress build is HTTP 200. `data.type` of `universal_image` from `active` means no successful environment build is in use.
   - If you have to end the turn while `data.status` is still `IN_PROGRESS`, report the build id and that it is still running. Do not call the environment ready and do not start a second build.
6. A build the user asked for outside of creation uses the same wait. Pass `--draft` when agents must not pick it up yet. Any `--ref` requires `--draft` (`--ref repo=branch`, repeatable). Wait until that build's `data.status` is terminal. A draft `SUCCEEDED` does not make the environment ready and does not satisfy the primordial check. Do not activate drafts.
7. Update with `update <id> --name` or `--environment-json <path>`. a repo-file environment is not updated with `--environment-json`. A name-only update does not need a build. After `--environment-json`, run `builds` before posting. Saving that config can start a configuration-change build. If a non-draft build is already `IN_PROGRESS`, wait on it when the user asked for a build. Do not POST a second one. An update is not delivery. Delete only when the user named the environment and told you to delete it. `delete` refuses to run without `--yes`.

Read [references/api.md](references/api.md) when a call returns an error, or when the configuration itself is in question.

## Report

After creation, deliver the environment only when the primordial build succeeded. Give the environment id, name, owner, repository URLs, build id, status, and completed time. A personal environment overrides a committed `.cursor/environment.json` for that user. The API stores a copy and does not set `repoFile`, so later edits to the file in git do not change this environment. That is the inline-config snapshot. A Config as code environment follows the file. Do not patch its `environmentJson` (`409 repo_file_environment_locked`). Change the file and build that branch, or create a separate saved environment. If the build failed, give those same fields plus `failure.type` and `failure.code`, and say it is not ready. Leave the API key out. When you report an API timestamp, convert it to the user's zone.
