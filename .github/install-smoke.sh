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

echo tampered >"$dest/$first_name/SKILL.md"
mkdir -p "$dest/extra-smoke-skill"
echo extra >"$dest/extra-smoke-skill/SKILL.md"
mkdir -p "$dest/unrelated-smoke-dir"
echo keep >"$dest/unrelated-smoke-dir/note.txt"

output=$(HOME="$home1" ./install.sh "$dest" 2>&1)
echo "$output" | grep -q "updated $first_name"
cmp -s "$dest/$first_name/SKILL.md" ".agents/skills/$first_name/SKILL.md"
test -f "$dest/extra-smoke-skill/SKILL.md"
test "$(cat "$dest/extra-smoke-skill/SKILL.md")" = "extra"
echo "$output" | grep -vq "removed "
test "$(cat "$dest/unrelated-smoke-dir/note.txt")" = "keep"

output2=$(HOME="$home1" ./install.sh "$dest" 2>&1)
for dir in .agents/skills/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  name=$(basename "$dir")
  echo "$output2" | grep -q "updated $name"
done
test -f "$dest/extra-smoke-skill/SKILL.md"
test "$(cat "$dest/unrelated-smoke-dir/note.txt")" = "keep"

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
