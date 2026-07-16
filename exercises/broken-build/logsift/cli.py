"""Command-line entry point: summarize an access log file."""

import argparse
import sys

from .parser import parse_lines
from .report import render_json, render_report


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="logsift",
        description="Summarize an HTTP access log in Common Log Format.",
    )
    parser.add_argument("logfile", help="path to the access log file")
    parser.add_argument(
        "--top",
        type=int,
        default=3,
        help="number of endpoints to show (default: 3)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail on the first malformed line instead of skipping it",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the report as JSON instead of text",
    )
    args = parser.parse_args(argv)

    with open(args.logfile, "r", encoding="utf-8") as handle:
        entries = parse_lines(handle, skip_malformed=not args.strict)

    renderer = render_json if args.json else render_report
    sys.stdout.write(renderer(entries, top=args.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
