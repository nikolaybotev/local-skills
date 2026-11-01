#!/bin/sh
set -eu

# Install skills from this repo into an agent skills directory.
# Re-running adds missing skills and overwrites skills from this source.
# It does not delete anything in the destination.
#
#   ./install.sh
#   ./install.sh ~/.cursor/skills
#   curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s
#   curl -fsSL https://raw.githubusercontent.com/nikolaybotev/local-skills/main/install.sh | sh -s -- ~/.cursor/skills

dest="${1:-$HOME/.agents/skills}"
repo_url="https://github.com/nikolaybotev/local-skills.git"
if [ -n "${LOCAL_SKILLS_REPO_URL:-}" ]; then
  repo_url="$LOCAL_SKILLS_REPO_URL"
fi
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
  script_dir=$(
    CDPATH=
    cd "$(dirname "$0")" && pwd
  )
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
dest=$(
  CDPATH=
  cd "$dest" && pwd
)

installed=0
updated=0
found=0

tar_excludes='--exclude .cache --exclude .venv --exclude .git --exclude __pycache__'

copy_skill() {
  dir=$1
  target=$2
  mkdir -p "$target"
  # shellcheck disable=SC2086
  tar -C "$dir" $tar_excludes -cf - . | tar -C "$target" -xf -
}

for dir in "$src"/*; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  found=1
  name=$(basename "$dir")
  target="$dest/$name"
  if [ -e "$target" ]; then
    copy_skill "$dir" "$target"
    echo "updated $name -> $target"
    updated=$((updated + 1))
  else
    copy_skill "$dir" "$target"
    echo "installed $name -> $target"
    installed=$((installed + 1))
  fi
done

if [ "$found" -eq 0 ]; then
  echo "error: no skills found in $src" >&2
  exit 1
fi

echo "done: $installed installed, $updated updated, destination $dest"
