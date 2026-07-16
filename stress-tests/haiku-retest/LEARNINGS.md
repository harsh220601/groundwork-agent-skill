# Learnings Log — LibTrack

## 2026-07-16 — Category policy leaked into later checkouts

- **Symptom**: Regular member (Priya Raman) got 42-day loan + $0.00 fine instead of 21-day loan + $7.50 fine; only happened when a faculty checkout occurred first; all 46 tests passed.

- **Root cause**: PolicyEngine.policy_for() at line 44 did `policy = self._base` (aliasing the internal dict) then updated it with category overrides. Faculty resolution permanently mutated self._base from {loan_days: 21, daily_fine_cents: 25, ...} to {loan_days: 42, daily_fine_cents: 0, ...}. Subsequent regular-member checkout got the corrupted base.

- **Fix**: Changed line 44 in libtrack/policies.py from `policy = self._base` to `policy = dict(self._base)` to make an independent copy before merging overrides.

- **Prevention**: Added regression test `test_policy_isolation_faculty_then_regular` in tests/test_policies.py that would fail with the bug and pass with the fix; captures the order-dependent failure pattern.

- **Keywords**: aliasing, shared mutable state, order-dependent checkout failure, policy_for, wrong due date, zero fine
