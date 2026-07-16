# Trace 2 — Build: member accounts feature (fines → balance → borrowing block)

Task: add an end-to-end feature to the just-repaired LibTrack codebase: fines accrue to a
member balance, payments reduce it, balance ≥ $5.00 blocks checkouts and renewals.
Brownfield on purpose — building into existing code exposes more method than greenfield.

## What I looked at first, and why

1. Read `loans.py` and `models.py` IN FULL before designing — the feature had to hang off
   `return_book`'s fine computation and `checkout`/`renew`'s guard structure. Design decisions
   (where the balance lives, where the guard goes) came from the code as it is, not from an
   imagined architecture.
2. Wrote the success criteria BEFORE any implementation, as a numbered list: fine posts to
   balance; balance/payment APIs with validation; ≥500¢ blocks checkout AND renewal with
   exact-threshold semantics (500 blocks, 499 allows); paying down re-enables; the 36 existing
   tests stay green; README updated.

## Evidence gathered before forming opinions

- `return_book` computes the fine but discards it after returning — so the posting point was
  unambiguous. `checkout` already had a guard sequence (member → policy → loan limit), which
  fixed where the new guard belongs: after member resolution, BEFORE `catalog.checkout_copy`,
  so a blocked checkout can never leak a claimed copy.

## Hypotheses / design decisions and how alternatives died

- Balance on the `Member` dataclass vs. a `_balances` dict in `LoanService`: chose the service
  dict — `Member` is a pure data type everywhere else, and mutating shared dataclass instances
  is exactly the bug class I had just fixed in this repo. The repo's own history informed the
  design.
- Threshold as a named constant with a justification comment (why $5: half the fine cap; one
  late return can't lock anyone out) — not a magic number.

## Verification at every step

1. Wrote `tests/test_accounts.py` (13 tests incl. boundary 500/499, overpay, zero-payment,
   unknown member, re-enable-after-payment, renewal block) BEFORE implementing.
2. Ran it: FAILED at import (API doesn't exist) — red state confirmed, so a later green means
   something.
3. Implemented (2 exceptions, constant, 3 methods, 3 call-site edits). Ran full suite:
   49/49 pass (36 old + 13 new).
4. Hostile review of my own diff before calling it done: verified guard ordering (no copy leak
   on block), faculty unaffected (0 fines never post), the renewal test genuinely reaches the
   balance check (loan not overdue, since the overdue check precedes it), and no existing test
   or assertion was modified.
5. Updated README so docs match behavior — the "living project system" habit.

## Moments I was tempted to assume, and what I did instead

- Tempted to put the balance check after the loan-limit check in `checkout` (append-style "add
  new code at the end of the guards"). Checked the failure ordering implications and put it
  right after member resolution instead: a blocked member should hear about fines, not about
  loan limits.
- Tempted to skip the README edit as "not code." It was in my own pre-stated criteria; skipping
  it would be quietly shrinking the definition of done.

## Where a weaker model would have hallucinated or faked success

1. Written the implementation first, then tests shaped to whatever the implementation does —
   tests that can't fail encode bugs as spec.
2. Skipped exact-threshold tests; boundary semantics (≥ vs >) would then be whatever the code
   happened to say.
3. Placed the guard after `catalog.checkout_copy`, silently corrupting copy counts on every
   blocked checkout — invisible to happy-path tests.
4. Claimed "all tests pass" from partial runs (only the new file), missing breakage in the
   other 36.

## Method distilled

- Read the code you're extending in full before designing; let existing structure and even the
  repo's bug history drive decisions.
- Success criteria first, as a checkable list; tests written from the criteria, run RED before
  implementation.
- Guard placement / ordering is design, not detail — reason about what half-done state a
  failure leaves behind.
- Done includes docs: behavior change ⇒ README/map update in the same session.
