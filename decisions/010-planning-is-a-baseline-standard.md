# 010. Make the planning standard baseline, not owner-facing

- **Date:** 2026-08-27
- **Status:** accepted

## Context and problem statement

Nothing in this universe constrained how a working plan is written. One build
ran a 2,273-line plan of 241 checkboxes for 15 days, retired it with 24 rows
still pending, invented eleven design and plan documents mid-flight because rows were not
implementable as written, and merged 30 of 44 pull requests over the size
convention. The new `standards/planning.md` fixes that. It has to be readable by
the agent that writes the plan, and that agent is working inside the repository
that owns the outcome.

## Considered options

- Mark it `owner_facing: true`, like `documentation.md`.
- Add it to `profiles.yaml` under `baseline`, like `work-routing.md`.
- Add it to selected profiles only.
- Fold the rules into `work-routing.md`, which is already baseline.

## Decision

Add `planning.md` to `baseline.standards`. Every governed repository's generated
`AGENTS.md` section links it.

## Rationale

[`work-routing.md`](../standards/work-routing.md) sets the precedent and the
reason. It was owner-facing, no generated section linked it, and two cold tests
could not answer from inside a repository where a plan belongs. A standard that
only `architecture` links is a standard only an agent already in `architecture`
reads.

A plan is authored in the repository that owns the outcome, per
`work-routing.md`. So is the pull request the size gate applies to. Both rules
are broken by an agent that never opens `architecture`, which makes an
owner-facing link the wrong home.

Folding the rules into `work-routing.md` was the cheapest option — a generated
section links the file, not its headings, so it would have invalidated no
baseline and cost no re-sync. It was rejected because the two answer different
questions. `work-routing.md` says where a change starts; this says how the plan
is written. One summary line cannot carry both, and the size gate would have
been invisible in the line a reader sees.

Per-profile registration was rejected for the same reason it would look
attractive: every profile that ships code plans work, so the selection would be
"all of them minus `fork-upstream-governed`", which `conformance: none` already
excludes.

The accepted cost is one more line in eleven generated sections. The managed
section budget is 40 non-blank lines and this change leaves it inside that.

## Consequences

- Every governed repository's generated `AGENTS.md` section is now stale.
  `tooling/universe drift` names them; each re-sync is follow-up work in the
  owning repository.
- A row that one pull request cannot close now fails plan approval, and an
  oversized pull request needs a named override in its body.
- `standards/planning.md` and the big-build skill in `myskills` now state
  overlapping rules. The standard is authoritative; the skill is executable
  behaviour that has to follow it. See
  [003](./003-myskills-remains-separate.md). Until the matching `myskills`
  change lands, `big-build` §11.5 still calls size a signal and still claims to
  define the convention. Nothing mechanical detects that staleness, so the two
  changes travel together or the conflict is live.
