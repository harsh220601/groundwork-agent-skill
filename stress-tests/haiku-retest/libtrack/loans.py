"""Circulation desk operations: checkouts, returns, renewals and fines."""

from datetime import date, timedelta
from typing import Dict, List, Optional

from .catalog import Catalog
from .models import Loan, Member
from .policies import PolicyEngine


class CirculationError(Exception):
    """Base class for circulation problems."""


class UnknownMemberError(CirculationError):
    """Raised when a member id is not registered."""


class UnknownLoanError(CirculationError):
    """Raised when a loan id does not exist."""


class LoanLimitExceededError(CirculationError):
    """Raised when a member is already at their active-loan limit."""


class AlreadyReturnedError(CirculationError):
    """Raised when acting on a loan that has been closed out."""


class RenewalNotAllowedError(CirculationError):
    """Raised when a loan cannot be renewed."""


class OutstandingFinesError(CirculationError):
    """Raised when unpaid fines block a checkout or renewal."""


class PaymentError(CirculationError):
    """Raised when a fine payment is invalid."""


# Members owing this much or more cannot check out or renew until they pay
# down the balance.  $5.00 is half the regular fine cap: high enough that a
# single slightly-late return never locks anyone out, low enough that fines
# cannot pile up unboundedly across loans.
CHECKOUT_BLOCK_THRESHOLD_CENTS = 500


def calculate_fine_cents(
    due_on: date,
    returned_on: date,
    daily_fine_cents: int,
    max_fine_cents: int,
    grace_days: int,
) -> int:
    """Fine owed for a return, in cents.

    Returns within the grace window owe nothing.  Once past the grace
    window, the fine covers every day past the due date (grace days
    included), capped at ``max_fine_cents``.
    """
    days_overdue = (returned_on - due_on).days
    if days_overdue <= grace_days:
        return 0
    fine = days_overdue * daily_fine_cents
    return min(fine, max_fine_cents)


class LoanService:
    """Front-desk operations for a single branch."""

    def __init__(self, catalog: Catalog, policy_engine: Optional[PolicyEngine] = None) -> None:
        self._catalog = catalog
        self._policies = policy_engine or PolicyEngine()
        self._members: Dict[str, Member] = {}
        self._loans: Dict[int, Loan] = {}
        self._balances: Dict[str, int] = {}
        self._next_loan_id = 1

    # -- members ---------------------------------------------------------

    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member

    def get_member(self, member_id: str) -> Member:
        try:
            return self._members[member_id]
        except KeyError:
            raise UnknownMemberError(member_id) from None

    # -- accounts --------------------------------------------------------

    def balance_cents(self, member_id: str) -> int:
        """Outstanding fine balance for ``member_id``, in cents."""
        self.get_member(member_id)
        return self._balances.get(member_id, 0)

    def record_payment(self, member_id: str, cents: int) -> int:
        """Apply a payment and return the remaining balance, in cents."""
        balance = self.balance_cents(member_id)
        if cents <= 0:
            raise PaymentError("payment must be a positive amount of cents")
        if cents > balance:
            raise PaymentError(
                "payment of {} exceeds outstanding balance of {}".format(cents, balance)
            )
        self._balances[member_id] = balance - cents
        return self._balances[member_id]

    def _require_clear_balance(self, member_id: str) -> None:
        balance = self.balance_cents(member_id)
        if balance >= CHECKOUT_BLOCK_THRESHOLD_CENTS:
            raise OutstandingFinesError(
                "{} owes {} cents in fines; pay below {} to borrow again".format(
                    member_id, balance, CHECKOUT_BLOCK_THRESHOLD_CENTS
                )
            )

    # -- loans -----------------------------------------------------------

    def get_loan(self, loan_id: int) -> Loan:
        try:
            return self._loans[loan_id]
        except KeyError:
            raise UnknownLoanError(loan_id) from None

    def active_loans_for(self, member_id: str) -> List[Loan]:
        return [
            loan
            for loan in self._loans.values()
            if loan.member_id == member_id and loan.is_active
        ]

    def checkout(self, member_id: str, isbn: str, on: Optional[date] = None) -> Loan:
        if on is None:
            on = date.today()
        member = self.get_member(member_id)
        self._require_clear_balance(member_id)
        policy = self._policies.policy_for(member)

        if len(self.active_loans_for(member_id)) >= policy["max_active_loans"]:
            raise LoanLimitExceededError(
                "{} already has {} active loans".format(
                    member_id, policy["max_active_loans"]
                )
            )

        self._catalog.checkout_copy(isbn)
        loan = Loan(
            loan_id=self._next_loan_id,
            isbn=isbn,
            member_id=member_id,
            checked_out_on=on,
            due_on=on + timedelta(days=policy["loan_days"]),
            daily_fine_cents=policy["daily_fine_cents"],
            max_fine_cents=policy["max_fine_cents"],
            grace_days=policy["grace_days"],
        )
        self._next_loan_id += 1
        self._loans[loan.loan_id] = loan
        return loan

    def return_book(self, loan_id: int, on: Optional[date] = None) -> int:
        """Close out a loan and return the fine owed, in cents."""
        if on is None:
            on = date.today()
        loan = self.get_loan(loan_id)
        if not loan.is_active:
            raise AlreadyReturnedError(loan_id)

        loan.returned_on = on
        self._catalog.return_copy(loan.isbn)
        fine = calculate_fine_cents(
            loan.due_on,
            on,
            loan.daily_fine_cents,
            loan.max_fine_cents,
            loan.grace_days,
        )
        if fine:
            self._balances[loan.member_id] = (
                self._balances.get(loan.member_id, 0) + fine
            )
        return fine

    def renew(self, loan_id: int, on: Optional[date] = None) -> Loan:
        """Extend a loan by one loan period, measured from its due date."""
        if on is None:
            on = date.today()
        loan = self.get_loan(loan_id)
        if not loan.is_active:
            raise AlreadyReturnedError(loan_id)
        if on > loan.due_on:
            raise RenewalNotAllowedError(
                "loan {} is overdue and cannot be renewed".format(loan_id)
            )

        member = self.get_member(loan.member_id)
        self._require_clear_balance(loan.member_id)
        policy = self._policies.policy_for(member)
        if loan.renewals >= policy["renewal_limit"]:
            raise RenewalNotAllowedError(
                "loan {} has reached its renewal limit".format(loan_id)
            )

        loan.due_on = loan.due_on + timedelta(days=policy["loan_days"])
        loan.renewals += 1
        return loan
