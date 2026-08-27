# 011. Baseline the initiative-state pushes the withdrawn exception excused

- **Date:** 2026-08-27
- **Status:** accepted

## Context and problem statement

[009](./009-architecture-is-pull-request-only.md) withdrew the exception that
let durable initiative state under `initiatives/*/` push to `main` directly. The
catalogue still carried the field that implemented it,
`architecture.direct_push.allowed_paths: ["initiatives/"]`, which tells the
audit to excuse a commit that touches only that prefix. Fifteen such commits,
all from 2026-08-21 and 2026-08-22, sit in the last fifty on `main`. Removing
the field alone makes the audit fail on all fifteen.

## Considered options

- Keep `allowed_paths`.
- Remove `allowed_paths` and accept the fifteen findings.
- Remove `allowed_paths` and move `baseline_commit` to the last push it excused.

## Decision

Remove `allowed_paths`. Move `baseline_commit` from `bfc5130` to `ad01989`, the
last initiative-state push made under the exception.

## Rationale

`allowed_paths` is not a record of the past. It is a standing permission.
Keeping it means the check excuses the next agent that pushes initiative state,
while `agent-operation.md`, `AGENTS.md`, and 009 all say it must not. A control
that contradicts the rule it implements is worse than no control.

Accepting the fifteen findings was rejected because they are not violations.
Each one was correct under the rule in force on the day it was made. An audit
that fails on lawful history teaches a reader to ignore it. That is what
`baseline_commit` is for, and every catalogue entry already gives it that
meaning.

The trade-off accepted: the baseline now covers more commits than `bfc5130` did,
so a violation before `ad01989` would no longer be reported. Between the two
commits, nothing reached `main` except merged pull requests and these fifteen.

## Consequences

- A direct push to `architecture`'s `main` after `ad01989` fails the audit,
  including one under `initiatives/`.
- `architecture` carries no path exception. `deploys` keeps the only one left.
- A later rule withdrawal repeats this shape: remove the exception, and baseline
  what it lawfully excused.
