#!/usr/bin/env bash
set -euo pipefail

# Markdown and shell only. No compiler or package install.

# Install this checkout's skills so a branch tests its own tree.
# Cloud Agent Skills menu and runtime read ~/.cursor/skills-cursor.
# Existing skill folders are left in place.
repo_root=$(
  CDPATH=
  cd "$(dirname "$0")/.." && pwd
)
"${repo_root}/install.sh" "${HOME}/.cursor/skills-cursor"
