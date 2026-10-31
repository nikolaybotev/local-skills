#!/usr/bin/env python3
import sys
from pathlib import Path


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end].strip("\n")


def field_value(block: str, key: str):
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith(f"{key}:"):
            i += 1
            continue
        rest = line[len(key) + 1 :].strip()
        if rest in (">-", "|"):
            folded = []
            i += 1
            while i < len(lines) and (
                lines[i].startswith("  ") or lines[i].startswith("\t")
            ):
                folded.append(lines[i].strip())
                i += 1
            return "\n".join(folded).strip()
        return rest.strip('"').strip()
    return None


def main() -> int:
    skills_root = Path(".agents/skills")
    if not skills_root.is_dir():
        print("missing .agents/skills", file=sys.stderr)
        return 1

    dirs = [p for p in skills_root.iterdir() if p.is_dir()]
    if not dirs:
        print("no skill directories", file=sys.stderr)
        return 1

    ok = True
    for skill_dir in sorted(dirs):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            print(f"{skill_dir.name}: missing SKILL.md", file=sys.stderr)
            ok = False
            continue
        block = parse_frontmatter(skill_md.read_text())
        if block is None:
            print(f"{skill_dir.name}: bad frontmatter fences", file=sys.stderr)
            ok = False
            continue
        name = field_value(block, "name")
        if name != skill_dir.name:
            print(f"{skill_dir.name}: name mismatch ({name!r})", file=sys.stderr)
            ok = False
        desc = field_value(block, "description")
        if not desc:
            print(f"{skill_dir.name}: missing description", file=sys.stderr)
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
