"""Helpers for working with access-log timestamps."""

from datetime import datetime

TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def parse_timestamp(text):
    """Parse a CLF timestamp such as '01/Jul/2026:10:02:07 +0000'."""
    return datetime.strptime(text, TIMESTAMP_FORMAT)


def hour_bucket(moment):
    """Return the hour bucket label for a datetime, e.g. '2026-07-01 10:00'."""
    return moment.strftime("%Y-%m-%d %H:00")
