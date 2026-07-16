# LibTrack

LibTrack is a small circulation system for a single library branch. It keeps
a catalog of titles (with per-title copy counts), registers members, and
handles the day-to-day desk operations: checkouts, returns, renewals, and
late fines.

## Lending policies

Members belong to one of three categories. Every category starts from the
branch-wide defaults; students and faculty get a few adjusted terms.

| Category | Loan period | Max active loans | Renewals | Daily fine | Fine cap |
|----------|-------------|------------------|----------|------------|----------|
| regular  | 21 days     | 5                | 2        | $0.25      | $10.00   |
| student  | 28 days     | 8                | 2        | $0.25      | $10.00   |
| faculty  | 42 days     | 5                | 4        | none       | none     |

Fine rules:

- Every category has a 2-day grace window after the due date. A book
  returned within the grace window owes nothing.
- Once past the grace window, the fine covers every day past the due date
  (grace days included), at the member's daily rate, capped at the fine cap.
- Fine terms are snapshotted onto the loan at checkout, so a later policy
  change never changes what an existing borrower owes.

Account rules:

- Fines post to the member's account balance at return time.
- Payments (`record_payment`) must be positive and cannot exceed the balance.
- A member owing $5.00 or more cannot check out or renew until the balance
  is paid below $5.00.

Renewal rules:

- A renewal extends the due date by one loan period, measured from the
  current due date (not from the day the renewal is requested).
- Overdue loans cannot be renewed.
- Each loan can be renewed up to the category's renewal limit.

## Layout

```
libtrack/
  models.py     data types: Book, Member, Loan
  catalog.py    titles and copy availability
  policies.py   per-category lending policy resolution
  loans.py      checkouts, returns, renewals, fines
demo.py         scripted walkthrough of a morning at the desk
tests/          unit tests
```

## Running the demo

From the project root:

```
python3 demo.py
```

## Running the tests

From the project root:

```
python3 -m unittest discover -s tests -v
```

Requires Python 3.9+. No third-party dependencies.
