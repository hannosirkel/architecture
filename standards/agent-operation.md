# Agent operation standard

Work in an isolated worktree. Never commit to a default branch. One writer per
worktree. Never touch another agent's state.

These four rules cover almost every way a multi-agent workspace breaks.

## Worktrees

Isolate any non-trivial change in a Git worktree. This applies to every agent
and every harness, whatever default location the harness would otherwise pick.

**Worktrees live outside every repository, at `~/app/.worktrees/<repo>/<task>`.**

```bash
git -C ~/app/<repo> fetch origin
git -C ~/app/<repo> worktree add ~/app/.worktrees/<repo>/<task> -b <branch> origin/main
```

Branch from the remote default branch, not from whatever the primary checkout
has checked out. Another agent may be working there.

An in-repo worktree is a second copy of the tree. Every tree-walking tool then
needs to be taught to skip it, once per tool per location, and a stray copy of a
source directory becomes a lint and publication hazard. Outside the repository
there is nothing to exclude, and `git worktree list` still finds it.

Do not use `/tmp`, which is lost on reboot. Do not use a harness-specific
default such as `.claude/worktrees/`.

A fresh worktree holds only tracked files. It is not usable until the ignored
local state is present. The repository's own `AGENTS.md` states what that is.

Remove a worktree with `git worktree remove` once its branch is merged or
abandoned. Never delete or reset a worktree you did not create.

## Branches and commits

Agents never commit to a default branch. Branch, open a pull request, and
self-merge only where policy allows.

One exception exists, and only one: an empty repository needs an initial commit
before a branch can exist. Push it directly, then work by branch from the next
commit onward.

The audit whitelists that case and nothing else.

**Durable initiative state under `initiatives/*/` in `architecture` used to be a
second exception**, on the reasoning that a coordination record is not a code
change and gating it behind review would stall the resume path it protects. It
was withdrawn on 2026-08-23, because it never worked: `architecture`'s
`required_status_checks` rule rejects a push whose commit has no checks yet, so
every direct push had been failing since the ruleset was applied while three
documents said otherwise. Initiative state now goes through a pull request like
everything else. See
[`decisions/009`](../decisions/009-architecture-is-pull-request-only.md).

The resume path is preserved a different way: `architecture` requires **zero**
approving reviews, so an agent opens a pull request and merges it once the
checks pass, without waiting for a human. What it cannot do is push to `main`
with nothing having verified the change.

Five private repositories cannot enforce this through a ruleset. The GitHub plan
does not offer rulesets on a private repository. There the rule is the
enforcement, and the audit checks it against commit metadata.

## Multi-agent safety

- Never write into a dirty or shared worktree.
- Never stash, reset, clean, rebase, amend, or force-push another agent's work.
- Never switch another session's branch or delete its state.
- Never change a repository's checked-out branch or HEAD, including an empty,
  unborn, or detached one.
- Keep deployment, DNS, credential, and other stateful changes under one
  coordinating agent.
- Read an active work record without editing it, unless its owner joins the
  work.

## Working across repositories

Some changes span two repositories. When they do:

1. Prepare and validate the compatible change in both.
2. Push the repository that supplies the interface first.
3. Then push the repository that consumes it.

A commit that depends on an unpublished interface breaks the checkout for
everyone else.

Register a cross-repository initiative in `architecture`. See
[`work-routing.md`](./work-routing.md).

## Subagent delegation

Delegate bounded work that can be verified independently. The primary agent
keeps responsibility for architecture, integration, security decisions, and
final verification.

Use the model tier that matches the job:

| Tier | OpenAI | Anthropic | Use for |
| --- | --- | --- | --- |
| top | Sol | Fable | source-of-truth conflicts, security policy, final review |
| mid | Terra | Opus | orchestration, integration, judgment |
| low | Luna | Sonnet | bounded execution, inventory, mechanical edits |

Resolve a tier to whatever the running runtime exposes. If a named model is
unavailable, substitute within the same tier and record it. Never drop a review
step to a lower tier silently. If only a lower tier is available, record it as
an open item for the operator.

### Good tasks to delegate

- Repository reconnaissance and inventory.
- Locating files, configuration keys, call sites, and existing tests.
- Investigating one isolated component.
- Implementing a small, specified change inside an established design.
- Writing tests for explicitly defined behaviour.
- Running checks and summarising the result.
- Reviewing a bounded diff.

Parallelise delegated tasks that are genuinely independent, do not edit the same
files, and do not depend on each other's conclusions.

### Tasks the primary agent keeps

- Architecture and cross-component design.
- Security, authentication, secrets, and recovery decisions.
- Resolving ambiguous or conflicting requirements.
- Migration ordering, compatibility, and rollback.
- Deciding whether a test or requirement may be weakened.
- Final review and completion verification.

A subagent may investigate these. Its conclusions are advisory.

### How to instruct a subagent

Every delegation is self-contained and states:

1. **Objective** — one concrete outcome.
2. **Scope** — exact repositories, files, and allowed paths.
3. **Authority** — read-only, may edit named files, or may run checks.
4. **Constraints** — what must not change, and what it must not do.
5. **Acceptance criteria** — observable conditions for success.
6. **Verification** — the commands it must run.
7. **Deliverable** — the expected summary, patch, or evidence.
8. **Unknowns** — require it to report uncertainty rather than guess.

Use the smallest scope that still gives meaningful independent work.

Subagents do not commit, push, rotate credentials, change DNS, or deploy unless
explicitly authorised. Subagents never own durable state; the orchestrator
records their assignments and results.

## Skills

Use a relevant skill when one exists. Reusable executable skills live in
`myskills`. `architecture` pins approved skill versions and owns one skill of
its own, the universe audit. See
[`repository-contract.md`](./repository-contract.md).
