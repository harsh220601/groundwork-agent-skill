import io
import json
import unittest

from helpers import make_entry
from logsift.report import render_json


class RenderJsonTests(unittest.TestCase):
    def entries(self):
        return [
            make_entry(path="/home", status=200, size=100),
            make_entry(path="/search?q=desk", status=200, size=200),
            make_entry(path="/search?q=lamp", status=500, size=300),
        ]

    def test_structure_and_totals(self):
        data = json.loads(render_json(self.entries()))
        self.assertEqual(data["total_requests"], 3)
        self.assertEqual(data["total_bytes"], 600)
        self.assertAlmostEqual(data["error_rate"], 1 / 3)
        self.assertEqual(data["status_breakdown"], {"2xx": 2, "5xx": 1})

    def test_top_endpoints_grouped_and_limited(self):
        data = json.loads(render_json(self.entries(), top=1))
        self.assertEqual(data["top_endpoints"], [{"path": "/search", "count": 2}])

    def test_output_ends_with_newline(self):
        self.assertTrue(render_json(self.entries()).endswith("\n"))


if __name__ == "__main__":
    unittest.main()
