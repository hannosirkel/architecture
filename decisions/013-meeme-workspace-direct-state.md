# 013. Let Meeme persist declared workspace state directly

- **Date:** 2026-09-04
- **Status:** accepted

## Context and problem statement

Meeme uses its repository as the durable source for identity, instructions,
memory, and other OpenClaw workspace state. Requiring a pull request after each
session makes routine persistence depend on a review workflow. Giving the bot a
broad default-branch exception would also let it change CI, hooks, dependencies,
or unrelated repository content without review.

## Considered options

- Require a pull request for every workspace-state update.
- Permit direct pushes only for declared workspace-state paths.
- Permit the bot to push any repository path directly.

## Decision

Permit direct pushes only for `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`,
`HEARTBEAT.md`, `MEMORY.md`, `memory/`, and `experiments/`. Treat a file entry
as an exact path. Treat an entry with a trailing slash as a directory prefix.

Use branches and pull requests for every other path, including `AGENTS.md`.
Keep the repository private and secret-free.

## Rationale

The narrow allowlist keeps persistence reliable without granting routine access
to CI, hooks, dependency configuration, or the repository contract. A mixed
commit fails when one changed path is outside the allowlist, so an allowed file
cannot carry an unrelated change through the exception.

Requiring pull requests for all state was rejected because it makes normal
memory persistence fragile. A repository-wide exception was rejected because
it removes review from executable and governance changes.

## Consequences

- Meeme can persist its own identity and memory after a session.
- The pre-push hook and universe audit must enforce the same path boundary.
- Changes outside the allowlist continue through branches and pull requests.
