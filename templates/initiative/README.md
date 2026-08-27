# Initiative template

Copy this directory when a change spans several peer repositories or has no
clear single owner. See
[`standards/work-routing.md`](../../standards/work-routing.md) for when that
applies.

## Layout

```text
initiatives/active/<name>.md          the contract, canonical
initiatives/active/<name>/            its durable state
  resolved-plan.md
  state.yaml
  open-questions.md
  decisions/
  journal/YYYY-MM-DD.md
  evidence/
```

The contract and its state directory are siblings. The state directory holds no
second copy of the contract. Record the contract's content digest in
`state.yaml` so drift between the approved contract and the running one is
detectable.

Do not rename or date-prefix the contract. The invocation string, the resume
path, and the file name must stay aligned.

## Rules

- Durable initiative state goes through a pull request, like every other
  change. `architecture` requires zero approving reviews, so an agent merges
  its own state update once the checks pass. See
  [`decisions/009`](../../decisions/009-architecture-is-pull-request-only.md).
- Do not create one enormous append-only journal. Use dated files.
- Do not commit a raw transient log. Commit a concise evidence summary.
- Add `migration-map.yaml`, `repositories.yaml`, or `skills.lock.yaml` only when
  the initiative has that kind of state.
- Move the initiative to `initiatives/completed/` only when doing so does not
  break a resume path.

## Minimum `state.yaml`

```yaml
schema_version: 1
initiative: <name>
status: DISCOVERING | IMPLEMENTING | BLOCKED | COMPLETE
contract_path: initiatives/active/<name>.md
contract_digest: "sha256:..."
current_phase: <phase>
current_gate: <gate>
last_completed_step: null
next_action: <what happens next>
last_run:
  runtime: <runtime>
  tier: top | mid | low
  model: "<model>"
  at: "<ISO 8601 UTC>"
repositories: {}
worktrees: {}
completed_steps: []
open_prs: []
blockers: []
operator_action_required: null
```

`last_run` is an audit trail, not a lock. All governed repositories have one
owner and one session advances an initiative at a time. Do not build lease,
heartbeat, or takeover machinery.

The protections that matter if two sessions ever overlap are the mechanical ones
in [`standards/agent-operation.md`](../../standards/agent-operation.md):
isolated worktrees, one writer per worktree, and never writing into a dirty or
shared checkout.

## Resuming

1. Read the contract and the state before acting.
2. Verify the contract digest, repository HEADs, worktrees, open PRs, and
   blockers.
3. Reconcile drift explicitly.
4. Continue from `next_action`.
5. Do not repeat completed work unless its evidence is stale or invalid.
6. Do not ask the operator to restate a fact available in Git or in state.
