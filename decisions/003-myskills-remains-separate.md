# 003. Keep `myskills` separate from `architecture`

- **Date:** 2026-08-21
- **Status:** accepted

## Context and problem statement

`architecture` governs how work is done. `myskills` holds executable procedures
that do work. Both are private, both are cross-repository, and merging them
would be easy.

## Considered options

- Merge `myskills` into `architecture`.
- Keep them separate, with `architecture` pinning skill versions.
- Keep them separate with no relationship recorded.

## Decision

Keep them separate. `architecture` defines approved intent and pins skill
commits in an initiative's `skills.lock.yaml`. `myskills` contains reusable
executable behaviour.

## Rationale

They have different change rates, different risk profiles, and different
reviews. A skill change is an executable-behaviour change: it needs tests and
review. A standards edit is a policy change: it needs a decision.

Merging them would put executable code behind a governance review and governance
text behind a skills review. Neither gains.

`myskills` also has a path toward public sanitization that `architecture` does
not. Merging would close it.

## Consequences

- `architecture` owns exactly one skill, `skills/audit-universe/`. See
  [005](./005-audit-skill-lives-in-architecture.md).
- An initiative that needs a new reusable capability adds it to `myskills`,
  tests it, and pins the commit.
- Initiative-specific orchestration stays in the initiative. Do not create a
  one-off skill for a single piece of work.
