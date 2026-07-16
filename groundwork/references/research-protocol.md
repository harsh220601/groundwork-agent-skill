# Deep-Research Protocol (unfamiliar libraries, APIs, tools, domains)

## Contents
- When this applies
- The protocol
- Offline fallbacks
- Applying what you learned
- Right vs wrong examples

## When this applies

Any time you will state or rely on SPECIFIC names, signatures, flags, defaults, or behaviors
of a library, API, tool, or domain that you have not verified this session. That is the
trigger: specifics from memory. It does not cover language basics or universal tools you use
generically — it covers every identifier you'd have to look up to be sure of. Libraries change
under you; what you remember is some version, not this version.

## The protocol

1. **Pin the exact version first.** Read the lockfile/manifest, or query the package
   (`pip show X`, `npm ls X`, `tool --version`). Every claim you make will be about THIS
   version. Write it down. When nothing is installed or versioned (a hosted API, a protocol,
   a domain concept), pin the authoritative SOURCE instead — which docs/spec, retrieved when —
   and scope every claim to that source.
2. **Write the ignorance inventory.** List, explicitly, what you do not know and will need:
   API names, signatures, error handling, defaults, breaking changes since the version you
   remember. This list IS your research plan — without it you'll research vibes and stop at
   familiarity.
3. **Read authoritative sources against the inventory.** Official docs, changelog/migration
   guides (crucial when your memory is of an older major version), then the installed source
   itself. Note which pages you actually read — they're your citations.
4. **Probe before you build.** For each API you'll rely on, run a minimal snippet against the
   INSTALLED version proving it exists and behaves as documented. Docs are testimony; runtime
   is ground truth. Probes are tiny (1-5 lines each) and cheap; a failed probe before coding
   costs seconds, a failed assumption inside the feature costs the whole debugging loop.
5. **Reconcile discrepancies explicitly.** When docs and runtime disagree, record both facts
   and decide which layer the constraint lives at (type-checker vs runtime; deprecated vs
   removed). Real example: docs said `z.record()` "requires two arguments"; the installed
   4.4.3 accepted one at runtime — the requirement was TypeScript-level. Both facts true; a
   claim about "what the API requires" must name its layer.
6. **Then build**, using only probed APIs, with the self-testing loop. Anything used without a
   probe gets an ASSUMED tag until the test run verifies it.

## Offline fallbacks

No network? Local ground truth still exists — use it and say which you used:
- the installed package's own source and type stubs (read the actual function you'll call);
- `--help` / man pages for CLIs — never guess flags; probing `--help` is the anti-hallucination
  move for command syntax;
- bundled docs/README in the package directory;
- the runtime itself: import the thing and introspect (`dir()`, `typeof`, REPL probes).
When even that can't answer (e.g. hosted API behavior), tag the claim UNKNOWN and say what
you'd check with access — do not fall back to memory silently.

## Applying what you learned

- Prefer current idioms over deprecated ones even when both work — you researched precisely
  to avoid writing last-major-version code.
- Carry version facts into LEARNINGS.md when they cost you time ("v4 renamed `{message}` to
  `{error}`") and into PROJECT-MAP.md when they constrain the project ("requires Node ≥ 20").
- In your report, separate "the docs say" from "I observed" — they're different evidence
  grades, and readers need to know which they're getting.

## Right vs wrong examples

- WRONG: Writing `z.string().email()` from memory of v3 while v4 is installed, and shipping
  when it happens not to crash (deprecated ≠ correct).
  RIGHT: Changelog read → "v4 prefers top-level `z.email()`" → probe confirms it exists in
  4.4.3 → build with it.
- WRONG: "The library exposes a `parallel` option for this." (memory, no probe)
  RIGHT: "Probed the installed version: constructor accepts `{concurrency}` (probe output
  below); docs call it `concurrency` since v2. Using that."
- WRONG: Researching by reading three blog posts about the library in general.
  RIGHT: Researching the six items on the ignorance inventory, from the official changelog +
  installed source, probing each before use.
