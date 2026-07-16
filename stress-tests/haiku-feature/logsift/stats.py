"""Aggregate statistics over parsed log entries."""

from collections import Counter
from typing import Dict, Iterable, List, Tuple

from .parser import LogEntry
from .timeutil import hour_bucket


def top_endpoints(entries: Iterable[LogEntry], limit: int = 5) -> List[Tuple[str, int]]:
    """The most requested endpoints as (path, count) pairs.

    Ordered by request count descending, ties broken alphabetically by path.
    """
    # Group by path only: /search?q=lamp and /search?q=desk both count as /search.
    counts = Counter(entry.path.split("?", 1)[0] for entry in entries)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:limit]


def status_breakdown(entries: Iterable[LogEntry]) -> Dict[str, int]:
    """Request counts bucketed by status class, e.g. {'2xx': 10, '5xx': 1}."""
    counts = Counter("%dxx" % (entry.status // 100) for entry in entries)
    return dict(counts)


def error_rate(entries: Iterable[LogEntry]) -> float:
    """Share of requests with a 5xx status, between 0.0 and 1.0."""
    entries = list(entries)
    if not entries:
        return 0.0
    errors = sum(1 for entry in entries if entry.status >= 500)
    return errors / len(entries)


def total_bytes(entries: Iterable[LogEntry]) -> int:
    """Sum of response sizes across all entries."""
    return sum(entry.size for entry in entries)


def requests_per_hour(entries: Iterable[LogEntry]) -> Dict[str, int]:
    """Request counts keyed by hour bucket, e.g. {'2026-07-01 10:00': 4}."""
    counts = Counter(hour_bucket(entry.timestamp) for entry in entries)
    return dict(counts)
