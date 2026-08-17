#!/usr/bin/env python3
"""Stop the browser instance that was launched for this skill.

Only kills a process whose command line contains this skill's user-data-dir
and remote-debugging-port. Never killall. Does not touch the user's personal
browser profile.
"""

import os
import signal
import subprocess
import sys
import time

from config import DEBUG_PORT, EXIT_ACTION, EXIT_OK, USER_DATA_DIR, probe_version


def browser_pids():
    try:
        output = subprocess.check_output(["ps", "-ax", "-o", "pid=,command="], text=True)
    except Exception as exc:
        print(f"FAIL: could not list processes: {exc}", file=sys.stderr)
        sys.exit(EXIT_ACTION)

    pids = []
    port_flag = f"--remote-debugging-port={DEBUG_PORT}"
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        pid_str, _, command = line.partition(" ")
        if USER_DATA_DIR in command and port_flag in command:
            try:
                pids.append((int(pid_str), command.strip()))
            except ValueError:
                continue
    return pids


def main():
    pids = browser_pids()
    if not pids:
        version = probe_version()
        if version is None:
            print("status=already_stopped")
            print(f"cdp=http://127.0.0.1:{DEBUG_PORT}")
            sys.exit(EXIT_OK)
        print(
            "FAIL: CDP is still up but no matching browser process was found. "
            "Not killing unrelated browsers.",
            file=sys.stderr,
        )
        sys.exit(EXIT_ACTION)

    for pid, command in pids:
        print(f"stopping pid={pid}", file=sys.stderr)
        print(f"command={command}", file=sys.stderr)
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            continue

    deadline = time.time() + 8
    while time.time() < deadline:
        if probe_version() is None and not browser_pids():
            print("status=stopped")
            sys.exit(EXIT_OK)
        time.sleep(0.2)

    still = browser_pids()
    if still:
        print("process still alive after SIGTERM, sending SIGKILL", file=sys.stderr)
        for pid, _command in still:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                continue
        time.sleep(0.5)

    if probe_version() is None:
        print("status=stopped")
        sys.exit(EXIT_OK)

    print("FAIL: browser still exposing CDP after stop", file=sys.stderr)
    sys.exit(EXIT_ACTION)


if __name__ == "__main__":
    main()
