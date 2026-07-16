"""Parsing for Common Log Format access logs."""

import re
from datetime import datetime
from typing import Iterable, List, NamedTuple

from .timeutil import parse_timestamp

LINE_RE = re.compile(
    r'^(?P<host>\S+) (?P<ident>\S+) (?P<user>\S+) '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r'(?P<status>\d{3}) (?P<size>\d+|-)$'
)


class ParseError(ValueError):
    """Raised when a log line does not match the expected format."""


class LogEntry(NamedTuple):
    host: str
    timestamp: datetime
    method: str
    path: str
    status: int
    size: int


def parse_line(line: str) -> LogEntry:
    """Parse one CLF line into a LogEntry, raising ParseError on junk."""
    match = LINE_RE.match(line.strip())
    if match is None:
        raise ParseError("unrecognized log line: %r" % line.strip())
    size_field = match.group("size")
    return LogEntry(
        host=match.group("host"),
        timestamp=parse_timestamp(match.group("time")),
        method=match.group("method"),
        path=match.group("path"),
        status=int(match.group("status")),
        size=0 if size_field == "-" else int(size_field),
    )


def parse_lines(lines: Iterable[str], skip_malformed: bool = True) -> List[LogEntry]:
    """Parse many lines, skipping blank lines.

    Malformed lines are dropped unless skip_malformed is False, in which
    case the first one raises ParseError.
    """
    entries = []
    for line in lines:
        if not line.strip():
            continue
        try:
            entries.append(parse_line(line))
        except ParseError:
            if not skip_malformed:
                raise
    return entries
