# LogSift

LogSift is a small command-line tool that summarizes HTTP access logs written in
Common Log Format (CLF). It is used internally to get a quick picture of traffic,
error rates, and hot endpoints from raw server logs without spinning up any
heavier tooling.

It has no dependencies outside the Python standard library and supports
Python 3.9+.

## What it does

Given a log file where each line looks like:

```
198.51.100.23 - - [01/Jul/2026:10:02:07 +0000] "GET /search?q=lamp HTTP/1.1" 200 2210
```

LogSift parses every line and prints a plain-text report containing:

- **Total requests** — the number of successfully parsed lines.
- **Total bytes** — the sum of response sizes. A size of `-` counts as 0 bytes.
- **Error rate** — the share of requests with a 5xx status code, as a percentage.
- **Top endpoints** — the most requested endpoints. Requests are grouped by
  path only: query strings are ignored, so `/search?q=lamp` and `/search?q=desk`
  both count toward `/search`. Endpoints are ordered by request count
  (descending), with ties broken alphabetically by path.
- **Status breakdown** — request counts bucketed by status class
  (`2xx`, `3xx`, `4xx`, `5xx`).

Malformed lines (truncated writes, junk from log rotation, etc.) are skipped by
default. In strict mode, the first malformed line raises a `ParseError`.

## Usage

From the project root:

```
python3 -m logsift.cli path/to/access.log
python3 -m logsift.cli path/to/access.log --top 5
python3 -m logsift.cli path/to/access.log --strict
python3 -m logsift.cli path/to/access.log --json
```

## Project layout

```
logsift/
    __init__.py     public API re-exports
    parser.py       CLF line parsing -> LogEntry records
    timeutil.py     timestamp parsing and hour bucketing
    stats.py        aggregate statistics over LogEntry records
    report.py       plain-text report rendering
    cli.py          command-line entry point
tests/              unittest suite and fixtures
```

## Running the tests

From the project root:

```
python3 -m unittest discover -s tests -v
```
