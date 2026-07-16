"""Report rendering: plain text and JSON."""

import json

from .stats import error_rate, status_breakdown, top_endpoints, total_bytes

TITLE = "LogSift Report"


def _pct(value):
    return "%.1f%%" % (value * 100)


def render_report(entries, top=3):
    """Render the summary report for a sequence of LogEntry records."""
    entries = list(entries)
    lines = [TITLE, "=" * len(TITLE)]
    lines.append("Total requests: %d" % len(entries))
    lines.append("Total bytes:    {:,}".format(total_bytes(entries)))
    lines.append("Error rate:     %s" % _pct(error_rate(entries)))
    lines.append("")
    lines.append("Top endpoints:")
    for path, count in top_endpoints(entries, limit=top):
        lines.append("  %-32s %d" % (path, count))
    lines.append("")
    lines.append("Status breakdown:")
    for bucket, count in sorted(status_breakdown(entries).items()):
        lines.append("  %s  %d" % (bucket, count))
    return "\n".join(lines) + "\n"


def render_json(entries, top=3):
    """Render the summary report as a JSON document (same data as the text report)."""
    entries = list(entries)
    payload = {
        "total_requests": len(entries),
        "total_bytes": total_bytes(entries),
        "error_rate": error_rate(entries),
        "top_endpoints": [
            {"path": path, "count": count}
            for path, count in top_endpoints(entries, limit=top)
        ],
        "status_breakdown": status_breakdown(entries),
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
