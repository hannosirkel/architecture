# 005. Keep the universe audit skill in `architecture`

- **Date:** 2026-08-21
- **Status:** accepted

## Context and problem statement

A conformance pass proves the universe was true once. Nothing keeps it true
afterwards. The audit therefore has to exist as a first-class deliverable, and
it has to live somewhere.

[003](./003-myskills-remains-separate.md) says reusable skills live in
`myskills`.

## Considered options

- Put the audit skill in `myskills`, with the rest of the skills.
- Put it in `architecture`, as a named exception.
- Have no skill; run the CLI directly.

## Decision

The audit skill lives in `architecture/skills/audit-universe/`, as a thin
wrapper over `tooling/universe`. It is the only skill `architecture` owns.

## Rationale

The audit is inseparable from the catalogue, the profiles, and the standards it
audits. Housing it in `myskills` would split one behaviour across two
repositories and force a version bump there for every standards edit here.

It is not reusable beyond this universe, which is the test `myskills` membership
actually applies.

The exception is narrow and does not open a general skills tree in
`architecture`. Anything reusable beyond this universe still belongs in
`myskills`.

## Consequences

- The skill is invoked explicitly by the operator. There is no scheduler, cron,
  daemon, or watcher. One owner running one command when they want the answer
  needs no automation around it.
- Part of the audit runs in `architecture`'s own CI on every push to `main`:
  catalogue validity, link checking, layout, and a regeneration of every
  repository's expected `AGENTS.md` section at the parent and at the head, to
  report which repositories the change just invalidated. That comparison is
  between two generated outputs, so it needs no clones and no token.
- **Do not filter that CI job by path.** The generated section depends on the
  standards, the catalogue, the templates, `profiles.yaml`, and the generator
  itself. A path filter goes blind exactly where breakage is most likely.
- The audit reports; it does not fix. Every fix it implies is ordinary work.
- Scheduling the full audit later is a workflow with a cron. Do not build it
  now, and do not build a dashboard for it ever.
