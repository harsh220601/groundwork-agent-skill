#!/usr/bin/env python3
"""Validate the structure of the standing-orders document (root + skill reference copy).

The contract comes from the extraction prompt the document answers:
  - 10 areas, in a fixed order
  - every procedure written as trigger -> action ("When ... , ...")
  - one worked example per area, and the failure it prevents named
  - area 10 lists exactly 10 fake-competence patterns, each with a tell and a counter
  - a final gate checklist ending in the fix-and-re-check rule
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_DOC = ROOT / "fable-standing-orders.md"
REF_DOC = ROOT / "groundwork" / "references" / "standing-orders.md"

AREA_HEADINGS = [
    "## 1. Reading intent",
    "## 2. Breaking problems down",
    "## 3. Effort placement",
    "## 4. Verification",
    "## 5. Known vs guessed",
    "## 6. Self-attack",
    "## 7. Completeness",
    "## 8. Refusing to guess",
    "## 9. Delivery",
    "## 10. Fake competence",
]
GATE_HEADING = "## Final gate"
GATE_RULE = "fix and re-check. Never send anyway."

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def split_sections(text: str, label: str) -> dict[str, str]:
    positions = []
    for heading in AREA_HEADINGS + [GATE_HEADING]:
        idx = text.find(heading + "\n")
        check(idx != -1, f"{label}: missing section {heading!r}")
        positions.append((idx, heading))
    ordered = [p for p in positions if p[0] != -1]
    check(ordered == sorted(ordered), f"{label}: sections are out of order")
    sections: dict[str, str] = {}
    for i, (idx, heading) in enumerate(ordered):
        end = ordered[i + 1][0] if i + 1 < len(ordered) else len(text)
        sections[heading] = text[idx:end]
    return sections


def validate_doc(path: Path, label: str) -> None:
    if not path.is_file():
        errors.append(f"{label}: {path.name} does not exist")
        return
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text, label)

    for heading in AREA_HEADINGS:
        body = sections.get(heading, "")
        if not body:
            continue
        check(
            re.search(r"^\s*[-*]?\s*(?:\([a-z]\)\s+)?\**When ", body, re.MULTILINE) is not None,
            f"{label} {heading}: no trigger->action rule (line starting 'When ...')",
        )
        check("Example:" in body, f"{label} {heading}: no worked example ('Example:')")
        check("Prevents:" in body, f"{label} {heading}: failure not named ('Prevents:')")

    ten = sections.get(AREA_HEADINGS[9], "")
    if ten:
        patterns = re.findall(r"^\s*(?:###\s*)?\**\d+\.\s", ten, re.MULTILINE)
        check(len(patterns) >= 10, f"{label} area 10: found {len(patterns)} patterns, need 10")
        check(ten.count("Tell:") >= 10, f"{label} area 10: fewer than 10 'Tell:' markers")
        check(ten.count("Counter:") >= 10, f"{label} area 10: fewer than 10 'Counter:' markers")

    gate = sections.get(GATE_HEADING, "")
    if gate:
        items = re.findall(r"^\s*(?:\d+\.|- \[ \]|-)\s+\S", gate, re.MULTILINE)
        check(len(items) >= 5, f"{label} final gate: only {len(items)} checklist items, need >= 5")
        check(GATE_RULE in gate, f"{label} final gate: missing literal rule {GATE_RULE!r}")


def main() -> None:
    validate_doc(ROOT_DOC, "root")
    validate_doc(REF_DOC, "reference")

    skill = (ROOT / "groundwork" / "SKILL.md")
    if skill.is_file():
        check(
            "references/standing-orders.md" in skill.read_text(encoding="utf-8"),
            "SKILL.md does not route to references/standing-orders.md",
        )

    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        raise SystemExit(1)
    print("Validated standing orders: root + reference copies, 10 areas, final gate")


if __name__ == "__main__":
    main()
