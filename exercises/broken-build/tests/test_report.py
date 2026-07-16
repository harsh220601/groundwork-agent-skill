import os
import unittest

from helpers import make_entry
from logsift.parser import parse_lines
from logsift.report import render_report

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


class RenderReportTests(unittest.TestCase):
    def test_totals_and_error_rate(self):
        entries = [
            make_entry(path="/a", size=100),
            make_entry(path="/a", size=200),
            make_entry(path="/b", status=500, size=50),
        ]
        report = render_report(entries)
        self.assertIn("Total requests: 3", report)
        self.assertIn("Total bytes:    350", report)
        self.assertIn("Error rate:     33.3%", report)

    def test_top_endpoints_section_groups_query_strings(self):
        entries = [
            make_entry(path="/search?q=lamp"),
            make_entry(path="/search?q=desk"),
            make_entry(path="/home"),
        ]
        report = render_report(entries, top=2)
        endpoint_lines = [ln for ln in report.splitlines() if ln.startswith("  /")]
        self.assertEqual(len(endpoint_lines), 2)
        self.assertRegex(endpoint_lines[0], r"^  /search\s+2$")
        self.assertRegex(endpoint_lines[1], r"^  /home\s+1$")

    def test_respects_top_argument(self):
        entries = [make_entry(path="/page-%d" % i) for i in range(6)]
        report = render_report(entries, top=4)
        endpoint_lines = [ln for ln in report.splitlines() if ln.startswith("  /")]
        self.assertEqual(len(endpoint_lines), 4)

    def test_report_from_sample_fixture(self):
        with open(os.path.join(FIXTURES, "sample_access.log"), "r", encoding="utf-8") as handle:
            entries = parse_lines(handle)
        report = render_report(entries)
        self.assertIn("Total requests: 12", report)
        search_lines = [ln for ln in report.splitlines() if "/search" in ln]
        self.assertEqual(len(search_lines), 1)
        self.assertRegex(search_lines[0], r"^  /search\s+3$")


if __name__ == "__main__":
    unittest.main()
