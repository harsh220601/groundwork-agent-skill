"""A short end-to-end walkthrough of a morning at the circulation desk."""

from datetime import date, timedelta

from libtrack.catalog import Catalog
from libtrack.loans import LoanService
from libtrack.models import Book, Member


def dollars(cents: int) -> str:
    return "${:,.2f}".format(cents / 100)


def main() -> None:
    today = date.today()

    catalog = Catalog()
    catalog.add_book(Book("9780262046305", "Introduction to Algorithms", "Cormen et al.", copies_total=3))
    catalog.add_book(Book("9781491946008", "Fluent Python", "Luciano Ramalho", copies_total=1))
    catalog.add_book(Book("9780134685991", "Effective Java", "Joshua Bloch", copies_total=2))

    service = LoanService(catalog)
    service.register_member(Member("M-100", "Dr. Elena Chen", category="faculty"))
    service.register_member(Member("M-101", "Priya Raman"))
    service.register_member(Member("M-102", "Sam Okafor", category="student"))

    print("Checkouts on {}".format(today.isoformat()))
    print("-" * 68)
    morning_queue = [
        ("M-100", "9780262046305"),
        ("M-101", "9781491946008"),
        ("M-102", "9780134685991"),
    ]
    loans = []
    for member_id, isbn in morning_queue:
        loan = service.checkout(member_id, isbn, on=today)
        member = service.get_member(member_id)
        book = catalog.get_book(isbn)
        days = (loan.due_on - today).days
        print(
            "{:<18} ({:<8}) {:<28} due {} ({} days)".format(
                member.name,
                member.category,
                book.title[:28],
                loan.due_on.isoformat(),
                days,
            )
        )
        loans.append(loan)

    print()
    print("Late return")
    print("-" * 68)
    loan = loans[1]  # Priya's copy of Fluent Python
    returned_on = loan.due_on + timedelta(days=30)
    fine = service.return_book(loan.loan_id, on=returned_on)
    book = catalog.get_book(loan.isbn)
    print(
        "{} returned on {} (30 days past due), fine owed: {}".format(
            book.title, returned_on.isoformat(), dollars(fine)
        )
    )


if __name__ == "__main__":
    main()
