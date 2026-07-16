# Project Map — LibTrack

Updated: 2026-07-16 | Verified against: `python3 -m unittest discover -s tests -v` → 47 passing

## What this is

LibTrack is a library circulation system for a single branch. It manages a catalog of titles, 
member registration, and desk operations: checkouts, returns, renewals, and late fines. Each 
member category (regular/student/faculty) has distinct lending terms via a policy engine.

## Intended behavior

- **Checkouts**: Member gets due date according to their category — faculty (42 days), student (28 days), regular (21 days)
- **Fines**: Charged at category-specific daily rate ($0.25/day for regular/student, $0.00 for faculty) with 2-day grace window
- **Policy isolation**: Category resolution never corrupts the base policy; each checkout gets its own independent policy copy

## Commands (run from project root)

- Test: `python3 -m unittest discover -s tests -v` → 47 passing, OK
- Run demo: `python3 demo.py` → walks through morning checkouts and a late return with fine calculation

## Architecture at a glance

**Policy Engine** (policies.py) resolves the effective lending terms for each member category by
copying the branch-wide defaults and merging category-specific overrides. **LoanService** (loans.py)
uses this policy to calculate due dates at checkout and fines at return time. **Catalog** (catalog.py)
tracks copy availability.

## Where things live (key files only)

- `libtrack/policies.py` — PolicyEngine: policy resolution for member categories
- `libtrack/loans.py` — LoanService: checkout, return, renewal, fine calculation; CirculationError exceptions
- `libtrack/models.py` — Data types: Book, Member, Loan
- `libtrack/catalog.py` — Catalog: title and copy inventory
- `demo.py` — End-to-end walkthrough with three member categories
- `tests/` — Unit tests organized by module

## Invariants and gotchas

- **Policy isolation required**: PolicyEngine.policy_for() must make a dict copy of self._base before updating with overrides. Mutating the shared dict causes category settings to leak into subsequent checkouts (see LEARNINGS).
- Fine terms are snapshotted onto the Loan record at checkout time; later policy changes do not retroactively affect what an existing loan owes.
- Grace window is 2 days: returns within the grace period owe nothing; fines accrue for every day after.
- Members owing $5.00 or more cannot checkout or renew.

## Decisions

- 2026-07-16: Fixed policy aliasing bug (PolicyEngine.policy_for) by copying base policy before override merge
