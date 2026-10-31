#!/usr/bin/env bash
set -euo pipefail

# Piped install without a checkout: default URL, no override env (unset GITHUB_REPOSITORY in Actions).
home_pipe=$(mktemp -d)
pipe_dest=$(mktemp -d)
(
  unset LOCAL_SKILLS_REPO_URL
  unset GITHUB_REPOSITORY
  HOME="$home_pipe" sh -s -- "$pipe_dest" <./install.sh
)
pipe_installed=0
for dir in "$pipe_dest"/*; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  pipe_installed=$((pipe_installed + 1))
done
test "$pipe_installed" -ge 1

fake_git_dir=$(mktemp -d)
printf '%s\n' '#!/bin/sh' 'exit 99' >"$fake_git_dir/git"
chmod +x "$fake_git_dir/git"
export PATH="$fake_git_dir:$PATH"

home1=$(mktemp -d)
dest=$(mktemp -d)
HOME="$home1" ./install.sh "$dest"

installed=0
for dir in .agents/skills/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  name=$(basename "$dir")
  test -f "$dest/$name/SKILL.md"
  installed=$((installed + 1))
done
test "$installed" -ge 1

first_name=""
for dir in .agents/skills/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  first_name=$(basename "$dir")
  break
done
canary="$dest/$first_name/canary-smoke"
echo canary >"$canary"
output=$(HOME="$home1" ./install.sh "$dest" 2>&1)
for dir in .agents/skills/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  name=$(basename "$dir")
  echo "$output" | grep -q "skip $name"
done
test "$(cat "$canary")" = "canary"

home2=$(mktemp -d)
HOME="$home2" ./install.sh
for dir in .agents/skills/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  name=$(basename "$dir")
  test -f "$home2/.agents/skills/$name/SKILL.md"
done

home3=$(mktemp -d)
HOME="$home3" bash .cursor/install.sh
for dir in .agents/skills/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  name=$(basename "$dir")
  test -f "$home3/.cursor/skills-cursor/$name/SKILL.md"
  test ! -e "$home3/.agents/skills/$name"
done
