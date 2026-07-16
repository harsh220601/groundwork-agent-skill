import unittest
from datetime import date, timedelta

from libtrack.catalog import Catalog, NoCopiesAvailableError
from libtrack.loans import (
    AlreadyReturnedError,
    LoanLimitExceededError,
    LoanService,
    RenewalNotAllowedError,
    UnknownMemberError,
    calculate_fine_cents,
)
from libtrack.models import Book, Member
from libtrack.policies import PolicyEngine

DAY_ONE = date(2026, 3, 2)


class FineCalculationTest(unittest.TestCase):
    def test_on_time_return_owes_nothing(self):
        due = DAY_ONE
        self.assertEqual(calculate_fine_cents(due, due, 25, 1000, 2), 0)

    def test_early_return_owes_nothing(self):
        due = DAY_ONE
        returned = due - timedelta(days=4)
        self.assertEqual(calculate_fine_cents(due, returned, 25, 1000, 2), 0)

    def test_return_within_grace_owes_nothing(self):
        due = DAY_ONE
        returned = due + timedelta(days=2)
        self.assertEqual(calculate_fine_cents(due, returned, 25, 1000, 2), 0)

    def test_return_past_grace_charges_every_overdue_day(self):
        due = DAY_ONE
        returned = due + timedelta(days=3)
        self.assertEqual(calculate_fine_cents(due, returned, 25, 1000, 2), 75)

    def test_fine_is_capped(self):
        due = DAY_ONE
        returned = due + timedelta(days=90)
        self.assertEqual(calculate_fine_cents(due, returned, 25, 1000, 2), 1000)


class LoanServiceTest(unittest.TestCase):
    def setUp(self):
        self.catalog = Catalog()
        self.catalog.add_book(Book("978-1", "Dune", "Frank Herbert", copies_total=2))
        self.catalog.add_book(Book("978-2", "Hyperion", "Dan Simmons"))
        self.catalog.add_book(Book("978-3", "Contact", "Carl Sagan"))
        self.service = LoanService(self.catalog)
        self.service.register_member(Member("M-1", "Ada Lovelace"))
        self.service.register_member(Member("M-2", "Grace Hopper", category="student"))
        self.service.register_member(Member("M-3", "Alan Turing", category="faculty"))

    def test_checkout_sets_due_date_for_regular_member(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        self.assertEqual(loan.due_on, DAY_ONE + timedelta(days=21))

    def test_checkout_sets_due_date_for_student_member(self):
        loan = self.service.checkout("M-2", "978-1", on=DAY_ONE)
        self.assertEqual(loan.due_on, DAY_ONE + timedelta(days=28))

    def test_checkout_snapshots_fine_terms(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        self.assertEqual(loan.daily_fine_cents, 25)
        self.assertEqual(loan.max_fine_cents, 1000)
        self.assertEqual(loan.grace_days, 2)

    def test_checkout_reduces_availability(self):
        self.service.checkout("M-1", "978-1", on=DAY_ONE)
        self.assertEqual(self.catalog.available_copies("978-1"), 1)

    def test_checkout_fails_when_no_copies_left(self):
        self.service.checkout("M-1", "978-2", on=DAY_ONE)
        with self.assertRaises(NoCopiesAvailableError):
            self.service.checkout("M-2", "978-2", on=DAY_ONE)

    def test_checkout_unknown_member_raises(self):
        with self.assertRaises(UnknownMemberError):
            self.service.checkout("M-404", "978-1", on=DAY_ONE)

    def test_loan_limit_is_enforced(self):
        tight = {
            "loan_days": 21,
            "max_active_loans": 2,
            "renewal_limit": 2,
            "grace_days": 2,
            "daily_fine_cents": 25,
            "max_fine_cents": 1000,
        }
        service = LoanService(self.catalog, PolicyEngine(base_policy=tight))
        service.register_member(Member("M-9", "Mary Shelley"))
        service.checkout("M-9", "978-1", on=DAY_ONE)
        service.checkout("M-9", "978-2", on=DAY_ONE)
        with self.assertRaises(LoanLimitExceededError):
            service.checkout("M-9", "978-3", on=DAY_ONE)

    def test_return_restores_availability(self):
        loan = self.service.checkout("M-1", "978-2", on=DAY_ONE)
        self.service.return_book(loan.loan_id, on=DAY_ONE + timedelta(days=5))
        self.assertEqual(self.catalog.available_copies("978-2"), 1)

    def test_on_time_return_owes_nothing(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        fine = self.service.return_book(loan.loan_id, on=loan.due_on)
        self.assertEqual(fine, 0)

    def test_late_return_charges_regular_daily_rate(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        fine = self.service.return_book(loan.loan_id, on=loan.due_on + timedelta(days=7))
        self.assertEqual(fine, 7 * 25)

    def test_faculty_owe_no_fines(self):
        loan = self.service.checkout("M-3", "978-1", on=DAY_ONE)
        fine = self.service.return_book(loan.loan_id, on=loan.due_on + timedelta(days=30))
        self.assertEqual(fine, 0)

    def test_double_return_raises(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        self.service.return_book(loan.loan_id, on=loan.due_on)
        with self.assertRaises(AlreadyReturnedError):
            self.service.return_book(loan.loan_id, on=loan.due_on)

    def test_renewal_extends_from_due_date(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        original_due = loan.due_on
        self.service.renew(loan.loan_id, on=DAY_ONE + timedelta(days=5))
        self.assertEqual(loan.due_on, original_due + timedelta(days=21))
        self.assertEqual(loan.renewals, 1)

    def test_renewal_limit_is_enforced(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        self.service.renew(loan.loan_id, on=DAY_ONE + timedelta(days=1))
        self.service.renew(loan.loan_id, on=DAY_ONE + timedelta(days=2))
        with self.assertRaises(RenewalNotAllowedError):
            self.service.renew(loan.loan_id, on=DAY_ONE + timedelta(days=3))

    def test_overdue_loan_cannot_be_renewed(self):
        loan = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        with self.assertRaises(RenewalNotAllowedError):
            self.service.renew(loan.loan_id, on=loan.due_on + timedelta(days=1))

    def test_active_loans_excludes_returned(self):
        first = self.service.checkout("M-1", "978-1", on=DAY_ONE)
        self.service.checkout("M-1", "978-2", on=DAY_ONE)
        self.service.return_book(first.loan_id, on=DAY_ONE + timedelta(days=1))
        active = self.service.active_loans_for("M-1")
        self.assertEqual([loan.isbn for loan in active], ["978-2"])


if __name__ == "__main__":
    unittest.main()
