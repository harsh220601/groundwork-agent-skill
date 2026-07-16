import unittest

from libtrack.catalog import (
    Catalog,
    DuplicateBookError,
    NoCopiesAvailableError,
    UnknownBookError,
)
from libtrack.models import Book


class CatalogTest(unittest.TestCase):
    def setUp(self):
        self.catalog = Catalog()
        self.catalog.add_book(Book("978-1", "Dune", "Frank Herbert", copies_total=2))
        self.catalog.add_book(Book("978-2", "Hyperion", "Dan Simmons"))

    def test_get_book(self):
        self.assertEqual(self.catalog.get_book("978-1").title, "Dune")

    def test_unknown_isbn_raises(self):
        with self.assertRaises(UnknownBookError):
            self.catalog.get_book("978-404")

    def test_duplicate_isbn_raises(self):
        with self.assertRaises(DuplicateBookError):
            self.catalog.add_book(Book("978-1", "Dune (2nd ed.)", "Frank Herbert"))

    def test_checkout_and_return_adjust_availability(self):
        self.assertEqual(self.catalog.available_copies("978-1"), 2)
        self.catalog.checkout_copy("978-1")
        self.assertEqual(self.catalog.available_copies("978-1"), 1)
        self.catalog.return_copy("978-1")
        self.assertEqual(self.catalog.available_copies("978-1"), 2)

    def test_checkout_with_no_copies_raises(self):
        self.catalog.checkout_copy("978-2")
        with self.assertRaises(NoCopiesAvailableError):
            self.catalog.checkout_copy("978-2")

    def test_search_matches_title_and_author(self):
        self.assertEqual([b.isbn for b in self.catalog.search("dune")], ["978-1"])
        self.assertEqual([b.isbn for b in self.catalog.search("simmons")], ["978-2"])
        self.assertEqual(self.catalog.search("asimov"), [])


if __name__ == "__main__":
    unittest.main()
