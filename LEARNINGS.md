# Learnings Log

## 2026-07-18 — Single-file deployment surfaces cross-layer contradictions
- Symptom: a cold-read audit of the combined single-file build (a fresh agent given ONLY the
  file) found conflicting orders the multi-file layout had masked: trivial-task scaling by
  diff size vs the no-runtime-change trivial tier; "create no files" for answer-type tasks
  vs step-zero map creation inside a repo; the characterization-update move vs the
  mechanical count gate; the Likely marker having no claim-ledger counterpart.
- Root cause: rules written in separate files were each locally coherent but were never
  checked pairwise against each other.
- Fix: four source edits — SKILL.md Loop scaling + answer-type file rule, a count-gate
  exception in self-testing-loop.md, and the bridge mapping Likely → ledger-ASSUMED with
  confirmation path in standing-orders.md.
- Prevention: scripts/build_master.py builds and verifies the single-file edition; re-run a
  cold-read audit (agent holding only the built file) after any rule change.
- Keywords: contradiction, cross-file, trivial tier, count gate, characterization, Likely ledger

## 2026-07-18 — Introspective triggers fail exactly when they are needed
- Symptom: adversarial review confirmed standing-orders area 8(b)'s trigger ("recall is a
  familiar-shaped blur rather than distinct memory") is untestable at execution time — and
  confabulated recall feels distinct precisely in the cases the rule exists to catch. All 5
  behavioral trap sims passed, yet the trigger was unexecutable as written.
- Root cause: the rule encoded an internal state instead of an observable artifact.
- Fix: replaced with the two-detail test in both standing-orders forms (state two specifics
  about the named artifact beyond what the answer needs; fewer → refuse), plus an
  environment-pull carve-out (if the artifact is in a file/source/doc you can read, read it
  and answer Certain).
- Prevention: scripts/validate_standing_orders.py enforces document structure; the
  executability critique lens is recorded in test-report.md round 3 for future revisions.
- Keywords: introspective trigger, familiar-shaped blur, confabulation, detail test, area 8

## 2026-07-18 — Cost-comparison gates are unexecutable rules
- Symptom: standing-orders area 1's ask-vs-proceed gate compared "cost of a wrong guess"
  with "cost of a clarifying round-trip" — two unmeasurable quantities with no tiebreak; two
  executors facing the same request could reach opposite conclusions.
- Root cause: a judgment-call comparison where an enumerable trigger was needed.
- Fix: condition (b) rewritten to observable terms — a plausible reading commits an
  irreversible/externally visible action (paste, send, sign, execute, pay) or makes the
  deliverable unusable under the other reading — with proceed-and-state-reading as the
  explicit default when undecided.
- Prevention: same validator; critique lens recorded in test-report.md round 3.
- Keywords: clarifying question, ask vs proceed, judgment call, unmeasurable, area 1
