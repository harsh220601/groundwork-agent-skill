"""Core data types used across the circulation system."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Book:
    """A title held by the branch, possibly in multiple copies."""

    isbn: str
    title: str
    author: str
    copies_total: int = 1


@dataclass
class Member:
    """A registered library member.

    ``category`` is one of ``"regular"``, ``"student"`` or ``"faculty"``
    and determines which lending policy applies.
    """

    member_id: str
    name: str
    category: str = "regular"


@dataclass
class Loan:
    """A single copy checked out to a member.

    Fine terms are recorded at checkout time so that later policy
    changes do not retroactively alter what a borrower owes.
    """

    loan_id: int
    isbn: str
    member_id: str
    checked_out_on: date
    due_on: date
    daily_fine_cents: int
    max_fine_cents: int
    grace_days: int
    returned_on: Optional[date] = None
    renewals: int = 0

    @property
    def is_active(self) -> bool:
        return self.returned_on is None
