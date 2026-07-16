# Research Notes — Methodology-Transfer Skill (Phase 0)

Date: 2026-07-16. Session: Claude Fable 5 in Claude Code.
Evidence labels: **VERIFIED** = a page fetched and read this session (by me or by a research
subagent that returned a quote + URL). **UNVERIFIED** = from memory or search snippets only.

## 1. Sources actually read this session

Read directly by me (full pages):
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices (full text)
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (full text)
- https://code.claude.com/docs/en/skills (full text, persisted to disk and read)

Read by research subagents this session (each finding returned with URL + verbatim quote):
- https://agentskills.io/specification (open Agent Skills spec)
- https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md
- https://github.com/anthropics/skills
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://code.claude.com/docs/en/best-practices , https://code.claude.com/docs/en/memory
- https://aider.chat/docs/repomap.html , https://aider.chat/2023/10/22/repomap.html ,
  https://aider.chat/2024/09/26/architect.html , https://aider.chat/docs/usage/conventions.html
- https://agents.md/ , https://llmstxt.org/ , https://code.claude.com/docs/llms.txt
- https://arc42.org/overview , https://c4model.com/
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://www.anthropic.com/research/swe-bench-sonnet (and /engineering/swe-bench-sonnet)
- https://claude.com/blog/building-agents-with-the-claude-agent-sdk
- https://platform.claude.com/docs/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Papers (fetched abstracts/full text): CoVe arXiv:2309.11495; Huang et al. self-correction
  arXiv:2310.01798; Reflexion arXiv:2303.11366; self-consistency arXiv:2203.11171; CodeT
  arXiv:2207.10397; MT-Bench judge biases arXiv:2306.05685; SWE-agent arXiv:2405.15793 (PDF);
  SWE-Bench+ arXiv:2410.06992; METR reward hacking metr.org/blog/2025-06-05-recent-reward-hacking;
  CoT-monitoring arXiv:2503.11926; lost-in-the-middle arXiv:2307.03172; IFScale arXiv:2507.11538;
  SCALEDIF arXiv:2510.14842; contrastive CoT arXiv:2311.09277; negated prompts arXiv:2209.12711
- https://swe-agent.com/latest/background/aci/ , https://docs.openhands.dev/sdk/guides/agent-stuck-detector
- https://www.anthropic.com/engineering/multi-agent-research-system
- https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents
- https://ampcode.com/manual , https://cursor.com/docs/rules
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide and gpt4-1_prompting_guide
- https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f (cross-harness compaction study)

## 2. DECISION: Skill structure (VERIFIED against official docs + open spec)

- `SKILL.md` with YAML frontmatter `name` + `description` ONLY (portable core of the
  agentskills.io spec). No Claude Code-only fields (`allowed-tools`, `context: fork`, `paths`,
  `$ARGUMENTS`, `` !`cmd` `` injection) — those don't exist in other harnesses.
- `name`: ≤64 chars, lowercase/digits/hyphens, no leading/trailing/double hyphen, MUST match the
  directory name, must not contain "anthropic"/"claude" (validation rules from overview + spec).
- `description`: ≤1024 chars, third person, states WHAT + WHEN, deliberately "pushy" with trigger
  keywords — Anthropic's own skill-creator says models under-trigger skills, so over-specify
  contexts. Adjudication of a critic finding: trigger keywords all go in the description, but the
  body ALSO opens with a one-line scope statement, because once loaded the body must stand alone.
