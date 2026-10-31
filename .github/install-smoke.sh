#!/usr/bin/env bash
set -euo pipefail

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
mkdir -p "$dest/stale-smoke-skill"
echo stale >"$dest/stale-smoke-skill/SKILL.md"
mkdir -p "$dest/unrelated-smoke-dir"
echo keep >"$dest/unrelated-smoke-dir/note.txt"

output=$(HOME="$home1" ./install.sh "$dest" 2>&1)
echo "$output" | grep -q "updated $first_name"
cmp -s "$dest/$first_name/SKILL.md" ".agents/skills/$first_name/SKILL.md"
test ! -e "$dest/stale-smoke-skill"
echo "$output" | grep -q "removed stale-smoke-skill"
test "$(cat "$dest/unrelated-smoke-dir/note.txt")" = "keep"

output2=$(HOME="$home1" ./install.sh "$dest" 2>&1)
for dir in .agents/skills/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/SKILL.md" ] || continue
  name=$(basename "$dir")
  echo "$output2" | grep -q "updated $name"
done
test ! -e "$dest/stale-smoke-skill"
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
