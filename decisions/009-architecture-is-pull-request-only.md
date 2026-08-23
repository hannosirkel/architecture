# 009. Route initiative state through pull requests like everything else

- **Date:** 2026-08-23
- **Status:** accepted

## Context and problem statement

[`agent-operation.md`](../standards/agent-operation.md) carried two exceptions
to "agents never commit to a default branch". The first let durable initiative
state under `initiatives/*/` in `architecture` commit to `main` directly, on the
reasoning that a coordination record is not a code change and gating it behind
review would stall the resume path it protects. `architecture`'s ruleset
therefore deliberately carried no `pull_request` rule.

The exception never worked. `required_status_checks` rejects a push whose commit
has no check runs against it, which is every freshly created commit, so
`architecture` had been pull-request-only from the moment its ruleset was
applied. Three documents described the opposite. It surfaced when the commit
closing the bootstrap initiative was rejected with `GH013`.

The same rule had broken image promotion on `deploys` an hour earlier, and the
general form of it was written into `security.md` between the two failures.

## Considered options

- Add the agent's app as a bypass actor, restoring the documented behaviour.
- Accept pull-request-only and withdraw the exception.
- Remove `required_status_checks` from `architecture`, keeping direct pushes.

## Decision

Accept pull-request-only. Withdraw the exception from `agent-operation.md`, and
give `architecture` the full branch-protection floor, including a
`pull_request` rule with `required_approving_review_count: 0`.

## Rationale

A bypass actor is exempt from the **whole** ruleset, not from one rule. GitHub
offers no per-rule bypass. Restoring the exception therefore means granting the
agent that writes to this repository constantly the ability to force-push and
delete `main` on the repository that governs every other one. That is a large
permanent grant bought to avoid a small recurring friction.

Removing `required_status_checks` was rejected for the same shape of reason: it
weakens the control to preserve the convenience.

The exception's rationale — do not stall the resume path — is preserved without
the grant. Zero required approvals means an agent opens a pull request and
merges it as soon as the checks pass, with no human in the loop. The cost is one
pull request per state update, and a state update that cannot merge is one whose
checks are failing, which is a thing worth stopping for.

`deploys` keeps its bypass actors, because its case is genuinely different: the
pushing identity is a release workflow, not an interactive agent, and it pushes
one fast-forward commit built from reviewed content.

## Consequences

- `architecture` now matches the branch-protection floor with no exception, so
  `deploys` is the only public repository that still carries one.
- Every change to `architecture` is verified by CI before it lands, including
  coordination records. That was already true in practice; it is now true in
  writing.
- A session that wants to record state must open a pull request. Slower by one
  step, and self-merging keeps it unattended.
- The `security.md` exception for `architecture` is withdrawn.