- Body < 500 lines (docs: "under 500 lines for optimal performance"), target well under —
  bloat measurably causes instruction-dropping ("Bloated CLAUDE.md files cause Claude to ignore
  your actual instructions!").
- `references/*.md` exactly one level deep, each linked from SKILL.md with "read this when…"
  routing; TOC at top of any reference file > 100 lines (docs: partial `head -100` reads happen).
- Progressive disclosure is real and has token budgets: metadata ~100 tokens always loaded;
  body <5k tokens on trigger; references zero cost until read (overview doc table).
- Writing style per official guidance: standing instructions (content persists across turns),
  checklists the model copies into its response, validator feedback loops with hard gates
  ("Only proceed when validation passes"), one default + escape hatch, consistent terminology,
  no time-sensitive info, forward-slash paths, concrete right-vs-wrong examples.

**Skill name decision:** `groundwork` (noun form is an accepted alternative per naming
conventions; short, durable, describes the method: ground every claim, do the groundwork first).

## 3. DECISION: Project map format

Candidates evaluated (all VERIFIED — see sources above):

| Candidate | Token cost | Lookup | Update friction | Weak models | Verdict |
|---|---|---|---|---|---|
| A. Aider-style ranked signature map | best (~1k tokens) | good | FAILS — needs tree-sitter + graph ranking tooling, regenerated not hand-edited | fine | Reject as format; steal the selection principle |
| B. Exhaustive annotated file tree | high | fine | high (every file touch = map edit) | drowns them | Reject — Anthropic explicitly excludes "file-by-file descriptions of the codebase" and anything derivable from code; /doctor trims exactly this |
| C. Architecture-first doc (arc42/C4) | high | poor (prose) | high | poor | Reject as-is; borrow zoom order (system → modules → key files) and Decisions/Glossary sections |
| D. Hybrid structured-markdown single file: non-derivable facts + curated llms.txt-style index | low (~200 lines cap) | good (headings, grep) | lowest — plain markdown edited with any file tool | best | **CHOSEN** |

**The chosen format** (full spec goes in `references/project-map-spec.md`):
single plain-markdown file `PROJECT-MAP.md` at project root, hard-capped ~200 lines, sections in
C4-ish zoom order: (1) What this is + intended behavior, (2) Commands (build/test/run — verified,
with the output that proves they work), (3) Architecture at a glance + data flow, (4) Curated
index: entry points and key files/dirs, one line each, llms.txt grammar (`- path — role`),
(5) Invariants/gotchas/cross-file causality ("changing X requires regenerating Y"),
(6) Decisions. Updated by direct edit after every meaningful change — no generator, no build step
(this is exactly how CLAUDE.md and Claude Code auto-memory work in production; MEMORY.md's
200-line/25KB index cap is proof agents can self-police size).

**Why markdown, single file:** llmstxt.org ("the most widely and easily understood format for
language models is Markdown"), AGENTS.md ecosystem (schema-free markdown, 60k+ repos claimed on
agents.md — count itself UNVERIFIED), every harness can read/edit it with generic file tools,
headings give cheap lookup, and JSON/YAML would add delimiter cost + brittle hand-editing.

**⚠️ Flagged conflict with the mission prompt (per discovery mandate):** the prompt asks for a
"directory/file purpose index". Anthropic's guidance explicitly says NOT to include exhaustive
file-by-file descriptions (derivable from code; bloat causes rule-dropping). Resolution: the map
carries a **curated** index — entry points, the ~10-30 files/dirs someone actually needs, and
"where to look for X" pointers — not every file. The mission's goal (next agent goes straight to
the right file) is served; the failure mode (200-line cap blown, adherence cliff) is avoided.
Not silently obeying either side; this is the logged adjudication.

## 4. DECISION: Anti-hallucination techniques that earn a place (evidence-ranked)

Techniques with direct evidence, strongest first:

1. **External signal or it didn't happen.** Every source converges: Claude Code docs ("Without a
   check it can run, 'looks done' is the only signal"; "show evidence rather than asserting
   success"), building-effective-agents ("ground truth from the environment at each step"),
   SWE-bench scaffold (top failure mode = overconfidence). → Rule: no success claim without a
   command run this session + its verbatim output.
2. **Intrinsic self-critique DOES NOT WORK — it degrades results.** Huang et al.: GPT-4 GSM8K
   95.5→89.0, GPT-3.5 CSQA 75.8→41.8 after bare "review your answer" rounds. → Rule: every
   review cycle must ingest something new and external (test output, lint, diff, docs).
   Never encode "reflect on your reasoning" as a step.
3. **Factored verification.** CoVe: verification in a context that cannot see the draft roughly
   doubles precision (0.17→0.36) because models copy their own hallucinations. Claude Code:
   fresh-subagent review of diff+criteria only. → Portable rule: verify the artifact against
   written criteria, not your memory of making it; use a fresh subagent where available.
