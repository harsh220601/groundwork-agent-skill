"""Shared builders for test data."""

from logsift.parser import LogEntry
from logsift.timeutil import parse_timestamp

DEFAULT_TS = "01/Jul/2026:10:00:00 +0000"


def make_entry(path="/", status=200, size=512, method="GET",
               host="203.0.113.7", ts=DEFAULT_TS):
    return LogEntry(
        host=host,
        timestamp=parse_timestamp(ts),
        method=method,
        path=path,
        status=status,
        size=size,
    )
