#!/usr/bin/env python3
"""Validate the portable structure of the Groundwork Agent Skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "groundwork"
SKILL_FILE = SKILL_DIR / "SKILL.md"
REFERENCE_DIR = SKILL_DIR / "references"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        fail("groundwork/SKILL.md must start with YAML frontmatter")

    try:
        frontmatter, body = text[4:].split("\n---\n", 1)
    except ValueError:
        fail("groundwork/SKILL.md frontmatter is not closed")

    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, body


def main() -> None:
    if not SKILL_FILE.is_file():
        fail("groundwork/SKILL.md is missing")

    text = SKILL_FILE.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)

    if set(fields) != {"name", "description"}:
        fail("frontmatter must contain exactly name and description")
    if fields["name"] != SKILL_DIR.name:
        fail("frontmatter name must match the skill directory name")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"]):
        fail("skill name must use lowercase letters, digits, and single hyphens")
    if not fields["description"] or len(fields["description"]) > 1024:
        fail("description must contain 1 to 1024 characters")

    body_lines = body.splitlines()
    if len(body_lines) >= 500:
        fail("SKILL.md body must remain below 500 lines")

    linked_names = set(re.findall(r"\(references/([^)]+\.md)\)", body))
    disk_names = {path.name for path in REFERENCE_DIR.glob("*.md")}
    missing = linked_names - disk_names
    unlinked = disk_names - linked_names
    if missing:
        fail(f"linked references are missing: {sorted(missing)}")
    if unlinked:
        fail(f"reference files are not linked from SKILL.md: {sorted(unlinked)}")

    forbidden = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if path.name == ".DS_Store" or "node_modules" in relative.parts or path.suffix == ".zip":
            forbidden.append(str(relative))
    if forbidden:
        fail(f"generated or vendored artifacts must not be committed: {forbidden}")

    if not (SKILL_DIR / "agents" / "openai.yaml").is_file():
        fail("groundwork/agents/openai.yaml is missing")

    print(
        f"Validated {fields['name']}: {len(disk_names)} references, "
        f"{len(body_lines)} SKILL.md body lines"
    )


if __name__ == "__main__":
    main()
