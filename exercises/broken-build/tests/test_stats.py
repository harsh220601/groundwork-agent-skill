import unittest

from helpers import make_entry
from logsift.stats import (
    error_rate,
    requests_per_hour,
    status_breakdown,
    top_endpoints,
    total_bytes,
)


class TopEndpointsTests(unittest.TestCase):
    def test_orders_by_count_then_path(self):
        entries = (
            [make_entry(path="/c")] * 3
            + [make_entry(path="/a")] * 2
            + [make_entry(path="/b")] * 2
        )
        self.assertEqual(
            top_endpoints(entries, limit=3),
            [("/c", 3), ("/a", 2), ("/b", 2)],
        )

    def test_limit_truncates(self):
        entries = [
            make_entry(path="/a"),
            make_entry(path="/b"),
            make_entry(path="/b"),
        ]
        self.assertEqual(top_endpoints(entries, limit=1), [("/b", 2)])

    def test_query_strings_are_ignored_when_grouping(self):
        entries = [
            make_entry(path="/search?q=lamp"),
            make_entry(path="/search?q=desk"),
            make_entry(path="/home"),
        ]
        self.assertEqual(
            top_endpoints(entries, limit=5),
            [("/search", 2), ("/home", 1)],
        )


class StatusTests(unittest.TestCase):
    def test_status_breakdown_buckets_by_class(self):
        entries = [
            make_entry(status=200),
            make_entry(status=201),
            make_entry(status=404),
            make_entry(status=500),
            make_entry(status=503),
        ]
        self.assertEqual(status_breakdown(entries), {"2xx": 2, "4xx": 1, "5xx": 2})

    def test_error_rate_counts_5xx_only(self):
        entries = [
            make_entry(status=200),
            make_entry(status=404),
            make_entry(status=500),
        ]
        self.assertAlmostEqual(error_rate(entries), 1 / 3)

    def test_error_rate_of_empty_log_is_zero(self):
        self.assertEqual(error_rate([]), 0.0)


class VolumeTests(unittest.TestCase):
    def test_total_bytes(self):
        entries = [make_entry(size=100), make_entry(size=250)]
        self.assertEqual(total_bytes(entries), 350)

    def test_requests_per_hour(self):
        entries = [
            make_entry(ts="01/Jul/2026:10:05:00 +0000"),
            make_entry(ts="01/Jul/2026:10:59:59 +0000"),
            make_entry(ts="01/Jul/2026:11:00:00 +0000"),
        ]
        self.assertEqual(
            requests_per_hour(entries),
            {"2026-07-01 10:00": 2, "2026-07-01 11:00": 1},
        )


if __name__ == "__main__":
    unittest.main()
