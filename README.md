# Groundwork

[![CI](https://github.com/harsh220601/groundwork-agent-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/harsh220601/groundwork-agent-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-groundwork-blue)](groundwork/SKILL.md)

**An evidence-first engineering methodology for coding agents.** Groundwork makes an agent
reproduce problems, read the real code, test its assumptions, verify its final work, and leave
useful project knowledge behind.

It is designed for software tasks including feature work, debugging, failing builds, code
review, unfamiliar-codebase exploration, API research, refactoring, configuration, and
performance work.

## Why Groundwork?

Coding agents commonly fail in two expensive ways: they invent facts they did not verify, or
declare success without running the result. Groundwork turns both failure modes into a concrete
workflow with five non-negotiables:

1. **Evidence or it did not happen.** Success claims include the command that ran and its real
   output.
2. **Read before referencing.** Files, APIs, and docs are opened before they are cited.
3. **Red before green.** Bugs get a failing regression check before the fix.
4. **Root cause over symptom.** Fixes address the cause without weakening checks.
5. **Leave the project smarter.** Project maps and learnings logs preserve verified context.

The full method is in [`groundwork/SKILL.md`](groundwork/SKILL.md). Detailed protocols are
loaded only when needed from [`groundwork/references/`](groundwork/references/).

## Install

The installable skill is the entire [`groundwork/`](groundwork/) directory.
For a ready-to-upload package, download
[`groundwork.zip`](https://github.com/harsh220601/groundwork-agent-skill/releases/latest/download/groundwork.zip)
from the latest release.

### Codex

```bash
git clone https://github.com/harsh220601/groundwork-agent-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R groundwork-agent-skill/groundwork "${CODEX_HOME:-$HOME/.codex}/skills/groundwork"
```

### Claude Code

```bash
git clone https://github.com/harsh220601/groundwork-agent-skill.git
mkdir -p "$HOME/.claude/skills"
cp -R groundwork-agent-skill/groundwork "$HOME/.claude/skills/groundwork"
```

### Other agent harnesses

Copy `groundwork/` into the harness's skills directory. The skill uses the portable Agent
Skills core frontmatter (`name` and `description`) and plain Markdown references. If the
harness does not automatically discover skills, point its standing instructions at
`groundwork/SKILL.md`.

See [`INSTALL.md`](INSTALL.md) for Claude web/API and generic installation details.

## Use

Invoke the skill explicitly when your harness supports named skills:

```text
Use $groundwork to diagnose and fix this failing test with evidence-first verification.
```

Its broad description is also designed to trigger automatically for software-engineering
tasks. For repositories where the method must always apply, add this to `AGENTS.md`,
`CLAUDE.md`, or the equivalent standing-instructions file:

```text
Before any engineering task, read groundwork/SKILL.md and follow it, including the
reference files it routes to.
```

## What is included?

| Path | Purpose |
| --- | --- |
| [`groundwork/`](groundwork/) | Installable skill and routed reference protocols |
| [`exercises/`](exercises/) | Reproducible Python and JavaScript engineering exercises |
| [`traces/`](traces/) | Worked bug-hunt, feature, research, and broken-build traces |
| [`stress-tests/`](stress-tests/) | Triggering and weaker-model evaluation artifacts |
| [`test-report.md`](test-report.md) | Stress-test results, defects found, and revisions made |
| [`research-notes.md`](research-notes.md) | Design research and methodology decisions |
| [`HONEST-LIMITS.md`](HONEST-LIMITS.md) | What the skill can and cannot transfer to an agent |

The traces and reports are development evidence, not timeless benchmark claims. Read
[`HONEST-LIMITS.md`](HONEST-LIMITS.md) before generalizing from them.

## Validate

```bash
python3 scripts/validate_skill.py
(cd exercises/bug-hunt && python3 -m unittest discover -s tests -v)
(cd exercises/broken-build && python3 -m unittest discover -s tests -v)
(cd exercises/zod-config && npm ci --ignore-scripts && node test.mjs)
```

GitHub Actions runs the validator plus the authored exercise and stress-test suites on every
push and pull request.

## Contributing

Issues and pull requests are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and
include the evidence used to justify methodology changes.

## License

Released under the [MIT License](LICENSE).
