# Gate 2 Self-Audit — six required systems, verified present

Audited against the actual files on disk (paths + locations cited). Structure facts, all
VERIFIED by script this session: SKILL.md body = 196 lines (<500); description = 792 chars
(<1024, third person, no XML); name `groundwork` matches directory, lowercase-hyphen-valid;
6 reference files, all linked exactly one level deep from SKILL.md; every reference file
>100 lines has a table of contents.

## 1. THE METHOD — present
- Evidence-first problem solving: SKILL.md "The Loop" (Orient→Define done→Plan→Build→Verify→
  Hostile review→Record) + non-negotiables 1-4.
- Read real code before theorizing: Loop step 1 + debugging-playbook.md Phase 1-2 ("Run the
  failing thing FIRST", README/map orientation).
- Reproduce before fixing: non-negotiable 3; debugging-playbook.md Phase 1.
- Hypothesis → cheapest test → confirm or kill: debugging-playbook.md Phase 3 (incl. the
  "explains all observations AND predicts an unobserved one" confirmation bar, from Trace 1).
- Root cause over symptom: non-negotiable 4; playbook Phase 4; red-CI section rule 5-6.
- Deep-research protocol: references/research-protocol.md (pin version → ignorance inventory →
  docs → probes → reconcile → build), distilled from Trace 3.

## 2. THE ANTI-HALLUCINATION PROTOCOL — present
- Never reference unread files/APIs/docs: SKILL.md non-negotiable 2; protocol "Grounding rules"
  1-3.
- Never fabricate output/results/numbers: protocol "Fabrication bans" ("If you did not run it,
  you do not have it").
- Missing info = two legal moves only: SKILL.md "Claim tags" + protocol section of that name.
- Claim ledger VERIFIED/ASSUMED/UNKNOWN with reconciliation before done: SKILL.md "Claim tags";
  protocol ledger discipline; reporting block in self-testing-loop.md carries LEDGER lines.

## 3. THE SELF-TESTING LOOP — present
- Define success in checkable terms before building: Loop step 2; self-testing-loop.md Step 1.
- Plan → build → test own work → hostile review → fix → re-run: Loop steps 3-6;
  self-testing-loop.md Steps 2-5 with the two exit criteria (demonstrated pass / honest blocker).
- Failure discipline (no deleting/weakening/skipping tests, no exit-code games, no
  "works on my end"): self-testing-loop.md "Failure discipline"; anti-gaming signature scan in
  anti-hallucination-protocol.md.
- Hard bans on "should work"/"likely fixes": SKILL.md non-negotiable 1 (banned phrases named).
- Outcome recorded in the living system: Loop step 7.

## 4. THE LIVING PROJECT SYSTEM — present
- Project map generated on first contact: SKILL.md "Step zero" 2; project-map-spec.md
  "Creating the map" (with template: intended behavior, verified commands, architecture,
  curated index, invariants, decisions).
- Updated on every change, same session: project-map-spec.md "Updating the map"; Loop step 7.
- Learnings log with root-cause+fix+prevention schema: learnings-log-spec.md (schema + real
  example from Trace 1).
- Check-log-FIRST before debugging: SKILL.md Loop step 1 + route table; learnings-log-spec.md
  "Check-the-log-first discipline"; debugging-playbook.md loop preamble.
- Session close-out verifying map/log reflect reality + handoff schema: project-map-spec.md
  "Session close-out and handoff".

## 5. THE CREATIVITY CLAUSE — present
- SKILL.md "Creative freedom": full freedom in HOW; "invent solutions, never facts"; no
  exemption from non-negotiables, Loop, or ledger.

## 6. WHAT RESEARCH ADDS — present and non-empty
- SKILL.md "Research-backed additions (where each lives)" indexes 13 additions; each is
  actually implemented at the cited location (stuck tripwires w/ hard numbers; proceed-vs-ask
  by reversibility; step-zero local-law files; pre-flight green check; capability fallback
  ladder; fresh-context hostile review scoped to correctness; one-sentence-diff effort scaling;
  describe-then-edit + check-after-every-edit; layered-failure repair + intent ranking;
  version pinning/ignorance inventory/docs-vs-runtime reconciliation; handoff schema;
  check-log-first; green-test distrust + anti-gaming scan). Sources for each are in
  research-notes.md §6.

## Writing-standard spot checks
- Imperative voice throughout; every ban paired with replacement behavior (e.g. "not run"
  instead of fabrication; "migrate the laggard" instead of recreating deleted modules).
- Contrastive right-vs-wrong examples present in SKILL.md and all four behavioral references,
  drawn from the real Phase 1 traces (aliasing bug, zod record arity, utils→timeutil).
- Encoded judgment: intent-source ranking, confirmation bar for hypotheses, effort scaling,
  reviewer scoping — each stated as an explicit rule, not "use judgment".
- Portability: no tool names (says "run the test command", "file tools", "where your
  environment can run a subagent"), no machine paths, no harness-specific frontmatter or
  features. Plain markdown only. Checked by reading every file this session.
