---
name: cursor-cloud-environments
description: >-
  Manage saved Cursor Cloud Agent environments from a self-hosted My Machines
  worker: list, create, update, delete, history, and builds. Use when the
  user asks to create or change a Cloud Agent environment, an environment
  build, or the dashboard environment for a repository, from a Cursor
  self-hosted worker. Creating an environment always starts a build and
  waits until that first build succeeds before the environment is delivered.
  Uses the worker's existing API key. Do not create a new Cursor API key.
  Do not use this to edit only a repo's .cursor/environment.json, or for
  cursor-cloud MCP setup on a hosted run that already has a linked
  environment.
---

# Cursor Cloud Agent environments

A saved environment is the dashboard object Cursor-hosted agents run in. From a self-hosted My Machines worker, create and change it with the Cloud Agents API. The `cursor-agent-worker` extension already minted a user API key and passed it to `agent worker start --api-key`. Use that key. Do not mint another one, do not open Cursor secret storage, and do not put the key in a shell command, a file, a commit, or the chat.

`cursor-cloud` MCP tools such as `trigger-environment-build` and `propose-environment-json` apply to this run's linked environment. A self-hosted run usually has none, and that override cannot express a Dockerfile. Do not use them to create the dashboard environment.

A self-hosted run does not read `.cursor/environment.json`. Only Cursor-hosted agents use the saved environment.

A custom image has to include `curl` and `ca-certificates`. The build installs the exec daemon with `curl`, and a missing `curl` fails that step with exit 127. Include `tar` and `gzip` as well so that download can be unpacked. `git` and `sudo` are required too.

## Script

`SKILL_DIR` is the directory that contains this `SKILL.md`. Run the script. Do not reimplement key discovery in the shell. Its stdout is JSON. The key never appears there.

```bash
python3 "$SKILL_DIR/scripts/environments.py" me
```

If `me` fails, stop. Tell the user the worker key is not available. Do not create a key.

`me` returns `apiKeyName`. It looks like `cursor-agent-worker-ext-<hostname>-<pid>-<timestamp>` and matches a row on the Cursor API Keys page. Report that name when you use the key.

## Procedure

1. Run `me`.
2. Before creating, run `list --repo github.com/owner/name`. If an environment for that repo already exists, keep that id and do not create another unless the user asked for a distinct one. Do not tell the user it is ready yet. Continue with the primordial build.
3. Create only when the user asked to create the environment. `--owner` defaults to `personal`. Pass one `--repo` per repository and `--environment-json` as a path to a JSON object. The file uses the same schema as `.cursor/environment.json`.
4. After create, run `history <id>`. Trust the history event with `"current": true` for the saved configuration. `get` can return `"environmentJson": null` even when that event holds the JSON. Do not deliver the environment yet.
5. Tell the user a personal environment overrides a committed `.cursor/environment.json` for them. The API stores a copy. It does not set `repoFile`, so later edits to the file in git do not change this environment. Say that when it matters. This is part of the final report, not permission to stop before the build.
6. Primordial build. Creating an environment from config includes its first build. Before you tell the user the environment is ready, a non-draft build of the default branch must have `SUCCEEDED`.
   - If `list` found an existing environment, run `builds <id>` first. A `SUCCEEDED` non-draft build already satisfies this. An `IN_PROGRESS` build is the one you wait on. Do not start a second. If every build failed, was cancelled, or was skipped, or there is no build, start one.
   - Otherwise run `build <id>` with no flags. That builds every repo's default branch. A long install is normal.
   - On HTTP 503, do not retry the POST. Run `builds <id>`. If a build appeared, wait on that one.
   - Poll `build-get <id> <buildId>` until status is `SUCCEEDED`, `FAILED`, `CANCELLED`, or `SKIPPED`. The first read can be `404`; retry the GET, not the POST. Wait about 45–60 seconds between reads. Do not treat `create` or `IN_PROGRESS` as success. `active` returning a universal image means no successful environment build is in use yet.
   - Deliver the environment only after `SUCCEEDED`. Include the build id, status, and completed time.
   - If that build fails, do not call the environment ready and do not start another build unless the user asks. Report `failure.type`, `failure.code`, and any message. Leave the environment in place.
7. A build the user asked for outside of creation uses the same wait. Pass `--draft` when agents must not pick it up yet. Any `--ref` requires `--draft` (`--ref repo=branch`, repeatable).
8. Update with `update <id> --environment-json <path>` or `--name`. Delete only when the user named the environment and told you to delete it. `delete` refuses to run without `--yes`. An update does not itself start the primordial build.

Read [references/api.md](references/api.md) when a call returns an error, or when the configuration itself is in question.

## Report

After creation, deliver the environment only when the primordial build succeeded. Give the environment id, name, owner, repository URLs, build id, status, and completed time. If the build failed, give those same fields plus the failure, and say it is not ready. Leave the API key out. When you report an API timestamp, convert it to the user's zone.
