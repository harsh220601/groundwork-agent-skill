# Installing the `groundwork` skill

The skill is the `groundwork/` folder: `SKILL.md` + `references/` (plain markdown, no
scripts, no network needs). It follows the Agent Skills open standard (agentskills.io):
only `name` and `description` frontmatter, so it works unmodified in any harness that
supports the standard. Everything below was checked against the official docs on 2026-07-16
(platform.claude.com skills overview + best practices; code.claude.com/docs/en/skills).

## Claude Code

- Personal (all your projects): copy the folder to `~/.claude/skills/groundwork/`
- Per-project: copy to `<repo>/.claude/skills/groundwork/`
- The directory name is the command name — keep it `groundwork` (it must match the
  frontmatter `name`). Claude loads it automatically when the description matches, or invoke
  it explicitly with `/groundwork`. Changes to SKILL.md are picked up live within a session.
- To share across a team, commit `.claude/skills/groundwork/` to the repo, or distribute via a
  Claude Code plugin (a `skills/` directory inside the plugin).

## claude.ai (web/desktop)

- Zip the folder: `cd <parent-of-groundwork> && zip -r groundwork.zip groundwork`
  (the zip must contain the `groundwork/` directory at its top level, with SKILL.md inside).
- Upload under Settings > Features (custom skills; requires Pro/Max/Team/Enterprise with code
  execution enabled). Skills are per-user on claude.ai — each teammate uploads their own copy.

## Claude API

- Upload via the Skills API (`/v1/skills` endpoints) and reference the returned `skill_id` in
  the `container` parameter together with the code-execution tool; requires the beta header
  `skills-2025-10-02`.
- Note: the API container has NO network access — fine for this skill (pure markdown), but its
  web-research instructions will fall back to the offline paths it defines.

## Any other agent harness (generic)

- Place the folder anywhere the agent can read, and add one line to the project's standing
  instruction file (AGENTS.md, CLAUDE.md, system prompt, or equivalent):
  `Before any engineering task, read groundwork/SKILL.md and follow it, including the
  reference files it routes to.`
- Skills do not sync across surfaces — install separately per surface you use.

## Verify the install (any surface)

Ask the agent: "What does the groundwork skill require before you may claim a task is done?"
A correct answer mentions running the defined checks after the final edit and evidence/claim
tags. Then give it a tiny real task and confirm you see the Loop checklist and an evidence
block in its answer.

## Belt-and-braces trigger (recommended)

Auto-triggering depends on the harness matching your request against the skill description.
Stress-testing showed a weak model can pick the right skill yet fail to load it if the harness
misconfigures the path. For any repo where you always want the methodology active, add the
one-line pointer (previous section) to CLAUDE.md / AGENTS.md — it costs a few tokens and makes
loading unconditional.
