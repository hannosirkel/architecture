# Open questions

**All eight are answered.** The operator approved the resolved plan at Gate 1,
authorised subagent delegation, and accepted every proposed default. This file
is kept as the record of what was asked and what was decided.

| Question | Outcome |
| --- | --- |
| Q1 subagent delegation and top-tier review | authorised; the review ran and found six defects |
| Q2 Habit Hooks `files` and `jscpd` | proposal accepted; see decisions/006 |
| Q3 `deploys` branch-protection floor | proposal accepted; named exception in standards/security.md |
| Q4 `robobook`'s `CLAUDE.md` symlink | proposal accepted; replaced by the generated pointer |
| Q5 `mihkel`'s ten root documents | proposal accepted; exception recorded as a local decision |
| Q6 `nomadtty`'s `change-trace.md` | kept, not deleted |
| Q7 `plepic`'s `docs/superpowers/` | moot: another session retired the plans mid-run |
| Q8 `deploys` declares `shell` | proposal accepted; evidence beats the contract's illustration |

## Q1 — May this session delegate to subagents, and to a top tier?

**Answered: option 1.** Delegation authorised. The §11 review ran at the top
tier and found six defects, two of which self-checking could not have caught.
§16 item 13 is satisfied for the three load-bearing documents. See
`evidence/top-tier-review.md`.

§11 requires a top-tier (Fable/Sol) review of authority boundaries, public and
private classifications, migration of shared standards, and the final
conformance review. §16 item 13 requires top-tier review of three documents and
says self-certification does not satisfy it. §8.1 requires parallel subagent
audits with a high-tier synthesis.

This session runs under an instruction not to use the subagent tool unless the
operator asks for it. §11 says: if only a lower tier is available, record it as
an open item rather than treating the review as done. This is that record.

**Options:**

1. Authorise subagent delegation for this initiative. The reviews happen as §11
   specifies.
2. Keep delegation off. Then §16 item 13 cannot be satisfied by this session,
   and the three load-bearing documents ship marked as awaiting review.

**Default if unanswered:** option 2, with the gap recorded in state and in the
final report.

## Q2 — Habit Hooks needs more than one command. Which way out?

**Status:** blocking for wave 2; see `evidence/habit-hooks-verification.md`.

Two facts contradict §7.6's model of a self-contained coaching layer:

- A repository declaring no language Habit Hooks has a plugin for scans nothing
  and prints a green tick. `generic` declares no `files`.
- The sensors spawn external tools. `jscpd`, `eslint`, `knip`, and `ts-morph`
  resolve from a project's `node_modules`. Four governed repositories have no
  `package.json` at all.

**Proposed:** the generator emits an explicit `files` list for every repository,
and `[sensors.jscpd] disabled = true` where there is no npm project. `line-count`
still runs there, which is the part that catches oversized files in YAML and
Markdown. The workstation prerequisite in `standards/code-quality.md` names the
full set: `uv`, `habit-hooks[python,typescript]`, `ruff`, `deptry`, `jq`, `node`.

**Alternative rejected:** adding `jscpd` as a devDependency to `deploys` and
`entpass` to satisfy a coach. That is a `package.json`, a lockfile, and a
Renovate surface in a repository that has no JavaScript, for one duplication
sensor.

**Default if unanswered:** the proposal above.

## Q3 — `deploys` cannot take the full branch-protection floor

**Status:** decided by evidence; confirm.

`deploys/main` receives automated digest pushes from `plepic` and `servitium`
release workflows. A `pull_request` rule breaks promotion. Its ruleset today is
`deletion` + `non_fast_forward` only.

**Proposed floor for `deploys`:** `deletion`, `non_fast_forward`, and
`required_status_checks` on the `Validate` workflow. No pull-request
requirement. Recorded as a named exception in `standards/security.md`, not as a
gap.

**Default if unanswered:** the proposal above.

## Q4 — `robobook`'s `CLAUDE.md` is a symlink

`robobook/CLAUDE.md` is a symlink to `AGENTS.md`. It cannot drift, which is
better than a pointer document that can. §7.1 requires a generated pointer file
identical everywhere.

**Proposed:** replace it with the generated pointer, for uniformity and because
a symlinked instruction file behaves differently across agent runtimes and on
filesystems without symlink support. Cost: one more generated file to keep in
step, which the sync tool already does.

**Default if unanswered:** the proposal above.

## Q5 — `mihkel`'s ten root documents

`mihkel` carries `SOUL.md`, `IDENTITY.md`, `ACCESS.md`, `WORKFLOWS.md`,
`PROJECT_STATE.md`, `TOOLS.md`, `USER.md`, `MEMORY.md`, `DECISIONS.md`, and
`HEARTBEAT.md` at the root. §5.10 says root documents stay few.

These are an agent's operating identity, read at runtime by the agent itself,
not documentation about a repository. Restructuring them to satisfy a layout
rule risks breaking a running agent.

**Proposed:** keep them. Record the exception as a decision in `mihkel`, linked
from its `AGENTS.md` per §7.3 item 6. The audit does not flag them.

**Default if unanswered:** the proposal above.

## Q6 — `nomadtty`'s `docs/ai/change-trace.md`

1166 lines of implementation history. §5.10 says `current/` does not narrate
history, and Git already holds it.

**Proposed:** read it for durable facts, fold anything durable into
`docs/current/`, then delete it. Deleting a document is a Gate 2 item when it is
disputed; this one is proposed rather than done.

**Default if unanswered:** keep it as `docs/current/change-trace.md` and flag it
for a later decision. Deleting without an answer is the worse error.

## Q7 — `plepic`'s `docs/superpowers/` versus Orange's convention

**Overtaken by events.** Another session merged the Stripe work and retired the
plans into the README while this initiative was running. `docs/superpowers/` no
longer exists in `plepic`, and the registered working path was removed from the
catalogue. The convention below still stands for the next repository that tracks
tool-generated plans.

Orange's convention ignores `docs/superpowers/` and routes tool-generated plans
to the private inventory. `plepic` tracks them in the public repository. §5.10
names `docs/working/`.

**Proposed:** `docs/working/` is the universe convention. `plepic` moves its
tracked plans there once the active transactional-email work completes; Orange
keeps routing its own to the private inventory, which is a public/private rule,
not a layout rule. Register both now, move nothing during wave 1.

**Default if unanswered:** the proposal above.

## Q8 — `deploys` declares `shell`, against the contract's illustration

§7.6 uses `deploys` as the example of an empty `languages` list. Evidence
contradicts it: three bash files, two of which carry the manifest contract
assertions.

**Proposed:** declare `shell`. §7.1 says populate from evidence, not
expectation, and the contract's illustration is not the catalogue.

**Default if unanswered:** the proposal above.
