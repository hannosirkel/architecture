# Repository contract

Every governed repository carries three files, a profile, and a declared
language set. Everything else follows from those.

## Required everywhere

```text
README.md
AGENTS.md
CLAUDE.md
```

`AGENTS.md` holds the rules. `CLAUDE.md` is a pointer to it and nothing else —
the same generated content everywhere, never a place where a rule lives.

Both are required whatever a given agent runtime reads natively. The cost is one
small generated file per repository, and it removes the question: Codex and
Claude Code cannot end up with different rules, because there is one set of
rules in one file.

**There is no local governance marker file.** Profile, declared visibility,
public-safety requirement, languages, and description live in
[`universe/repositories.yaml`](../universe/repositories.yaml) and are
materialised into `AGENTS.md` by the sync tool. The agent learns all of it in the
file it already opens first.

## Membership

A repository is governed because it appears in `universe/repositories.yaml`.
Membership does not depend on any file inside the repository.

A repository outside the catalogue is out of scope by construction. Do not
catalogue it, audit it, add files to it, or report it as a conformance failure.
Archived, legacy, and personal repositories under the same account are outside.
The account listing is not the universe.

## `languages`

`languages` is the load-bearing field. It is the set of languages the repository
actually contains. It determines:

- which language standards the generated `AGENTS.md` section links;
- which linters gate its CI;
- which Habit Hooks plugins its coaching instruction names.

Permitted values: `typescript`, `python`, `ansible`, `shell`. The list may be
empty.

Populate it from evidence, not expectation. A language listed but absent creates
checks that never run. A language present but undeclared has no gate at all.

The languageless `generic` coaching plugin applies to every repository. It is
never declared.

## `README.md`

State clearly:

- what the repository owns;
- what it does not own;
- intended visibility and public-safety status;
- how to develop and test it;
- how it is built and deployed, when that applies;
- where repository-local architecture and decisions live;
- where cross-repository standards and initiatives live.

## `AGENTS.md`

Every `AGENTS.md` has:

1. A generated managed section, between the markers below.
2. Repository purpose and boundaries.
3. Exact test and check commands, or reliable discovery instructions.
4. Public/private and secret-handling constraints for this repository.
5. Rules for plans, worktrees, commits, and changes to adjacent repositories.
6. Any local exception to a central standard, linked to an explicit decision.
7. Links to the language standards that apply, generated from `languages`.

Keep it short. [`documentation.md`](./documentation.md) sets the budget.

### The managed section

```text
<!-- BEGIN MANAGED ARCHITECTURE BASELINE -->
...
<!-- END MANAGED ARCHITECTURE BASELINE -->
```

The sync tool changes only the region between the markers. It refuses malformed,
missing, nested, or duplicated markers.

**One authority, and nothing stored twice.** `architecture` owns the baseline
text. The managed section carries no digest and no version number, and the
repository records neither.

Staleness is a diff. Regenerate the expected section from `architecture` at HEAD
and compare it to what is in the file. Same output means current; different
output means stale. There is no third state to get wrong.

If pinning a repository to an older baseline ever becomes necessary, add a
version marker then. It is not needed while every repository tracks HEAD.

## Profiles

A profile says what a repository additionally documents. It is data in
[`profiles.yaml`](../profiles.yaml), not a directory tree.

Different repository types need different local structures. Do not require a
repository to hold an empty copy of a directory it has no content for.

| Profile | Additionally documents |
| --- | --- |
| `governance-private` | catalogue, standards, profiles, cross-repository initiatives, conformance tooling |
| `platform-public-ready` | current state, decisions, recovery and provisioning |
| `inventory-private` | environment operations, recovery evidence, local working plans |
| `gitops-public` | deployment ownership, promotion and rollback, validation commands, public-secret constraints |
| `skills-private` | skill catalogue, tests, installation, security boundaries |
| `application-public` | local architecture and current state, decisions, optional working plans |
| `fork-public` | everything `application-public` does, plus upstream provenance, licence obligations, and the local delta |
| `research-private` | nothing beyond the baseline |

`fork-public` is not a reduced tier. It carries the same governance files and
code-quality gates as any public application repository. It differs only in what
it *additionally* documents.

## Checks and hooks

Central policy defines the expected outcome. The repository enforces it through
the lightest mechanism it already has.

Prefer, in this order:

```text
fast optional local checks
+ authoritative CI checks
+ repository rules where the plan allows them
```

Do not rely on a Git hook alone. Do not introduce a new hook framework
everywhere for visual uniformity.

Determine profile-appropriate handling for:

- secret scanning;
- the formatting and linting the repository already uses;
- behaviour-based tests;
- documentation and link validation;
- repository conformance validation;
- public/private boundary checks;
- container and dependency scanning, where the repository builds a deployable
  artifact;
- manifest validation, for GitOps and infrastructure repositories.

Record a justified profile exception rather than leaving a silent gap. An empty
configuration is not an exception.

## Skills governance

Reusable executable skills live in `myskills`. `architecture` defines approved
intent and pins skill versions in an initiative's `skills.lock.yaml`.

`architecture` owns exactly one skill, `skills/audit-universe/`, because it is
inseparable from the catalogue, profiles, and standards it audits. Housing it in
`myskills` would split one behaviour across two repositories and force a version
bump there for every standards edit here. That exception does not open a general
skills tree.

Before creating a skill:

1. Inventory the existing skills.
2. Map the need to an existing skill.
3. Reuse or compose where one fits.
4. Create only a missing *reusable* capability.
5. Test its behaviour and its safety boundaries.
6. Commit it in an isolated `myskills` worktree.
7. Record the exact commit in `skills.lock.yaml`.
8. Reload skills before relying on a new one.

Treat a skill change as an executable-behaviour change. It needs tests and
review.

A skill never widens permissions silently, modifies an unrelated repository,
rewrites history, or bypasses an operator gate.

Do not create a one-off skill for a single initiative. Keep initiative-specific
orchestration in the initiative. Promote only a reusable procedure.

## Adding a repository

Three steps:

1. Add the entry to `universe/repositories.yaml`.
2. Run `tooling/universe sync-baseline <repo>`.
3. Run `tooling/universe audit <repo>`.

Adding a repository is deliberately cheap.
