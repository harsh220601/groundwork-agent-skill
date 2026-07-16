# Project Map — LogSift
Updated: 2026-07-16 | Verified against: `python3 -m unittest discover -s tests` → 22 passed

## What this is
A stdlib-only Python tool that parses HTTP access logs in Common Log Format and renders a
plain-text summary report (totals, error rate, top endpoints, status breakdown).

## Intended behavior
- Parses CLF lines into LogEntry records; malformed lines are skipped by default, or raise
  ParseError with `--strict`.
- Top endpoints group by path only — query strings are ignored (`/search?q=a` counts as
  `/search`); ordered by count desc, ties broken alphabetically.
- Error rate counts 5xx only. `-` response size counts as 0 bytes.
- Report format: title, totals, error rate, top-N endpoints (`--top`, default 3), status
  breakdown by class (2xx/4xx/5xx).

## Commands (all verified — run from project root)
- Test: `python3 -m unittest discover -s tests -v` → 22 passing
- Run:  `python3 -m logsift.cli tests/fixtures/sample_access.log --top 3` → renders text report
- JSON: `python3 -m logsift.cli <log> --json` → same data as text report, JSON object
- No build/lint step. Python 3.9+, stdlib only.

## Architecture at a glance
cli.py (argparse, file IO) → parser.py `parse_lines` builds `LogEntry` NamedTuples
(timestamp via timeutil.parse_timestamp) → stats.py aggregates (top_endpoints,
status_breakdown, error_rate, total_bytes, requests_per_hour) → report.py `render_report`
formats the text output.

## Where things live (curated — key files only)
- logsift/cli.py — entry point (`python3 -m logsift.cli`), owns flags
- logsift/parser.py — CLF regex, LogEntry, ParseError, strict/skip behavior
- logsift/stats.py — all aggregation; query-string stripping lives HERE, not in parser
- logsift/report.py — text + JSON rendering (render_report, render_json)
- logsift/timeutil.py — timestamp parsing + hour bucketing (renamed from utils.py)
- tests/helpers.py — shared make_entry factory for tests
- tests/fixtures/sample_access.log — 12-line realistic fixture

## Invariants and gotchas
- parser KEEPS query strings in LogEntry.path (test_keeps_query_string_in_path); grouping
  strips them in stats.top_endpoints. Do not move stripping into the parser.
- top_endpoints's keyword is `limit` (tests depend on it); report.py passes `limit=top`.
- requests_per_hour exists in stats.py but is not shown in the report.

## Decisions
- 2026-07-16 Query-string stripping placed in stats (not parser) per README contract + parser
  test that requires raw paths preserved.

## Handoff
(none — no work in flight)
