"""The branch catalog: titles held and per-title copy availability."""

from typing import Dict, List

from .models import Book


class CatalogError(Exception):
    """Base class for catalog problems."""


class UnknownBookError(CatalogError):
    """Raised when an ISBN is not in the catalog."""


class DuplicateBookError(CatalogError):
    """Raised when a title is added under an ISBN that already exists."""


class NoCopiesAvailableError(CatalogError):
    """Raised when every copy of a title is already checked out."""


class Catalog:
    def __init__(self) -> None:
        self._books: Dict[str, Book] = {}
        self._available: Dict[str, int] = {}

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise DuplicateBookError(book.isbn)
        self._books[book.isbn] = book
        self._available[book.isbn] = book.copies_total

    def get_book(self, isbn: str) -> Book:
        try:
            return self._books[isbn]
        except KeyError:
            raise UnknownBookError(isbn) from None

    def available_copies(self, isbn: str) -> int:
        self.get_book(isbn)
        return self._available[isbn]

    def checkout_copy(self, isbn: str) -> None:
        if self.available_copies(isbn) < 1:
            raise NoCopiesAvailableError(isbn)
        self._available[isbn] -= 1

    def return_copy(self, isbn: str) -> None:
        book = self.get_book(isbn)
        if self._available[isbn] >= book.copies_total:
            raise CatalogError(
                "all copies of {} are already on the shelf".format(isbn)
            )
        self._available[isbn] += 1

    def search(self, text: str) -> List[Book]:
        """Case-insensitive substring search over titles and authors."""
        needle = text.lower()
        matches = [
            book
            for book in self._books.values()
            if needle in book.title.lower() or needle in book.author.lower()
        ]
        return sorted(matches, key=lambda book: book.title)
