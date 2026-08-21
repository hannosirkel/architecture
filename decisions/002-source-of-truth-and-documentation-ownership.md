# 002. Centralize policy, not repository truth

- **Date:** 2026-08-21
- **Status:** accepted

## Context and problem statement

Once a governance repository exists, the tempting failure is to move everything
into it. The opposite failure is to leave local instructions so thin that an
agent opening one repository cannot work.

## Considered options

- Move all documentation to `architecture` and leave pointers behind.
- Leave everything local and centralize nothing.
- Centralize policy; keep repository truth local; generate a managed baseline.

## Decision

Centralize a document only when it genuinely governs several repositories or the
universe as a whole. Keep repository-specific current truth, decisions,
operational runbooks, and active work in the owning repository.

Materialise a small managed section into each `AGENTS.md`, between markers,
generated from `architecture`.

## Rationale

Agents frequently open only one repository. Local instructions must stay
operationally sufficient, so "read the architecture repository" is not an
acceptable local instruction.

The distinction that works in practice is *policy* against *truth*. How a
repository must be worked on is policy and centralizes. How a particular
application behaves is truth and stays local.

Controlled duplication is allowed. A generated managed section is fine because
it cannot drift silently. A manually copied six-page standard is not.

Staleness is a diff, not a version number: regenerate the expected section from
`architecture` at HEAD and compare. Storing a digest in each repository would be
a second copy of a fact the generator already knows.

## Consequences

- Cross-repository moves lose ordinary Git file history. Provenance is recorded
  in the initiative's migration map instead.
- Every repository gains one generated region that must never be hand-edited.
  The audit detects a hand-edit and names the regeneration command.
- Symlinks, absolute local paths, and submodules are not used to share
  instructions.
- A standard nothing links is a standard nothing reads. No standard exists
  unless some generated `AGENTS.md` section links it.
