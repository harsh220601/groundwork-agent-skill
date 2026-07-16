# Project Map Specification (PROJECT-MAP.md)

## Contents
- Purpose and rules
- The template
- Creating the map (first contact)
- Updating the map (every change)
- Session close-out and handoff
- What stays OUT of the map

## Purpose and rules

`PROJECT-MAP.md` is a single markdown file at the project root that lets the next agent (or
you, next session) go straight to the right file instead of re-deriving the codebase.

Rules:
1. Hard cap ~200 lines. Overflow → prune or move detail into linked docs. An over-long map
   stops being read, which makes it worse than no map (readers trust it and miss things).
2. Plain markdown, edited directly with file tools. No generators, no build step.
3. Every command listed must have been RUN by whoever wrote it. The map records evidence, not
   intentions. A command you didn't run gets "(untested)" after it. Symmetrically, for READERS:
   the map is testimony — treat its claims as ASSUMED until you observe them yourself.
4. The map holds what CANNOT be derived by reading one file: commands, cross-file causality,
   invariants, decisions, gotchas. It is not a mirror of the directory listing.
5. If the project already uses AGENTS.md/CLAUDE.md: keep the map as its own file and add a
   one-line pointer from those files ("Codebase map: see PROJECT-MAP.md"), so every
   harness finds it.

## The template

```markdown
# Project Map — <project name>
Updated: <date> | Verified against: <test command> → <result>

## What this is
<2-4 lines: what the software does and for whom.>

## Intended behavior
<The contract in brief: what correct looks like. Key business rules, expected outputs.
This section is what "the app is supposed to do" means during debugging.>

## Commands (run from <where> — each line marked verified or (untested))
- Test:  `<command>` → currently <N passing / red because X / no test command exists — the
  check is <smoke script>>
- Build: `<command>`
- Run:   `<command>` → <what you should see>
- <lint/format/migrate as applicable>

## Architecture at a glance
<3-8 lines: the moving parts and the data flow between them.
"CLI (cli.py) → parser.py builds LogEntry records → stats.py aggregates → report.py renders".>

## Where things live (curated — key files only)
- path/one — <role, one line>
- path/two — <role, one line>
<Entry points, the files people actually edit, config. NOT every file.>

## Invariants and gotchas
- <"Changing X requires regenerating Y">
- <"Never mutate the shared policy dict — category resolution copies it (see LEARNINGS)">
- <non-obvious environment requirements>

## Decisions
- <date> <decision and one-line why>

## Handoff (only when work is in flight)
- Done: | In progress: | Files touched: | Next steps: | Constraints from user:
```

## Creating the map (first contact)

1. Gather evidence, cheaply: read README; list the tree (top 2 levels); read the main entry
   point and 2-3 most-imported modules; find the test/build commands (README, package
   manifest, CI config, Makefile).
2. RUN the test/build/run commands once each (step zero's baseline run already covers the
   test command — reuse its result); record actual results — including "currently red", which
   is vital context for whoever works here next. If NO test command exists, record that fact
   and point at the smoke/characterization script that serves as the check (see
   self-testing-loop). In a monorepo, the map lives at the package root you work in and covers
   that package; note the repo root and sibling packages in one line each.
3. Fill the template. Target 60-120 lines for a small project. 15 minutes of mapping saves
   every future session the same 15 minutes, compounding.
4. If the repo is huge: map the region you're working in properly, list the other top-level
   areas by name with one line each, and mark the map "partial — <area> mapped".

## Updating the map (every change)

After ANY change that alters behavior, structure, commands, or invariants — in the same
session, before reporting done:
1. Update the affected lines (edit in place; add/remove index entries; bump "Updated:").
2. New rule or trap discovered → add to Invariants. New/changed command → re-verify, update.
3. The check is one question: "would the map, as written, mislead the next agent about what I
   just did?" If yes, it's stale; fix it now. Report skips of this step honestly.

## Session close-out and handoff

Before ending any working session:
1. Re-read the map's Commands and Where-things-live sections against reality (30 seconds).
2. If work is unfinished, fill the Handoff section: done / in progress / files touched / next
   steps / user constraints. These five fields are what context-loss actually destroys.
3. If work is complete, clear any stale Handoff section.
4. Confirm LEARNINGS.md got its entries (see learnings-log-spec.md).

## What stays OUT of the map

- File-by-file descriptions of everything (derivable; bloats past the cap; goes stale fastest).
- Full API listings, dependency lists, directory dumps (derivable on demand).
- Prose history ("first we tried..."). Decisions get one line each in Decisions.
- Secrets, tokens, environment values. Names of required env vars are fine; values never.
