#!/usr/bin/env python3
"""Call the Cursor Cloud Agents environments API with the self-hosted worker's existing key.

The key is read from the worker process command line and is never printed.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.cursor.com"


def eprint(message):
    print(message, file=sys.stderr)


def process_rows():
    attempts = [
        ["ps", "-axww", "-o", "pid=,ppid=,command="],
        ["ps", "-eo", "pid=,ppid=,args="],
    ]
    last = "ps failed"
    for cmd in attempts:
        try:
            text = subprocess.check_output(cmd, text=True, errors="replace")
        except (OSError, subprocess.CalledProcessError) as exc:
            last = str(exc)
            continue
        rows = []
        for line in text.splitlines():
            parts = line.strip().split(None, 2)
            if len(parts) < 3:
                continue
            try:
                pid = int(parts[0])
                ppid = int(parts[1])
            except ValueError:
                continue
            rows.append((pid, ppid, parts[2]))
        if rows:
            return rows
    raise SystemExit(last)


def argv_token(command, flag):
    parts = command.split()
    if flag not in parts:
        return None
    index = parts.index(flag)
    if index + 1 >= len(parts):
        return None
    return parts[index + 1]


def api_key_from_command(command):
    if "worker" not in command or "start" not in command:
        return None
    token = argv_token(command, "--api-key")
    if token and token.startswith("crsr_") and len(token) >= 20:
        return token
    return None


def worker_key():
    rows = process_rows()
    by_pid = {pid: (ppid, command) for pid, ppid, command in rows}
    found = []
    seen = set()
    pid = os.getpid()
    while pid and pid not in seen:
        seen.add(pid)
        row = by_pid.get(pid)
        if row is None:
            break
        ppid, command = row
        token = api_key_from_command(command)
        if token:
            found.append(token)
            break
        pid = ppid
    if not found:
        for pid, _ppid, command in rows:
            token = api_key_from_command(command)
            if token:
                found.append(token)
    unique = list(dict.fromkeys(found))
    if len(unique) == 1:
        return unique[0]
    if not unique:
        raise SystemExit(
            "No self-hosted worker process with --api-key was found. "
            "This command only works on a Cursor My Machines worker the "
            "cursor-agent-worker extension started. Do not create a new API key."
        )
    names = []
    for pid, _ppid, command in rows:
        if api_key_from_command(command):
            names.append(f"pid {pid} name={argv_token(command, '--name') or '?'}")
    raise SystemExit(
        "More than one worker API key is running. Refusing to guess:\n"
        + "\n".join(names)
    )


def redact(value, secret):
    if isinstance(value, str):
        return value.replace(secret, "[redacted]")
    if isinstance(value, list):
        return [redact(item, secret) for item in value]
    if isinstance(value, dict):
        return {key: redact(item, secret) for key, item in value.items()}
    return value


def request(secret, method, path, query=None, body=None):
    url = API + path
    if query:
        url += "?" + urllib.parse.urlencode(query, doseq=True)
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            parsed = json.loads(raw) if raw else None
            return resp.status, parsed
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            parsed = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            parsed = {"raw": raw[:800]}
        return exc.code, parsed


def emit(secret, status, payload, ok):
    print(json.dumps({"ok": ok, "status": status, "data": redact(payload, secret)}, indent=2))
    return 0 if ok else 1


def repo_filter(value):
    text = value.strip()
    for prefix in ("https://", "http://", "ssh://git@"):
        if text.startswith(prefix):
            text = text[len(prefix) :]
    if text.startswith("git@"):
        text = text[4:].replace(":", "/", 1)
    text = text.strip("/")
    if text.endswith(".git"):
        text = text[:-4]
    if text.startswith("www."):
        text = text[4:]
    if "/" not in text:
        raise SystemExit(f"not a repository: {value}")
    return text


def repo_url(value):
    host_path = repo_filter(value)
    return "https://" + host_path


def environment_json_string(path):
    with open(path, encoding="utf-8") as handle:
        parsed = json.load(handle)
    if not isinstance(parsed, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return json.dumps(parsed)


def cmd_me(secret, _args):
    status, data = request(secret, "GET", "/v1/me")
    return emit(secret, status, data, status == 200)


def cmd_list(secret, args):
    query = []
    if args.query:
        query.append(("query", args.query))
    if args.owner:
        query.append(("owner", args.owner))
    for repo in args.repo:
        query.append(("repo", repo_filter(repo)))
    query.append(("limit", "100"))
    items = []
    seen = set()
    cursor = None
    pages = 0
    while pages < 10:
        page_query = list(query)
        if cursor:
            page_query.append(("cursor", cursor))
        status, data = request(secret, "GET", "/v1/environments", page_query)
        if status != 200:
            return emit(secret, status, data, False)
        for item in data.get("items") or []:
            item_id = item.get("id")
            if item_id not in seen:
                seen.add(item_id)
                items.append(item)
        cursor = data.get("nextCursor")
        pages += 1
        if not cursor:
            break
    return emit(secret, 200, {"items": items, "truncated": bool(cursor)}, True)


def cmd_get(secret, args):
    status, data = request(secret, "GET", f"/v1/environments/{args.id}")
    return emit(secret, status, data, status == 200)


def cmd_history(secret, args):
    query = [("limit", str(args.limit))]
    if args.cursor:
        query.append(("cursor", args.cursor))
    status, data = request(
        secret,
        "GET",
        f"/v1/environments/{args.id}/history",
        query,
    )
    return emit(secret, status, data, status == 200)


def cmd_builds(secret, args):
    query = [("limit", "100")]
    items = []
    seen = set()
    cursor = None
    pages = 0
    while pages < 10:
        page_query = list(query)
        if cursor:
            page_query.append(("cursor", cursor))
        status, data = request(
            secret, "GET", f"/v1/environments/{args.id}/builds", page_query
        )
        if status != 200:
            return emit(secret, status, data, False)
        for item in data.get("items") or []:
            item_id = item.get("id")
            if item_id not in seen:
                seen.add(item_id)
                items.append(item)
        cursor = data.get("nextCursor")
        pages += 1
        if not cursor:
            break
    return emit(secret, 200, {"items": items, "truncated": bool(cursor)}, True)


def cmd_build_get(secret, args):
    status, data = request(
        secret, "GET", f"/v1/environments/{args.id}/builds/{args.build_id}"
    )
    return emit(secret, status, data, status == 200)


def cmd_active(secret, args):
    status, data = request(secret, "GET", f"/v1/environments/{args.id}/builds/active")
    return emit(secret, status, data, status == 200)


def cmd_create(secret, args):
    body = {
        "owner": args.owner,
        "name": args.name,
        "repos": [{"url": repo_url(repo)} for repo in args.repo],
        "environmentJson": environment_json_string(args.environment_json),
    }
    status, data = request(secret, "POST", "/v1/environments", body=body)
    return emit(secret, status, data, status == 201)


def cmd_update(secret, args):
    if not args.name and not args.environment_json:
        raise SystemExit("update needs --name or --environment-json")
    body = {}
    if args.name:
        body["name"] = args.name
    if args.environment_json:
        body["environmentJson"] = environment_json_string(args.environment_json)
    status, data = request(secret, "PATCH", f"/v1/environments/{args.id}", body=body)
    return emit(secret, status, data, status == 204)


def cmd_delete(secret, args):
    if not args.yes:
        raise SystemExit("delete requires --yes, and only after the user asked to delete this environment")
    status, data = request(secret, "DELETE", f"/v1/environments/{args.id}")
    return emit(secret, status, data, status == 200)


def cmd_build(secret, args):
    if args.ref and not args.draft:
        raise SystemExit("--ref requires --draft")
    body = {}
    if args.draft or args.ref:
        body = {"draft": bool(args.draft)}
        if args.ref:
            refs = []
            for item in args.ref:
                if "=" not in item:
                    raise SystemExit("--ref must be repo=branch")
                repo, ref = item.split("=", 1)
                refs.append({"repoUrl": repo_url(repo), "ref": ref})
            body["refs"] = refs
    status, data = request(
        secret, "POST", f"/v1/environments/{args.id}/builds", body=body
    )
    if status == 503:
        eprint("503 upstream_error: do not retry; list builds before starting another.")
    if status == 429:
        eprint("429 rate_limit_exceeded: do not retry; list builds before starting another.")
    return emit(secret, status, data, status == 202)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("me", help="Identify the worker API key without printing it")

    list_parser = sub.add_parser("list", help="List saved environments")
    list_parser.add_argument("--query")
    list_parser.add_argument("--owner", choices=("personal", "team"))
    list_parser.add_argument("--repo", action="append", default=[])

    get_parser = sub.add_parser("get")
    get_parser.add_argument("id")

    history_parser = sub.add_parser("history")
    history_parser.add_argument("id")
    history_parser.add_argument("--limit", type=int, default=20)
    history_parser.add_argument("--cursor")

    builds_parser = sub.add_parser("builds")
    builds_parser.add_argument("id")

    build_get_parser = sub.add_parser("build-get")
    build_get_parser.add_argument("id")
    build_get_parser.add_argument("build_id")

    active_parser = sub.add_parser("active")
    active_parser.add_argument("id")

    create_parser = sub.add_parser("create")
    create_parser.add_argument("--owner", choices=("personal", "team"), default="personal")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--repo", action="append", required=True)
    create_parser.add_argument("--environment-json", required=True)

    update_parser = sub.add_parser("update")
    update_parser.add_argument("id")
    update_parser.add_argument("--name")
    update_parser.add_argument("--environment-json")

    delete_parser = sub.add_parser("delete")
    delete_parser.add_argument("id")
    delete_parser.add_argument("--yes", action="store_true")

    build_parser = sub.add_parser("build")
    build_parser.add_argument("id")
    build_parser.add_argument("--draft", action="store_true")
    build_parser.add_argument("--ref", action="append", default=[])

    args = parser.parse_args()
    secret = worker_key()
    commands = {
        "me": cmd_me,
        "list": cmd_list,
        "get": cmd_get,
        "history": cmd_history,
        "builds": cmd_builds,
        "build-get": cmd_build_get,
        "active": cmd_active,
        "create": cmd_create,
        "update": cmd_update,
        "delete": cmd_delete,
        "build": cmd_build,
    }
    sys.exit(commands[args.command](secret, args))


if __name__ == "__main__":
    main()
