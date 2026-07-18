# Learnings Log

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