4. **Distrust green tests.** SWE-Bench+ (31.08% of passing patches suspicious), Reflexion
   (16.3% false-pass from self-written tests), METR (agents monkey-patch evaluators; o3 hacked in
   ~80% of runs DESPITE explicit don't-cheat instructions), OpenAI monitor paper (hack signatures:
   always-return-true verify, sys.exit(0), raised SkipTest, stub constants). → Rules: tests must
   fail before the fix and pass after; diff must not touch tests/verifier/config unless that IS
   the task; mechanical diff self-inspection step, because instructions alone are insufficient.
5. **Reproduce-first debugging.** Anthropic SWE-bench prompt verbatim: "Rerun your reproduce
   script and confirm that the error is fixed!" → Encoded as the debugging loop's spine.
6. **Deterministic guardrails at the edit boundary.** SWE-agent ablation: linting the edit
   ≈ +3pp resolve rate; stops cascading errors. → Rule: syntax/lint/typecheck immediately after
   every edit, before moving on.
7. **Claim ledger.** Anthropic reduce-hallucinations doc: permission to say "I don't know",
   cite-or-retract, quote-first grounding. Mission floor requires VERIFIED/ASSUMED/UNKNOWN tags —
   compatible and adopted.
8. **Verification ladder.** Agent SDK post: rules-based checks best, visual second, LLM-as-judge
   explicitly last ("generally not a very robust method") with known biases (MT-Bench:
   position/verbosity/self-enhancement). → Encoded as an ordered ladder.
9. **Self-consistency as last resort** when nothing is executable (+17.9% GSM8K): state the
   answer twice via different routes; disagreement = don't trust it. Cheap, portable.

Rejected/softened:
- SWE-agent's 100-line observation window: 2024 GPT-4-era ACI artifact; modern harness Read
  tools have sane defaults, and the critic flagged codifying it as risky. Softened to "read
  selectively; don't dump whole trees into context."
- Bare "don't hallucinate" instructions: no evidence they work; replaced by mechanical steps.

## 5. DECISION: Writing for weaker models (evidence-backed rules used while authoring)

1. Positive imperatives; never a bare prohibition (negated-prompts paper: negation reliability
   is poor and worsens with scale). Pair every ban with the replacement behavior.
2. Few rules, front-loaded, repeated at the end (sandwich): IFScale (adherence decays with rule
   count; primacy bias), lost-in-the-middle (arXiv:2307.03172), GPT-4.1 guide (instructions at
   both ends of long content beat either alone).
3. Copy-into-response checklists with hard gates and loop-backs — officially recommended pattern;
   weak models cannot self-derive procedure (CoT is an emergent large-model capability).
4. Contrastive right-vs-wrong pairs that mirror real tasks; every behavior an example shows is
   also stated as a rule (GPT-4.1 guide: examples override prose).
5. Decision tables / explicit conditional routing; exactly one default + named escape hatch.
6. Rule + why in one clause — models generalize from motivation (Anthropic prompting docs:
   "Claude is smart enough to generalize from the explanation").
7. Emphasis adjudication (critic-flagged conflict): Claude Code docs say IMPORTANT/YOU MUST
   improves adherence on under-following models; skill-creator says all-caps everywhere is a
   yellow flag. Resolution: rule+why in imperative prose as default; reserve strong emphasis for
   the ~5 non-negotiables so it keeps discriminating. Logged, not silently resolved.
8. Deletion test per line ("Would removing this cause mistakes?"); conflict audit before shipping
   (SCALEDIF: rule conflict is a measured driver of non-compliance; later rule silently wins).
9. Consistent terminology: one term per concept, everywhere.

## 6. Discovery mandate — additions beyond the mission floor (each with source + reason)

Adopted into the skill (Section "What research adds" / woven into systems):
1. **Numeric tripwires for being stuck** — 2 failed fix attempts on the same issue → stop and
   re-derive from evidence (Claude Code /clear-after-two-corrections); 3 identical errors or 4
   identical action-observation repeats → declare stuck, change strategy or surface it
   (OpenHands stuck-detector). Reason: weak models flail; "use judgment" is not executable.
2. **Ask-vs-proceed action-class table** — reversible/read-only → proceed and document the
   assumption; destructive/irreversible/external → stop and ask (GPT-5 prompting guide
   persistence + confirmation-threshold pattern). Reason: weak models both over-ask and
   plow through deletes.
