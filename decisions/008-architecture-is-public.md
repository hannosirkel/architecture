# 008. Publish the architecture repository

- **Date:** 2026-08-22
- **Status:** accepted

## Context and problem statement

[`001`](./001-architecture-repository-role.md) put the catalogue, the standards
and the conformance tooling in a private repository, and said in the same breath
that private does not mean it may hold secrets. Once twelve repositories were
generating their `AGENTS.md` baselines from it, being private stopped being
neutral and started costing three specific things, each observed rather than
predicted:

- **Agents could not read the rules they are held to.** All three cold-test
  agents named this independently, from three unrelated repositories. One
  reconstructed the enforceable subset from `scripts/validate`, the CI workflow
  and a local ADR, and called it reverse-engineering rather than reading.
- **Link rot in the standards was invisible.** Every governed repository's
  `lychee.toml` excluded `hannosirkel/architecture`, because an anonymous
  checker returns 404 for a private repository that exists. The exclusion was
  correct and it meant the fourteen most load-bearing links in the universe were
  the only ones never checked.
- **Renovate could not resolve the shared preset.** A `local>` preset is fetched
  with the installation token, and GitHub does not let a public repository
  extend a preset held in a private one. Six repositories stopped receiving
  updates with `Cannot find preset's package`.

## Considered options

- Keep it private and accept all three costs.
- Keep it private and duplicate the standards into each governed repository.
- Publish it.

## Decision

Publish `architecture`.

## Rationale

The second option is the drift that `001` exists to prevent. Three copies of one
standard had already diverged before this initiative started; deliberately
recreating twelve copies to work around a visibility setting trades the whole
value of the governance layer for it.

The first option was tenable while `architecture` held only the operator's own
tooling. It stopped being tenable once its content became the thing every agent
in the universe is told to obey.

Publishing costs nothing that `001` had not already committed to: the repository
was written under `public_safe_required` from the start, so nothing in it was
ever allowed to depend on being unreadable.

**Verified before publishing, not after:** gitleaks across all 44 commits of
history, and a manual read for the things gitleaks does not model — RFC1918
addresses, home directory paths, hostnames, and personal identifiers. None
present.

## Consequences

- The standards are readable by any agent, and by anyone reviewing a governed
  repository's pull request.
- The `architecture` exclusion leaves every governed `lychee.toml`, so the
  standards links are checked for real. The five genuinely private repositories
  stay excluded.
- The `local>` Renovate preset resolves, and the six broken repositories
  onboarded.
- `architecture` can carry a branch-protection ruleset, which this plan does not
  offer on private repositories. It takes `deletion`, `non_fast_forward` and
  `required_status_checks`, without a pull-request rule: initiative state is
  committed directly to `main` by the session doing the work.
- Public safety is now enforced by reality rather than by rule. The catalogue
  already fails validation for a repository declared public with
  `public_safe_required: false`, so the guarantee cannot be quietly dropped.
- The `governance-private` profile became a misnomer and is now `governance`.
