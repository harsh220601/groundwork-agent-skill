import os
import unittest
from datetime import datetime, timezone

from logsift.parser import ParseError, parse_line, parse_lines

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


class ParseLineTests(unittest.TestCase):
    def test_parses_a_standard_line(self):
        line = '203.0.113.7 - - [01/Jul/2026:10:03:02 +0000] "POST /api/orders HTTP/1.1" 201 64'
        entry = parse_line(line)
        self.assertEqual(entry.host, "203.0.113.7")
        self.assertEqual(entry.method, "POST")
        self.assertEqual(entry.path, "/api/orders")
        self.assertEqual(entry.status, 201)
        self.assertEqual(entry.size, 64)
        self.assertEqual(
            entry.timestamp,
            datetime(2026, 7, 1, 10, 3, 2, tzinfo=timezone.utc),
        )

    def test_keeps_query_string_in_path(self):
        line = '198.51.100.23 - - [01/Jul/2026:10:02:07 +0000] "GET /search?q=lamp HTTP/1.1" 200 2210'
        self.assertEqual(parse_line(line).path, "/search?q=lamp")

    def test_dash_size_counts_as_zero(self):
        line = '192.0.2.44 - - [01/Jul/2026:10:06:01 +0000] "GET /healthz HTTP/1.1" 204 -'
        self.assertEqual(parse_line(line).size, 0)

    def test_rejects_garbage(self):
        with self.assertRaises(ParseError):
            parse_line("not a log line at all")


class ParseLinesTests(unittest.TestCase):
    def test_skips_malformed_lines_by_default(self):
        lines = [
            '203.0.113.7 - - [01/Jul/2026:10:03:02 +0000] "GET / HTTP/1.1" 200 100',
            "truncated garbage",
            '203.0.113.7 - - [01/Jul/2026:10:03:05 +0000] "GET /about HTTP/1.1" 200 100',
        ]
        entries = parse_lines(lines)
        self.assertEqual([entry.path for entry in entries], ["/", "/about"])

    def test_strict_mode_raises(self):
        with self.assertRaises(ParseError):
            parse_lines(["truncated garbage"], skip_malformed=False)

    def test_sample_fixture_parses(self):
        with open(os.path.join(FIXTURES, "sample_access.log"), "r", encoding="utf-8") as handle:
            entries = parse_lines(handle)
        self.assertEqual(len(entries), 12)
        self.assertEqual(sum(1 for entry in entries if entry.status >= 500), 1)


if __name__ == "__main__":
    unittest.main()
