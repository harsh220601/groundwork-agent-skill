# Contributing to Groundwork

Thanks for helping improve Groundwork. Changes should preserve its core goal: make verified,
honest engineering behavior easier for coding agents to follow.

## Before opening a change

- Open an issue for substantial methodology, structure, or compatibility changes.
- Keep the installable skill portable: plain Markdown, portable Agent Skills frontmatter, and
  no required runtime dependencies.
- Put detailed procedures in `groundwork/references/` and keep `groundwork/SKILL.md` focused on
  the core workflow and routing.
- Back behavior claims with a reproducible exercise, trace, authoritative source, or test.
- Update `HONEST-LIMITS.md` when evidence does not support a broader claim.

## Local checks

Run these after your final edit:

```bash
python3 scripts/validate_skill.py
(cd exercises/bug-hunt && python3 -m unittest discover -s tests -v)
(cd exercises/broken-build && python3 -m unittest discover -s tests -v)
(cd exercises/zod-config && npm ci --ignore-scripts && node test.mjs)
```

If you change a stress-test fixture, also run its corresponding suite under `stress-tests/`.

## Pull requests

Describe:

1. The problem or observed agent failure.
2. The evidence that confirms it.
3. The smallest methodology or documentation change that addresses it.
4. The checks run after the final edit and their actual results.
5. Any remaining assumptions or limits.

Do not weaken existing checks to make a change pass. If an existing check is wrong, include
independent evidence for changing it.
