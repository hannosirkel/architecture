# Build feedback loop — planned

Future large builds should close the useful half of the Context Development
Lifecycle without adding an eval platform. Keep one source for execution state,
test a cross-repository seam when it first becomes executable, and retain only
the failures that change a future check or instruction.

**Do not begin implementation from this record.** Start a separate approved
initiative after the Lousy Deal LD-01 working state is retired.

## Why this work exists

Lousy Deal LD-01 is the evidence base. At commit
[`cae1835`](https://github.com/hannosirkel/lousydeal/tree/cae18352d9024c33487e7622f2314c19279364db),
the build had grown from 26 planned rows to 42. One row remained open.

The process found serious faults, but paid too much to find them:

- The ledger was current while `docs/working/status.md`, plan checkboxes and the
  Big Build binding separately carried stale progress or plan shape.
- Several faults survived fresh-context review and appeared on the first real
  run. They crossed repository, runtime or external-state boundaries that a
  local diff could not execute.
- Targeted negative controls exposed tests that passed without protecting the
  property in their name. Large mutation campaigns also consumed more review
  effort than a future build should require.
- The 6,682-line working record preserved valuable discoveries together with
  transient commands, repeated facts and corrections to earlier prose.
- Synthesized briefs and explanatory comments introduced many false claims.
  Review then spent effort correcting context that the implementation did not
  need.

The immutable source is the
[`ld-01-foundation` state](https://github.com/hannosirkel/lousydeal/tree/cae18352d9024c33487e7622f2314c19279364db/docs/working/ld-01-foundation)
at that commit. Do not copy its journal into this repository.

## Outcome

Implement three changes as one cross-repository initiative.

### One execution state

Keep the ledger as the only persisted row state. Generate a resume summary from
the ledger and current repositories. Do not persist a second status document or
mirror row status into plan checkboxes.

An `architecture` initiative can still carry `state.yaml` for registration.
When Big Build owns execution, use a reference-only variant containing the
schema version, initiative name, contract path and digest, and the owning
ledger's repository and path. Do not record lifecycle status or a ledger commit:
status would mirror execution, while the commit would change with execution or
become stale. Omit `current_phase`,
`current_gate`, `last_completed_step`, `next_action`, `last_run`, `repositories`,
`worktrees`, `completed_steps`, `open_prs`, `blockers` and
`operator_action_required`. Update the initiative template to define this
variant.

Remove derived facts from a Big Build binding. A binding keeps only facts that
the plan and catalogue cannot supply: effect gates, operator and joint work,
anti-goals, declared initial absences, and plan-specific external checks.

Preflight computes plan shape, completed count, next row, repository facts and
the conflict map. It refuses when it cannot derive one of them. It does not ask
an author to keep a duplicate current.

### Verification at first executable use

Every cross-repository interface names its **first executable use** in the plan.
Here, an interface is a value or artifact produced in one repository and
consumed from another. The first executable use is the first row whose declared
prerequisites include the merged producer and a runnable consumer. Run one real
check in that row. Do not defer it to a later assembly row. If execution changes
external state, the existing effect gate still controls it.

Keep local tests on the rows that create each side of the interface. The first
executable-use check covers only the seam between them. An effect still waits
for its operator gate.

For a new custom guard or refusal path, demonstrate one discriminating negative
control: remove or invert the guarded condition, assert that the mutation was
applied, and observe the named check fail. Do not require general mutation
testing or a mutation score.

### Promotion instead of an exhaustive journal

Keep command output in CI or pull requests. Store only its reference in the
ledger. Do not require an append-only transcript of every action.

At a task boundary, record only an unexpected failure that could improve later
work. Put this small block in the row's ledger entry; do not create a findings
file:

| Field | Meaning |
| --- | --- |
| Failure | The observed behaviour, without a theory presented as fact |
| Earliest detector | The cheapest earlier check that could have found it |
| Scope | This row, this repository, or future builds |
| Disposition | Test, instruction, issue, or discard |

Before retirement, resolve every block. Implement its test or instruction,
create an issue for an unresolved repository problem, or record why it is
discarded. Promote only entries whose scope is `future builds`. A promoted entry
changes a deterministic check or one canonical instruction. Write one dated
evidence record that links those changes. Then remove the ledger and transient
blocks with the other working state. Existing pull-request, CI and dated
evidence records remain immutable.

## Repository work and order

Each row below is one pull request in one repository.

1. `architecture`: decide the final state and evidence contract. Update
   `standards/planning.md`, `standards/documentation.md`,
   `standards/repository-contract.md`, `templates/initiative/README.md` and its
   tests only where the existing contract conflicts with this outcome.
2. `myskills`: simplify Big Build state, binding and context-packet rules. Add
   installer tests for the delivered mechanism and focused tests for any new
   executable checker.
3. `myskills`: add purpose-built fixtures. One has a known producer row, first
   runnable consumer row and later assembly row. One ordinary application test
   is not a guard. Prove that derived progress and plan shape need no persisted
   mirror, that the seam check cannot move to the assembly row, and that the
   ordinary test needs no negative control.
4. `architecture`: run one cold-context exercise. Give a fresh agent the
   fixture and ask for the next row, the first executable-use check, and the
   future-build findings. Require the agent to write its resume summary to
   stdout and leave the fixture tree unchanged. Record errors; do not tune the
   prompt during the run.

The standards change supplies the interface. Publish it before `myskills`
consumes it. The final cold-context exercise runs against both merged revisions.

## Acceptance criteria

- The fixture has one ledger and no tracked status file or checked plan row.
  Two temporary copies with different ledger statuses produce different
  cold-context resume answers. The tracked source fixture stays unchanged and
  `git status --short` stays empty.
- Initiative `state.yaml` uses the reference-only variant and contains none of
  the progress, runtime, repository or worktree fields excluded above.
- The fixture binding contains no row count, resume position, current
  repository fact or hand-maintained conflict map.
- The seam fixture fails its review when the first-executable-use declaration
  is absent or points at its later assembly row. Its real seam command runs in
  the known first runnable consumer row.
- The custom-guard fixture confirms its mutation applied and then observes its
  named test fail. The ordinary-test fixture passes with no mutation step.
- The retirement fixture refuses an unresolved block. It moves a repository
  residual to an issue, records an explicit discard, leaves one dated evidence
  file linking the promoted change, and removes transient execution state.
- The cold-context exercise identifies the next row and seam check without
  conversation history and leaves no tracked diff.
- `bash tests/run` passes in `myskills`. Architecture's unit tests, Ruff,
  catalogue validation and universe audit pass. Existing safety tests are not
  weakened or deleted.

## Exclusions

Do not add:

- telemetry instrumentation, trace storage or an agent-observability service;
- any evaluation platform, probabilistic or deterministic;
- repeated-trial error budgets;
- a context package registry or new installer;
- a general mutation-testing framework or score;
- another persisted execution-state format or per-action transcript;
- central copies of repository-local execution state.

Reconsider task-evaluation infrastructure only after at least three builds use
the simplified process and produce a repeated failure that repository-native
checks cannot distinguish.

## CDLC boundary

This work adopts the smallest useful part of each stage:

| Stage | Adoption |
| --- | --- |
| Generate | Build task context from canonical plan, catalogue and ledger data. |
| Evaluate | Run one real seam check and one negative control where each applies. |
| Distribute | Continue using generated baselines and the existing skill installer. |
| Observe | Promote unexpected real-use failures at retirement. |

Distribution already has an owner and working machinery. Do not rebuild it in
this initiative. Observation supplies candidates; it does not justify retaining
a transcript.

## Starting the initiative

1. Confirm that LD-01 has retired and that its durable evidence is reachable by
   immutable commit reference.
2. Write `initiatives/active/build-feedback-loop.md` from the initiative
   template, with one row per pull request above.
3. Record the exact `architecture` and `myskills` starting commits.
4. Inventory every active Big Build plan before changing the skill. Migrate all
   of them before publishing the new mechanism. If one cannot migrate, stop the
   initiative; do not support two installed mechanisms.
5. Obtain operator approval of the state deletion and migration boundary before
   editing `myskills`.
