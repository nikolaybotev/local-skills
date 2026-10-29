# Environments API notes

Base URL: `https://api.cursor.com`. Auth is `Authorization: Bearer` using the worker key. Reference: https://cursor.com/docs/cloud-agent/api/endpoints

The script is the interface. This file is for errors and configuration behavior.

## Resolution

Cursor picks the first match:

1. A personal saved environment
2. A team saved environment
3. `.cursor/environment.json` in the repository, for a single-repo cloud agent, when no saved environment matches

Creating with this script makes a saved environment (a personal one, unless `--owner team`). That is a copy of the JSON. `repoFile` stays unset. An environment that reads its config from the repo is a different kind: a cloud agent start on a single repo with no saved environment yet adopts a valid committed `.cursor/environment.json`. Patching `environmentJson` on that kind returns `409 repo_file_environment_locked`.

## Calls the script makes

| Script | HTTP |
|---|---|
| `me` | `GET /v1/me` |
| `list` | `GET /v1/environments` |
| `get` | `GET /v1/environments/{id}` |
| `history` | `GET /v1/environments/{id}/history` |
| `builds` | `GET /v1/environments/{id}/builds` |
| `build-get` | `GET /v1/environments/{id}/builds/{buildId}` |
| `active` | `GET /v1/environments/{id}/builds/active` |
| `create` | `POST /v1/environments` |
| `update` | `PATCH /v1/environments/{id}` |
| `delete` | `DELETE /v1/environments/{id}` |
| `build` | `POST /v1/environments/{id}/builds` |

`list --repo` sends `github.com/owner/name`, without the scheme. Create and build refs send `https://github.com/owner/name`.

## Errors worth acting on

| Status | Meaning |
|---|---|
| `409 environment_name_conflict` | That owner already has this name. The body may include `environmentId`. Use that environment instead of creating another. |
| `400 repository_access` | Cursor cannot reach the repository through the user's source control connection. |
| `400 validation_error` | The JSON or a filter is invalid. |
| `409 environment_repo_edit_blocked` | A single-repo environment cannot change its repository. Create a new environment. |
| `409 repo_file_environment_locked` | The environment reads `.cursor/environment.json` from its only repo. Change the file and build that branch, or create a separate saved environment. |
| `503` on start build | Cursor could not confirm the build. Do not retry. List builds first. |
| `429` | Too many requests, or too many builds already in progress. |

`POST /v1/environments` returns `201`. `PATCH` returns `204` with no body. `POST .../builds` returns `202` and a build id. Reading that build immediately can briefly return `404`.

## environment.json

The create and update body field `environmentJson` is a JSON-encoded string of the same object a repo commits as `.cursor/environment.json`. Include a Dockerfile when the image is not the default Ubuntu image:

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "install": "swiftc --version"
}
```

`dockerfile` is relative to `.cursor/`. `context` of `..` is the repo root. Do not `COPY` the project into the image. Install `git` and `sudo`. Set `USER` and `WORKDIR`. `install` must finish and be safe to run again. It runs while a build is prepared, not as a long-running server.

A build with no body uses each repo's default branch and, once it succeeds, is what new agents start from. That first successful non-draft build is the primordial build. Environment creation is not finished until `build-get` reports `SUCCEEDED` for it. A failed, cancelled, or skipped build does not count, and neither does `IN_PROGRESS`. A draft build is not used until someone activates it. This script does not activate drafts. Any requested ref other than the default branch has to be a draft.
