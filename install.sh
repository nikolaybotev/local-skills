#!/bin/sh
set -eu

# Install skills from this repo into an agent skills directory.
# Existing skill folders are left alone.
#
#   ./install.sh
#   ./install.sh ~/.cursor/skills
#   curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s
#   curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s -- ~/.cursor/skills

dest="${1:-$HOME/.agents/skills}"
repo_url="https://github.com/nikolaybotev/local-skills.git"
tmp=""

cleanup() {
  if [ -n "$tmp" ]; then
    rm -rf "$tmp"
  fi
}

if [ "$#" -gt 1 ]; then
  echo "usage: install.sh [destination]" >&2
  exit 1
fi

case "$dest" in
  -h|--help)
    echo "usage: install.sh [destination]"
    echo "destination defaults to ~/.agents/skills"
    exit 0
    ;;
esac

# A checkout can install its own tree. A piped script has no tree, so clone.
src=""
if [ -f "$0" ]; then
  script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
  if [ -d "$script_dir/.agents/skills" ]; then
    src="$script_dir/.agents/skills"
  fi
fi

if [ -z "$src" ]; then
  if ! command -v git >/dev/null 2>&1; then
    echo "error: git is required to download the skills." >&2
    exit 1
  fi
  tmp=$(mktemp -d)
  trap cleanup EXIT
  git clone --depth 1 "$repo_url" "$tmp/local-skills"
  src="$tmp/local-skills/.agents/skills"
fi

if [ ! -d "$src" ]; then
  echo "error: skills directory not found: $src" >&2
  exit 1
fi

mkdir -p "$dest"
dest=$(CDPATH= cd "$dest" && pwd)

installed=0
skipped=0
found=0

for dir in "$src"/*; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  found=1
  name=$(basename "$dir")
  target="$dest/$name"
  if [ -e "$target" ]; then
    echo "skip $name (already at $target)"
    skipped=$((skipped + 1))
    continue
  fi
  mkdir -p "$target"
  # Shell caches and virtualenvs are not part of the skill.
  tar -C "$dir" \
    --exclude .cache \
    --exclude .venv \
    --exclude .git \
    --exclude __pycache__ \
    -cf - . | tar -C "$target" -xf -
  echo "installed $name -> $target"
  installed=$((installed + 1))
done

if [ "$found" -eq 0 ]; then
  echo "error: no skills found in $src" >&2
  exit 1
fi

echo "done: $installed installed, $skipped skipped, destination $dest"
