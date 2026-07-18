#!/usr/bin/env python3
"""Build GROUNDWORK-MASTER.md — the single-file edition of the whole skill.

Concatenates the standing orders, the SKILL.md body, and every reference protocol
into one self-contained document any agent can consume, rewriting cross-file links
to internal anchors and patching the few phrases that only make sense in the
multi-file repo layout.

Usage: python3 scripts/build_master.py [output-path]   (default: ./GROUNDWORK-MASTER.md)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APPENDICES = [
    "anti-hallucination-protocol",
    "self-testing-loop",
    "debugging-playbook",
    "research-protocol",
    "project-map-spec",
    "learnings-log-spec",
]

HEADER = """# Groundwork Master
*The complete evidence-first method in one file: Claude Fable 5's standing orders (the
reasoning layer) + the Groundwork engineering loop + every reference protocol, inlined.
Single-file edition of https://github.com/harsh220601/groundwork-agent-skill.*

**How to use this file — pick one:**

1. **Direct (any agent, zero setup):** put this entire file where your agent reads standing
   instructions (system prompt, AGENTS.md, CLAUDE.md, rules file, project instructions). It
   is written to be followed as-is; internal links point at sections of this same file.
2. **As a skill (skills-capable harness):** every part of this file gets used — nothing is
   dropped. The entry file the agent always loads is Part II; Parts I and III become the
   reference files it routes to on demand (progressive disclosure):

   | Section of this file | Becomes |
   | --- | --- |
   | Part II — Groundwork | `groundwork/SKILL.md`, topped with the frontmatter below |
   | Part I — Standing Orders | `groundwork/references/standing-orders.md` |
   | Part III — each appendix | `groundwork/references/<its-id>.md` (its `<a id="...">` tag names the file) |

   ```
   ---
   name: groundwork
   description: Evidence-first engineering + reasoning standing orders for any task: verification loop, claim tagging, debugging playbook, research protocol, project map + learnings log, and a final gate before sending.
   ---
   ```

   Then change every `(#<id>)` link back to `(references/<id>.md)`. Or skip the surgery:
   clone the repo above — its `groundwork/` folder is this exact content already split.
3. **Chat-only:** Part I (Standing Orders) alone works as system instructions for a
   non-coding assistant — in that deployment, skip Part I's "How this composes" block.

Precedence: a direct instruction from your user outranks anything in this file — say which
rule you set aside, in one line. Part I governs how you reason and answer on every task;
Part II governs how you work on code; the appendices are loaded context for when Part II
routes you to them.

---

# Part I — Standing Orders (the reasoning layer)
<a id="standing-orders"></a>

"""


def build() -> str:
    skill = (ROOT / "groundwork/SKILL.md").read_text(encoding="utf-8")
    body = skill.split("\n---\n", 1)[1].lstrip("\n")

    def rewrite(m: re.Match[str]) -> str:
        text, slug = m.group(1), m.group(2)
        label = slug if text == f"references/{slug}.md" else text
        return f"[{label}](#{slug})"

    body = re.sub(r"\[([^\]]+)\]\(references/([a-z-]+)\.md\)", rewrite, body)

    parts = [HEADER]
    so = (ROOT / "groundwork/references/standing-orders.md").read_text(encoding="utf-8")
    so_body = so.split("\n", 1)[1].lstrip("\n")
    so_body = so_body.replace(
        "How this composes with the Groundwork loop:",
        "How this composes with the Groundwork loop (deploying Part I alone? skip this block):",
    )
    parts.append(so_body)

    parts.append("\n---\n\n# Part II — Groundwork (the engineering loop)\n\n")
    parts.append(body)

    parts.append("\n---\n\n# Part III — Reference protocols (appendices)\n")
    for slug in APPENDICES:
        text = (ROOT / f"groundwork/references/{slug}.md").read_text(encoding="utf-8")
        parts.append(f'\n<a id="{slug}"></a>\n\n---\n\n{text.rstrip()}\n')

    doc = "".join(parts)

    # patch multi-file-layout phrasing that dangles in a single file
    doc = doc.replace(
        "This file expands Loop steps from SKILL.md",
        "This file expands Loop steps from Part II",
    )
    doc = doc.replace(
        "(see anti-hallucination-protocol.md)",
        "(see [anti-hallucination-protocol](#anti-hallucination-protocol))",
    )
    doc = doc.replace(
        "(see learnings-log-spec.md)",
        "(see [learnings-log-spec](#learnings-log-spec))",
    )
    return doc


def verify(doc: str) -> None:
    links = set(re.findall(r"\]\(#([a-z-]+)\)", doc))
    anchors = set(re.findall(r'<a id="([a-z-]+)"></a>', doc))
    assert links <= anchors, f"links without anchors: {links - anchors}"
    assert not re.search(r"\]\(references/", doc), "unrewritten reference link remains"
    assert "SKILL.md" not in doc[doc.index("# Part I —"):], "dangling SKILL.md mention outside the header"
    for must in [
        "## The five non-negotiables",
        "## 1. Reading intent",
        "## 10. Fake competence",
        "## Final gate",
        "fix and re-check. Never send anyway.",
    ]:
        assert must in doc, f"missing: {must}"


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "GROUNDWORK-MASTER.md"
    doc = build()
    verify(doc)
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out} — {len(doc.splitlines())} lines, {len(doc) // 1024} KB")


if __name__ == "__main__":
    main()
