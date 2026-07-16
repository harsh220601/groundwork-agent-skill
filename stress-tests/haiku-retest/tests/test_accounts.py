import unittest
from datetime import date

from libtrack.catalog import Catalog
from libtrack.loans import (
    LoanService,
    OutstandingFinesError,
    PaymentError,
    UnknownMemberError,
)
from libtrack.models import Book, Member


def make_service(copies=5):
    catalog = Catalog()
    catalog.add_book(Book("978-1", "Fluent Python", "Ramalho", copies_total=copies))
    service = LoanService(catalog)
    service.register_member(Member("M-1", "Ada", category="regular"))
    return service


def run_up_fine(service, days_late, on=date(2026, 1, 1)):
    """Check out and return late; returns the fine posted (cents)."""
    loan = service.checkout("M-1", "978-1", on=on)
    from datetime import timedelta

    return service.return_book(loan.loan_id, on=loan.due_on + timedelta(days=days_late))


class BalanceTest(unittest.TestCase):
    def test_new_member_owes_nothing(self):
        service = make_service()
        self.assertEqual(service.balance_cents("M-1"), 0)

    def test_unknown_member_raises(self):
        service = make_service()
        with self.assertRaises(UnknownMemberError):
            service.balance_cents("M-404")

    def test_fine_posts_to_balance(self):
        service = make_service()
        fine = run_up_fine(service, days_late=10)  # 10 * 25 = 250
        self.assertEqual(fine, 250)
        self.assertEqual(service.balance_cents("M-1"), 250)

    def test_on_time_return_posts_nothing(self):
        service = make_service()
        fine = run_up_fine(service, days_late=0)
        self.assertEqual(fine, 0)
        self.assertEqual(service.balance_cents("M-1"), 0)

    def test_fines_accumulate_across_loans(self):
        service = make_service()
        run_up_fine(service, days_late=10)  # 250
        run_up_fine(service, days_late=4)   # 4 * 25 = 100
        self.assertEqual(service.balance_cents("M-1"), 350)


class PaymentTest(unittest.TestCase):
    def test_payment_reduces_balance(self):
        service = make_service()
        run_up_fine(service, days_late=10)  # 250
        service.record_payment("M-1", 100)
        self.assertEqual(service.balance_cents("M-1"), 150)

    def test_payment_must_be_positive(self):
        service = make_service()
        run_up_fine(service, days_late=10)
        for bad in (0, -5):
            with self.assertRaises(PaymentError):
                service.record_payment("M-1", bad)

    def test_cannot_overpay(self):
        service = make_service()
        run_up_fine(service, days_late=10)  # 250
        with self.assertRaises(PaymentError):
            service.record_payment("M-1", 251)
        self.assertEqual(service.balance_cents("M-1"), 250)

    def test_payment_for_unknown_member_raises(self):
        service = make_service()
        with self.assertRaises(UnknownMemberError):
            service.record_payment("M-404", 100)


class CheckoutBlockTest(unittest.TestCase):
    def test_balance_at_threshold_blocks_checkout(self):
        service = make_service()
        run_up_fine(service, days_late=20)  # 20 * 25 = 500 == threshold
        with self.assertRaises(OutstandingFinesError):
            service.checkout("M-1", "978-1", on=date(2026, 6, 1))

    def test_balance_below_threshold_allows_checkout(self):
        service = make_service()
        run_up_fine(service, days_late=19)  # 475 < 500
        loan = service.checkout("M-1", "978-1", on=date(2026, 6, 1))
        self.assertTrue(loan.is_active)

    def test_paying_down_reenables_checkout(self):
        service = make_service()
        run_up_fine(service, days_late=20)  # 500
        service.record_payment("M-1", 1)
        loan = service.checkout("M-1", "978-1", on=date(2026, 6, 1))
        self.assertTrue(loan.is_active)

    def test_blocked_renewal(self):
        service = make_service()
        loan = service.checkout("M-1", "978-1", on=date(2026, 1, 1))
        run_up_fine(service, days_late=20, on=date(2026, 1, 2))  # second copy, 500 fine
        with self.assertRaises(OutstandingFinesError):
            service.renew(loan.loan_id, on=date(2026, 1, 10))


if __name__ == "__main__":
    unittest.main()
