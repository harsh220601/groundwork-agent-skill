# Trace 3 — Deep Research: Zod 4 (library I don't fully know)

Task: build a JSON config validator using Zod 4 idioms, on zod@4.4.3 (verified installed
version via `require('zod/package.json').version`), Node v25.9.0.
Done = a test script with 8 assertions passing + CLI exits 0/1 correctly. Defined BEFORE building.

## What I looked at first, and why

1. `npm install zod && node -e "...version"` — pin down the exact installed version before
   reading anything. Docs describe *a* version; my claims must be about *this* version.
2. Wrote an honest inventory of what I did NOT know before researching: the v4 error-customization
   param, the v4 error-formatting function names, `z.record` arity, `.default()` semantics,
   discriminated-union syntax. Writing the ignorance list first is the step that prevents
   "confidently writing Zod 3 code against Zod 4" — which is exactly what a weaker model does.

## Evidence gathered before forming opinions

- Fetched https://zod.dev/v4/changelog and https://zod.dev/error-formatting (official docs).
  Key deltas from what I "knew": `{ message }` → `{ error }`; `z.string().email()` →
  top-level `z.email()`; `.format()/.flatten()` → `z.treeifyError()/z.flattenError()` +
  `z.prettifyError()`; `.default()` now output-typed and short-circuiting (`.prefault()` = old
  behavior); `z.record` documented as two-arg; `.strict()` → `z.strictObject()`.
- Then ran a 7-probe script against the installed package BEFORE writing any real code —
  runtime is ground truth, docs are testimony.

## Hypotheses formed — and how the wrong ones died

- Hypothesis: "docs say z.record requires two args, so one-arg will throw." KILLED by probe:
  one-arg `z.record(z.string())` was ACCEPTED at runtime in 4.4.3. The two-arg requirement is a
  TypeScript-surface constraint, not a JS runtime one. Lesson: verify claims at the layer you
  will use them (JS runtime vs type-checker). I still used the two-arg form as canonical.
- Hypothesis (from Zod 3 memory): "error messages are set with { message }". Docs said `{ error }`;
  probe confirmed both string and callback forms work, and that the callback receives
  `issue.input` (probe printed 'Not a string!' / 'Required!').

## Verification at every step

- 7 runtime probes before authoring (all outputs captured in session transcript).
- `node test.mjs` → 8/8 checks passed, covering: defaults applied (enum/int/record), boundary
  values (65535 ok / 65536 rejected with my custom message), refine + custom error, error
  callback interpolation, discriminated-union per-variant fields (missing clientSecret/tokenUrl
  surfaced with correct paths), strictObject `unrecognized_keys`, prettifyError content,
  treeifyError nesting.
- CLI: invalid config → 5 issues printed with `→ at` paths, exit 1. Valid config → normalized
  output with defaults filled, exit 0. Both observed.

## Moments I was tempted to assume, and what I did instead

- I used `z.int()` top-level in the schema without having probed it (it "felt" like a v4
  addition). That was an ASSUMED claim riding on pattern-matching. It happened to be verified by
  the test run (schema construction would have thrown otherwise), but the honest process would
  have probed it first. Recorded as a near-miss: assumptions hidden inside "obviously fine" code
  are the ones that bite.
- Tempted to reuse Zod 3's `.flatten()` from memory for CLI output. Instead checked the
  error-formatting docs and used `z.prettifyError` — which didn't exist in my remembered API at all.

## Where a weaker model would have hallucinated or faked success here

1. Written Zod 3 code from memory (`{ message }`, `.format()`, `z.string().email()`), seen
   deprecation warnings or subtly wrong behavior, and shipped anyway.
2. Trusted the migration doc's "requires two arguments" and "fixed" working one-arg code — or
   argued from docs against observed runtime behavior instead of reconciling the two.
3. Skipped boundary tests (65535/65536) and claimed "port validation works" untested.
4. Claimed "tests pass" without running them, or run only the happy path and called it done.

## Method distilled from this exercise

- Pin the installed version first; it is the object of every claim.
- Write the ignorance inventory before researching; research the inventory, not vibes.
- Docs → runtime probes → only then real code. Probe each API you'll rely on, in isolation,
  cheaply. Reconcile every docs-vs-runtime discrepancy explicitly.
- Success criteria (test list + exit codes) written before the implementation.
