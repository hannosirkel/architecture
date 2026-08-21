# 001. Govern the universe from a separate private repository

- **Date:** 2026-08-21
- **Status:** accepted

## Context and problem statement

Twelve repositories share engineering rules, and every one of them held its own
copy. Three carried a near-identical documentation standard. The worktree rule
appeared twice in one file with two different answers. Nothing owned the map.

## Considered options

- A governance repository that owns policy and the catalogue.
- A parent repository or submodule tree containing the governed repositories.
- No central home; keep copying rules and accept the drift.

## Decision

Use a separate private repository, `architecture`, that owns only universe-wide
concerns: the catalogue, cross-repository standards, profiles, cross-repository
decisions, shared templates, conformance tooling, and durable state for
cross-repository initiatives.

## Rationale

The governing rule is that each fact has one authoritative home. `architecture`
owns the map and shared policy; each implementation repository owns its code,
its local architecture, its decisions, and its operating truth.

A submodule tree was rejected. It couples checkouts, breaks independent
branching, and makes every governed repository's history a function of the
governance repository's. Ownership of policy does not require ownership of the
trees.

Doing nothing was rejected on evidence: three copies of one standard had already
drifted, and the single-file worktree contradiction shows the copies were not
being read against each other.

## Consequences

- An agent working in one repository must still be able to work from that
  repository alone. That is why the baseline is materialised into `AGENTS.md`
  rather than replaced by a pointer.
- A policy change now has one place to make and a generator to propagate it.
- `architecture` is private, and private does not mean it may hold secrets.
- `architecture` is governed by the rules it defines. It is in its own
  catalogue.
