# Learnings Log Specification (LEARNINGS.md)

## Contents
- Purpose and the prime rule
- Entry schema
- When to write an entry
- Check-the-log-first discipline
- Maintenance

## Purpose and the prime rule

`LEARNINGS.md` is a single markdown file at the project root recording every root-caused bug
and hard-won discovery. The prime rule: **a problem in the log is never re-derived from
scratch — and a logged fix still gets proven like any other fix.** The log points you at the
root cause fast; reproduction before and re-run after remain mandatory, because the log is
testimony from a past session (possibly a careless one), not ground truth. The log is the
mechanism that makes session N+1 smarter than session N.

## Entry schema

Newest entries at the top. One entry per root-caused problem:

```markdown
## <date> — <one-line title naming the failure mode>
- Symptom: <what was observed, concretely — the thing a future search will match>
- Root cause: <the actual cause, one or two sentences>
- Fix: <what changed, with file/function names>
- Prevention: <the regression test added / the invariant now in the map / the habit>
- Keywords: <search terms a future agent might use: error text fragments, module names>
```

Real example:

```markdown
## 2026-07-16 — Category policy leaked into later checkouts
- Symptom: regular member got 42-day loan + $0 fine, but only when a faculty checkout
  happened first; tests all green.
- Root cause: PolicyEngine.policy_for aliased self._base and mutated it with
  category overrides — faculty resolution permanently polluted the shared defaults.
- Fix: copy before merge (policy = dict(self._base)) in libtrack/policies.py.
- Prevention: PolicyEngineIsolationTest (3 tests: cross-category isolation, base immutability);
  invariant added to PROJECT-MAP.md.
- Keywords: aliasing, shared mutable state, order-dependent, policy_for, wrong due date
```

## When to write an entry

Write one, in the same session as the discovery (memory of root causes decays by next session):
- every bug you root-caused (however small — small bugs recur too);
- every trap that cost you real time (a docs-vs-runtime mismatch, a version constraint, a
  test that can't run in isolation, a command that must run from a specific directory);
- every wrong assumption you caught yourself making about this project, if the next agent
  would plausibly make it too.

Skip entries for: things fully expressed by a test alone with no story ("typo in string"),
generic language facts, anything already in the log (update the existing entry instead).

## Check-the-log-first discipline

BEFORE starting any debugging work: open LEARNINGS.md and scan titles + keywords against your
symptom. Three outcomes:
1. Exact match → reproduce the symptom first, then apply the recorded fix as your leading
   hypothesis and prove it (reproduction red before, green after — same bar as any fix). Note
   the recurrence in the entry: a recurrence means the prevention failed — strengthen it. If
   the recorded fix does NOT make your reproduction pass, or contradicts what you observe,
   mark the entry "DISPUTED: <evidence>" and re-derive with the playbook.
2. Related match → read the entry; it may name the module or trap involved.
3. No match → proceed with the debugging playbook; your entry lands here afterward.
This lookup costs seconds and is mandatory ahead of any investigation — re-deriving a logged
root cause is the most avoidable waste in multi-session work.

## Maintenance

- Keep entries tight: 5-8 lines. The story belongs in the entry only insofar as it helps a
  future match.
- If the log grows past ~150 entries, group by area with `##` headers or split into
  LEARNINGS-<area>.md files linked from the top of the main log — keep titles+keywords
  greppable in one place.
- Never delete an entry because the code moved on; mark it "(historical — code replaced
  <date>)" instead. Old failure modes return with old patterns.
- An entry shown to be WRONG (misdiagnosed cause, fix that doesn't fix) is different from
  historical: correct it in place, keeping a one-line "(previously claimed X — disproven by
  <evidence>, <date>)" so the wrong version can't silently come back.
