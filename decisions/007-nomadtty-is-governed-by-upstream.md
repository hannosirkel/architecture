# 007. Catalogue `nomadtty`, but do not govern it

- **Date:** 2026-08-22
- **Status:** accepted

## Context and problem statement

`nomadtty` is a maintained fork of
[shifulegend/nomadtty](https://github.com/shifulegend/nomadtty). Everything else
in this universe is code written here. This is not.

The bootstrap first treated it as an ordinary public application repository. It
prepared a full conformance change: a generated `AGENTS.md` section, a
`CLAUDE.md` pointer, `.habit-hooks/config.toml`, `renovate.json`, seven actions
pinned to commit SHAs, and least-privilege `permissions:` blocks. It also
consolidated four rival instruction systems into one.

That work was correct against the contract. It was wrong for a fork.

## Considered options

- **Govern it fully.** Apply the baseline, and record the added files in delta
  documentation so a future upstream merge reads them as intentional.
- **Catalogue it, do not govern it.** Record what the repository is and what it
  must not hold; leave its conventions to upstream.
- **Remove it from the catalogue.** A repository outside the catalogue is out of
  scope by construction.

## Decision

Catalogue it, do not govern it.

`universe/repositories.yaml` keeps the entry, with `governed: false` and the
profile `fork-upstream-governed`, whose `conformance: none` makes the tooling
skip it. `sync-baseline` refuses to write into it. `audit` names it as skipped
rather than reporting it clean.

## Rationale

Every governance file this universe would add is a **divergence a future
upstream merge has to reconcile**, in a repository whose conventions are
upstream's to set. The universe holds as few divergences from upstream as it
can, because each one is a merge conflict waiting for whoever pulls the next
upstream fix.

The value the governance layer buys elsewhere does not apply here. It exists to
stop twelve repositories drifting from each other. A fork is *meant* to track
something outside the universe; measuring it against the universe's conventions
measures the wrong thing.

Removing the entry entirely was rejected. Membership is what makes a repository
known, and the ownership facts are worth recording: `nomadtty` is public, it
must not hold Orange credentials or private host details, and it exists. A
repository nobody has written down is a repository nobody checks before putting
something in it.

## Consequences

- The conformance tooling skips it. `audit` prints
  `nomadtty: not governed; conformance skipped`, never `clean`. A silent pass
  for an unaudited repository is the placebo this tooling exists to avoid.
- Two prepared pull requests were closed unmerged: the wave 0 workflow hardening
  and the wave 1 instruction consolidation. Its four instruction systems, its
  unpinned actions, and its missing `permissions:` blocks all remain. Those are
  now upstream's concerns, or a separate deliberate decision here.
- The `fork-public` profile is gone. It had one member and now describes
  nothing this universe does.
- The boundary in the catalogue entry still binds. It is an ownership fact, not
  a governance mechanic.
- A finding this initiative surfaced in `nomadtty` stands on its own merits:
  `docs/issues/mtls-tests-need-openssl-3.5.md`. Its `Publish` workflow gates on
  `CI`, so releases are blocked until it is fixed.
- If a second fork joins later, this profile is ready and the decision is made.
