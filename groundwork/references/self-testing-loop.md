# Self-Testing Loop

This file expands Loop steps from SKILL.md and uses the SAME numbering: step 2 = Define done,
step 4 = Build, step 5 = Verify, step 6 = Hostile review, step 7 = Record.

## Contents
- Step 2: Define done before building
- Step 4: Build in checked increments
- Step 5: Verify — run your own work
- Step 6: Hostile review checklist
- Exit criteria — the only two exits
- Failure discipline
- Flaky checks and pre-existing failures
- Effort scaling
- Reporting with evidence

## Step 2: Define done before building

Before writing any code, write down:
1. The exact commands that will prove success, and what their output/exit code must be. The
   list MUST include the user's reported scenario or the real entry point exercising the
   requested behavior, and at least one check that would FAIL if the requested change were
   absent — name which one. Criteria a reverted change would still pass are invalid.
2. The edge cases that must hold — boundaries at exact limits (the 500th cent, the 65535th
   port), empty inputs, the unhappy paths.
3. What must NOT change (no new failures vs the step-zero baseline, API compatibility,
   output format).

The criteria list is append-only once written: weakening or removing a criterion requires the
same evidence bar as changing a failing check (docs, tests, user intent) and a "CRITERIA
CHANGED:" line in the final report.

If nothing checkable exists (no tests, no runnable entry), creating a check is the first
deliverable: a smoke script that runs the real code path and asserts on its output. Label it a
CHARACTERIZATION check — it records behavior as found (bugs included) and detects change, not
correctness; note that in the map. When you later change behavior deliberately and verifiably,
updating the characterization expectation to the new verified output is a defined move — state
the before/after in the report.

Write tests FROM the criteria, BEFORE the implementation, and run them: they must fail (red)
for the RIGHT reason — an assertion mismatch about the missing behavior, not an import error or
typo. Quote the red output. Tests written after the code tend to encode whatever the code does
— bugs become spec.

## Step 4: Build in checked increments

1. For any non-trivial change, describe the change in prose first — which files, which
   functions, what moves where — then apply it as small, uniquely-anchored edits. Separating
   "decide the change" from "type the change" prevents both from being done badly at once.
2. After EVERY edit, run the cheapest check that can catch a break: syntax check, import,
   compile, lint. Fix before the next edit — an error built upon compounds.
