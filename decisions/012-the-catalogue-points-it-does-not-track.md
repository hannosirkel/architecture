# 012. Make `notable_local_work` point at initiatives, not track progress

- **Date:** 2026-08-28
- **Status:** accepted

## Context and problem statement

`standards/work-routing.md` said to register substantial active work in
`notable_local_work`, by path and status. It set a floor and no ceiling: it
never said what is *not* registered, never fixed the granularity, and the
tooling checks only that a registered path exists — never that it should.

The result was predictable and happened. Working on `lousydeal`, an agent
registered the slice plan `docs/working/ld-01-foundation.md` **and** the
initiative's resume file `docs/working/status.md`, on top of the already-present
`docs/working/fresh-build.md`. Three entries for one initiative, one of them a
file whose entire purpose is to change every time work progresses.

Nothing pushed back. `tooling/universe validate` reported clean, because every
path existed.

## Considered options

- Leave the rule as it is and treat over-registration as a review matter.
- State the ceiling and the granularity in the standard.
- Add a tooling check that rejects entries by path shape.

## Decision

State the ceiling and the granularity in the standard: one entry per initiative,
never per artifact, and an explicit list of what is not registered — status and
resume files, per-slice plans beneath a registered initiative, ledgers and
journals, decision records and issues.

The operative test is written into the standard: **an entry that would change
because work progressed inside one repository does not belong here.**

## Rationale

The catalogue's job is to answer *"is something under way, and where"*. It is
not a second place to read a repository's progress, and it cannot be one without
becoming a mirror that goes stale — which the same section already forbids for
journals and decision logs, without noticing that a status file is the same
thing under another name.

Leaving it to review was rejected because review is what already passed. The
entries were added by an agent reading the standard carefully and finding no
reason to stop; a reviewer reading the same standard has no ground to object.

A tooling check was rejected as the wrong instrument. The distinction is about
what an entry *means*, not what its path looks like, and a filename check would
be defeated by a rename while adding a rule nobody can read from the standard.
The standard is where a reader and an agent both look, and the audit's blind
spot is now stated in the standard rather than left to be discovered.

The trade-off accepted: this section grew from seven lines to twenty-five, which
the prose budget resists. It buys a rule that does not need re-deriving, and the
growth is mostly a table.

## Consequences

- `lousydeal` keeps one entry, `docs/working/fresh-build.md`. The slice plan and
  the status file are its own business.
- An initiative that spans repositories still gets one entry, not one per
  repository. The entry names the repository that owns the outcome.
- Over-registration stays invisible to `tooling/universe validate`. The standard
  now says so, so a reviewer knows the check does not cover it.
- Registering a *new* initiative is unchanged, and retiring one still updates
  `notable_local_work` in the same change.
