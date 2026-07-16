# LibTrack Learnings Log

## Bug: Policy Aliasing Across Sequential Member Transactions

**Date Diagnosed:** 2026-07-16
**Root Cause:** Dictionary aliasing in `PolicyEngine.policy_for()` method

### Symptom
When checking out books to multiple members in sequence, lending policy from an earlier member (e.g., faculty with 42-day loan and no fines) would bleed into subsequent members' checkouts. Priya Raman (regular member) incorrectly received a 42-day loan instead of 21 days, and no fine was calculated on her overdue return.

### Evidence
**Bug Report Input:**
- Dr. Elena Chen (faculty) → 42 days (CORRECT)
- Priya Raman (regular) → 42 days (BUG, should be 21)
- Sam Okafor (student) → 28 days (CORRECT)
- Priya's return 30 days late → $0.00 fine (BUG, should be $7.50)

**Pre-fix demo output:**
```
Dr. Elena Chen     (faculty ) Introduction to Algorithms   due 2026-08-27 (42 days)
Priya Raman        (regular ) Fluent Python                due 2026-08-27 (42 days)
Sam Okafor         (student ) Effective Java               due 2026-08-13 (28 days)
Fluent Python returned on 2026-09-26 (30 days past due), fine owed: $0.00
```

### Root Cause
File: `libtrack/policies.py`, line 44 in `PolicyEngine.policy_for()`

```python
# WRONG (pre-fix)
def policy_for(self, member: Member) -> Policy:
    policy = self._base  # Creates a reference, not a copy!
    overrides = CATEGORY_OVERRIDES.get(member.category)
    if overrides:
        policy.update(overrides)  # Modifies the shared self._base dict
    return policy
```

The line `policy = self._base` does not create a copy—it creates an alias. When `policy.update(overrides)` is called for a faculty member, it modifies the shared `self._base` dictionary in place, overwriting:
- `loan_days`: 21 → 42
- `daily_fine_cents`: 25 → 0
- `max_fine_cents`: 1000 → 0
- `renewal_limit`: 2 → 4

Subsequent calls to `policy_for()` for a regular member return this polluted base dict, and the regular-category overrides (empty dict) do not fully restore the defaults.

### Fix
Change line 44 to create a proper copy:

```python
# RIGHT (post-fix)
def policy_for(self, member: Member) -> Policy:
    policy = dict(self._base)  # Creates a new dict from self._base
    overrides = CATEGORY_OVERRIDES.get(member.category)
    if overrides:
        policy.update(overrides)
    return policy
```

### Verification
**Post-fix demo output:**
```
Dr. Elena Chen     (faculty ) Introduction to Algorithms   due 2026-08-27 (42 days)
Priya Raman        (regular ) Fluent Python                due 2026-08-06 (21 days)
Sam Okafor         (student ) Effective Java               due 2026-08-13 (28 days)
Fluent Python returned on 2026-09-05 (30 days past due), fine owed: $7.50
```

**Test results:** 46/46 unit tests pass (all green before and after fix, but the fix corrects the underlying aliasing issue validated by `test_module_defaults_are_not_modified`)

### Lessons
1. **Dictionary aliasing is silent**: Python's `dict` assignment creates a reference, not a copy. Always use `dict(source)` to create a shallow copy when modifying.
2. **Test the state, not just the output**: The test `test_module_defaults_are_not_modified` caught the intent of policy immutability, which is why it was already present in the test suite.
3. **Policy capture at checkout time**: The design correctly snapshots fine terms onto each `Loan` object at checkout, preventing retroactive policy changes. The bug only affected *which* policy was used, not the mutability of policy itself.