3. Guard placement and failure ordering are design decisions: reason about what state a
   failure leaves behind (e.g., validate BEFORE consuming a resource, so a rejected operation
   can't leak side effects).
4. Write the new failing test before the production change and do not edit the test afterward;
   if you must edit it, re-run it against the pre-change code (revert/stash/backup) and watch
   the FINAL text fail. Red-before-green binds to the final test text, not an early draft.

## Step 5: Verify — run your own work

1. Re-run the full step-2 check list AFTER your final edit — not a subset, not only the tests
   you just wrote, and not a green run from before the last change. Evidence predating an edit
   certifies a program that no longer exists.
2. Mechanical count gate: for any behavior change or bug fix, the number of tests/checks that
   ran must be GREATER than the baseline count. Unchanged count = the new check was never
   added = go back to step 4. One exception: a deliberate, verified behavior change recorded
   by updating a characterization expectation in place — name the updated check and show the
   before/after instead of growing the count.
3. Run the real entry point once with realistic input and READ its output. Tests certify
   units; the entry point certifies the task.
4. Record verbatim summary lines (pass/fail/skip counts, exit codes), not flattering excerpts.

## Step 6: Hostile review checklist

Switch roles: you are a skeptical reviewer seeing only the change (diff or before/after copies)
and the step-2 criteria. Work every box:
- [ ] Would every step-2 check pass even if the change were reverted? If yes, the criteria are
      invalid — rewrite them and redo step 5.
- [ ] Each new test detects its bug/feature: revert the change temporarily and run the named
      test — quote the red; restore and re-run green. (Mental simulation only if reversion is
      impossible, citing the earlier red run of the same unedited test text.)
- [ ] Boundary semantics tested at the exact boundary (=, one below, one above).
- [ ] No EXISTING test, fixture, or verifier config was weakened, deleted, skipped, or
      loosened. New tests for red-before-green are expected — list them by name.
- [ ] No anti-gaming signatures (see anti-hallucination-protocol.md) outside explicit user
      orders.
- [ ] Error paths leave clean state (nothing consumed/locked/half-written on the failure path).
- [ ] Docs/map updated if behavior or commands changed.
Enumerate EVERY finding and mark each one KEPT (fix + re-run step 5) or DISMISSED with a
one-line reason; dismissals go in the final report. Silence about a finding is non-compliance.
Keep scope: correctness findings get fixed; cosmetic ones get dismissed with a reason, not
silently chased into a rewrite. Where subagents exist, run this checklist in a fresh context
that has only the change + criteria.

## Exit criteria — the only two exits

1. **Demonstrated pass** — every step-2 check ran after the final edit and passed; no new
   failures vs baseline; no load-bearing ASSUMED left in the ledger.
2. **Honest blocker** — you cannot make it pass. This exit must be earned: either (a) at least
   two distinct root-cause attempts, documented with the evidence that killed each, or (b) a
   named external blocker (missing access, credentials, network, a user decision). Report what
   you tried, the current failure verbatim, your best remaining hypothesis (tagged), and what
   you'd try next.
"Mostly works", "should work", and "works on my end" are not exits — they are the space between
the two exits where fake success lives.

## Failure discipline

When a check fails:
- Root-cause it with the debugging playbook. The failing check is evidence, not an obstacle.
- Never delete a failing test, weaken its assertion, skip it, or edit its expectation to match
  broken output — unless the USER explicitly ordered it (then comply, state the lost coverage
  once, and record it), or you have independent evidence the check itself is wrong (docs,
  other tests, maintainer intent) — surface that evidence in the report alongside the change.
- Never bypass a failing gate with exit-code tricks or environment fudging.

## Flaky checks and pre-existing failures

- Pre-existing failures recorded in the step-zero baseline are not yours: "done" = your checks
  pass AND no NEW failures versus that baseline. Log pre-existing failures in LEARNINGS.md;
  fix them only if they block the task or are the task.
- A check that fails intermittently: characterize it — re-run 3 times with ZERO edits between
  runs. Divergent results = flaky; log it, exclude it from your pass/fail gate, and state the
  exclusion in your report. This diagnostic re-run is different from banned retry-until-green:
  characterization changes nothing and reports the flake; retry-until-green hides it and
  claims the lucky run as proof.

## Effort scaling

- Trivial tier — applies ONLY to changes with no runtime behavior change: comments, docs,
  string typos in messages, renames fully verified by compiler/tests. Any edit to executable
  logic, conditions, or data is standard tier regardless of size. In the trivial tier, Define
  done and Plan may be one line each, but the step-2 behavioral check still runs after the
  edit (for docs: build/render or link-check; for renames: the compiler/suite).
- Standard task: the full loop.
- Large/risky task (migrations, cross-cutting refactors): add a written plan with rollback
  notes, and verify in stages — after each stage, not only at the end.

## Reporting with evidence

End every task with this block (adapt labels, keep substance):

```
DONE: <what changed, one line>
PROOF: <exact step-2 command> → <verbatim summary line: counts + exit code>
       <entry-point command> → <key line(s) of real output>
       (all runs postdate the final edit; test count baseline <N> → now <M>)
NEW CHECKS: <tests/checks added, by name — each seen red before the fix> | none + why
REVIEW: <hostile-review findings: KEPT n / DISMISSED m with reasons> | clean
CRITERIA CHANGED: <changes to the done-list + evidence> | none
LEDGER: VERIFIED: <load-bearing facts, each with inline evidence>
        ASSUMED: <only genuinely uncheckable items + why> | none (after reconciliation scan)
        UNKNOWN: <what you couldn't determine + how you'd find out> | none
RECORDED: <map/log edits made>  ("none needed" is legal only if the change touched no
          non-test source, no commands, and no invariants — otherwise name the map sections
          you re-read and why they still hold)
```

If a reader could not reconstruct whether the task truly succeeded from your report alone, the
report is incomplete — regardless of how good the work was.
