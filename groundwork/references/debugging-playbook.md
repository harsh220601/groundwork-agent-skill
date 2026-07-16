# Debugging Playbook

## Contents
- The debugging loop
- Phase 1: Reproduce
- Phase 2: Isolate
- Phase 3: Root-cause
- Phase 4: Fix and prove
- Repairing a broken build / red CI (layered failures)
- Symptom → first suspect table
- Stuck protocol
- Right vs wrong examples

## The debugging loop

Reproduce → Isolate → Root-cause → Red test → Fix → Prove. Never reorder: a fix written
before reproduction is a guess wearing a fix's clothes.

Before anything else: check LEARNINGS.md for this symptom. A log match accelerates hypothesis
selection — it never replaces proof. On a match: still reproduce the symptom (Phase 1), apply
the recorded fix as your leading hypothesis, and require the same red-before-green evidence as
any fix (Phase 4). If the symptom doesn't reproduce, or the recorded fix doesn't make your
reproduction pass, the entry may be wrong: mark it DISPUTED in the log with your evidence and
re-derive with the full playbook. The log is testimony from a past session, not ground truth.

## Phase 1: Reproduce

1. Run the failing thing FIRST — the app, the test, the command from the bug report. The error
   output is your primary evidence; code reading comes second.
2. Reproduce the exact reported symptom before forming any theory. If you cannot reproduce it,
   say so and gather more information — do not fix what you cannot see.
3. Capture the reproduction as a runnable command or script. You will re-run it after the fix;
   it is your before/after proof.
4. Note what the reproduction tells you beyond the report. Example from a real hunt: a member
   got wrong loan terms only AFTER a faculty checkout — the reproduction revealed
   order-dependence the user never mentioned, which pointed straight at shared mutable state.

## Phase 2: Isolate

1. Read the test suite's verdict: if tests are green while the bug is live, the bug sits in a
   coverage gap — green tests certify only what they exercise, nothing more.
2. Locate the owning module before opening files: README/map layout tables, directory names,
   then search for the domain terms from the symptom.
3. Shrink the world: find the smallest input, sequence, or state that still shows the symptom.
   Every element you remove is a hypothesis eliminated for free.

## Phase 3: Root-cause

1. Write down 2-3 candidate hypotheses BEFORE reading deeply. Cheap discipline: it stops the
   first plausible-looking line of code from hijacking your judgment.
2. Test hypotheses cheapest-first, and prefer probes that can only succeed one way: a 5-line
   script that prints the suspect state settles more than an hour of reading.
3. A hypothesis is confirmed when it (a) explains EVERY observation, including the weird ones,
   and (b) predicts something you haven't observed yet — and the prediction checks out.
   Example: "shared dict pollution" explained why students looked half-right (their own
   override masked one field) and predicted students silently inherited zero fines — probing
   confirmed the prediction. That's confirmation; consistency alone is not.
4. Kill hypotheses explicitly. Say "H2 is dead because <evidence>". A hypothesis that quietly
   survives returns later as a wrong fix.
5. State the root cause in one sentence, with the evidence, BEFORE writing the fix. If you
   cannot write that sentence, you are still in phase 3.

## Phase 4: Fix and prove

1. Write a regression test that captures the bug, run it, and WATCH IT FAIL — for the RIGHT
   reason: quote the red output and confirm it is an assertion mismatch matching the reported
   symptom, not an import/collection/typo error. The red must bind to the FINAL test text: if
   you edit the test after the fix, re-run the edited text against the pre-fix code
   (revert/stash/backup copy) and watch it fail again. A test that never failed, or failed for
   an unrelated reason, proves nothing about your fix.
2. Apply the smallest fix that addresses the cause. Resist drive-by refactors — they widen the
   diff and muddy the proof.
3. Run: the regression test (now green), the full suite (nothing else broke), and the original
   reproduction from Phase 1 (the user's actual scenario, not just your abstraction of it).
4. Paste real output for all three. Then write the LEARNINGS.md entry:
   symptom → root cause → fix → prevention.

## Repairing a broken build / red CI (layered failures)

Broken states are onions. The visible error usually hides more behind it.

1. Run the failing command; read the WHOLE output, not just the last line.
2. An import/collection/compile error doesn't fail one test — it prevents whole modules from
   loading. Count what ran: "9 tests ran" in a repo with 3 test files means failures are being
   masked. Treat the run count as evidence.
3. Fix exactly ONE root cause, then RE-RUN the full command. Never batch fixes against a masked
   failure list — half of them will be guesses about failures you haven't actually seen yet.
4. Repeat until green, then run the real entry point (CLI, server, demo) once — "the suite
   passes" and "the app works" are different claims; the ticket usually means the second.
5. Before fixing any mismatch (wrong name, wrong signature, wrong behavior), establish the
   intended direction — search EVERY reference/call site first:
   - Majority usage + tests define the intent; the stale minority gets migrated forward.
   - Never "fix" by recreating what a refactor deliberately removed, and never rename a
     function back to match its one stale caller: check which side the other callers are on.
   - Rank intent sources: user's words > tests > README/docs > code comments > your instinct.
6. Never edit a test's expectation to match broken output. If you believe the TEST is wrong,
   that's a claim needing its own evidence (README, other tests, docs) — surface it, don't
   silently rewrite it.

## Symptom → first suspect table

| Symptom | Check first |
|---|---|
| Correct, then wrong after certain earlier operations (order-dependent) | Shared mutable state: aliased dicts/lists, mutable default args, module-level caches, singletons |
| Off-by-one day/index/boundary | Inclusive vs exclusive ranges; `<` vs `<=`; boundary values at exactly the limit |
| Works locally, fails in CI (or vice versa) | Environment deltas: versions, env vars, cwd, timezone/locale, missing files |
| Intermittent/flaky | Time, randomness, ordering assumptions (dict/set/parallelism), external state |
| Wrong aggregate/total | Duplicates, filter conditions, unit mismatch (cents vs dollars), int division |
| ImportError/ModuleNotFoundError after "refactor" | Half-finished rename: grep old name repo-wide; check which callers migrated |
| Everything fails at once | One shared cause upstream (fixture, config, conftest/setup) — not N separate bugs |

## Stuck protocol

- Two failed fix attempts on the same issue → stop. Re-run the reproduction, re-read the raw
  error and the code with fresh eyes; write down what you now know that you didn't at attempt
  one. Your model is wrong somewhere — locate the wrong belief before touching code again.
- Third occurrence of the same error → change instruments: add print/log lines at the suspect
  boundary, bisect the input, or bisect history if version control exists.
- Still stuck after that → report honestly: what you observed (verbatim), what you ruled out
  (with evidence), your best remaining hypothesis (tagged ASSUMED), and what you'd try next.
  An honest "stuck, here's the map of the territory" beats a fake fix every time.

## Right vs wrong examples

- WRONG: The suite is green, so the reported bug must be user error.
  RIGHT: The suite is green AND the demo reproduces the bug — so the suite has a gap where the
  bug lives. Both facts are evidence.
- WRONG: "I see the problem" after reading one file → edit → "should be fixed."
  RIGHT: Probe confirms the hypothesis → regression test fails → one-line fix → regression
  passes, suite passes, original scenario re-run and observed correct.
- WRONG: ImportError for `pkg.utils` → create `pkg/utils.py` to satisfy the import.
  RIGHT: Grep shows production migrated to `pkg.timeutil`; only a test helper lags. Migrate the
  laggard; re-run; expect the true failure list to grow now that hidden tests load.
