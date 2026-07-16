# LibTrack Project Map

## Project Purpose
LibTrack is a library circulation system managing member registrations, book checkouts, returns, renewals, and late fines across three membership categories (regular, student, faculty).

## Architecture

### Core Modules

**libtrack/models.py**
- `Book`: Represents a catalog title with ISBN, title, author, and copy count
- `Member`: Represents a registered library member with ID, name, and category (regular/student/faculty)
- `Loan`: Represents a checked-out copy with loan period, fine terms (captured at checkout time for policy immutability)

**libtrack/policies.py**
- `PolicyEngine`: Resolves effective lending policy for a member
- `DEFAULT_POLICY`: Branch-wide defaults (21-day loan, $0.25/day fine, 2-day grace, $10 fine cap)
- `CATEGORY_OVERRIDES`: Category-specific policy adjustments (student: 28 days/8 loans; faculty: 42 days/4 renewals/no fines)
- **Critical logic**: `policy_for(member)` must create a fresh dict copy on each call to prevent policy aliasing across sequential member transactions

**libtrack/catalog.py**
- `Catalog`: Manages book inventory, ISBN lookup, and copy availability tracking
- Raises on duplicate ISBN or unknown ISBN

**libtrack/loans.py**
- `LoanService`: Orchestrates circulation operations
- `calculate_fine_cents()`: Computes overdue fines (grace window, daily rate, cap)
- Core methods:
  - `checkout()`: Creates loan, captures fine terms from policy, enforces limits
  - `return_book()`: Calculates fine, updates member balance, closes loan
  - `renew()`: Extends due date by one loan period, enforces renewal limits

### Circulation Rules
- Fines: 2-day grace window, then daily rate until cap (faculty exempt)
- Fine terms snapshot at checkout time (policy immutable for loan lifespan)
- Loans unpaid at $5+ balance cannot checkout/renew
- Active loan limits enforced per category
- Renewals: limited per category, extend from current due date (not checkout date)

## Entry Points
- **demo.py**: Scripted walkthrough showing faculty, regular, and student checkouts + late return
- **tests/**: Unit tests covering all modules (46 tests, all passing)

## Known Issues / Learnings
See LEARNINGS.md

## Test Coverage
- test_accounts.py: Balance tracking, payment validation, checkout blocking
- test_catalog.py: Inventory, ISBN registration, availability
- test_loans.py: Checkouts, returns, renewals, fine calculation, policy application
- test_policies.py: Policy resolution for each category, aliasing prevention

All tests verify real behavior (no mocking of core logic).