3. **Step zero: obey local law** — look for AGENTS.md / CLAUDE.md / .cursor/rules /
   CONVENTIONS.md (nearest wins) and follow them; probe unknown CLIs with `--help` instead of
   guessing flags (Claude Code best practices; agents.md precedence rule). Reason: cheapest
   anti-hallucination move for commands; respects the host project.
4. **Handoff schema** — before context runs out or a session ends mid-task, write: accomplished /
   in progress / files touched / next steps / constraints (the exact fields all major harnesses'
   compaction preserves, per cross-harness study). Reason: session continuity is where weak
   agents silently lose state.
5. **Fresh-context review with scoping caveat** — reviewer sees diff + criteria only, and reports
   only correctness-affecting findings (Claude Code: "A reviewer prompted to find gaps will
   usually report some, even when the work is sound"). Reason: prevents both self-grading and
   review-driven over-engineering.
6. **Effort scaling** — if the diff is describable in one sentence, skip the plan (Claude Code);
   scale ceremony to task size (Anthropic multi-agent post tiers). Reason: weak models over-apply
   rituals; calibration must be explicit.
7. **Describe-then-edit split** — state the change in prose first, then apply as small,
   uniquely-anchored edits (aider architect/editor: separating reasoning from edit-formatting
   scored 85% on their benchmark, best result). Reason: directly targets weak-model edit failures.
8. **Codify step / learnings log flow** — after review/debug, distill lessons into a repo file the
   next session reads first (Every's compound engineering: "80% of compound engineering is in the
   plan and review parts"). Mission already mandates the log; research adds the check-log-FIRST
   discipline and the entry schema.
9. **Empty output is information** — explicitly note "command ran, produced no output" instead of
   treating it as failure or fabricating output (SWE-agent ACI). Reason: a documented
   weak-model confusion point.
10. **Name the feedback loop in the task spec** — when starting any task, write down which
    command/URL/log will prove it works (Amp manual: "Tell the agent how to best review its
    work"). Reason: makes the self-testing loop concrete before building.

Critic-identified gaps and how the plan addresses them:
- Triggering reliability on weak models unknown → Phase 3 tests description-triggering with a
  cheaper model; INSTALL.md will recommend a one-line pointer from CLAUDE.md/AGENTS.md as a
  belt-and-braces load path on harnesses where auto-trigger is weak.
- Rule-count budget vs. rule superset → SKILL.md carries only the non-negotiables + the loop +
  routing; everything else lives in references (progressive disclosure is the budget mechanism).
- Capability floor of Haiku-class models → empirical question; Phase 3 cheaper-model runs.
- Evidence from 2024-era harnesses may not transfer → magnitudes treated as directional; no
  2024-specific mechanics codified (e.g. no 100-line window rule).
- Feature availability across harnesses → skill gets an explicit fallback ladder (no subagents →
  artifact-only re-read; no git → manual before/after copies; no test runner → write a smoke
  script; no network → say so and mark claims UNVERIFIED).

## 7. Installation facts for Phase 4 (VERIFIED this session)

- Claude Code: `~/.claude/skills/<name>/SKILL.md` (personal) or `.claude/skills/<name>/SKILL.md`
  (project); nested and parent discovery; live change detection; plugins for distribution.
- claude.ai: upload zip via Settings > Features; Pro/Max/Team/Enterprise with code execution
  enabled; per-user, not org-synced.
- Claude API: upload via `/v1/skills` endpoints; requires code-execution tool + beta header
  `skills-2025-10-02`; container has NO network access and no runtime package installs.
- Skills do not sync across surfaces; install separately per surface.
- Open standard: agentskills.io — name must match directory; only name+description are core.

## 8. Unverified items carried forward (flagged, not relied on)

- "60,000+ open-source projects" AGENTS.md adoption figure (agents.md's own claim).
- Aider's ranking = PageRank specifically (docs say only "graph ranking algorithm").
- Haiku "cannot generate syntactically correct actions" benchmark claim — could not be located
  in fetched sources; NOT used as a design input.
- Any quantitative head-to-head of map formats — none exists in fetched sources; format decision
  rests on convergent qualitative rationale + production precedent.
- Exact SWE-agent "10.7pp vs shell-only" figure ambiguity (7.0pp vs no-demonstration 10.67pp).
- METR/CoT-monitor percentages are for frontier models in 2025 evals; treated as directional
  evidence that anti-cheat instructions alone are insufficient, nothing more.
