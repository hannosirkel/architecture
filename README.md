# architecture

Engineering governance for the managed universe. This repository owns the map
and the shared policy. Each implementation repository owns its code, its local
architecture, its decisions, and its operating truth.

Private. Private does not mean it may hold a secret.

## What it owns

- [`universe/repositories.yaml`](./universe/repositories.yaml) — the catalogue.
  A repository is governed because it appears here.
- [`universe/relationships.md`](./universe/relationships.md) — how the
  repositories relate.
- [`standards/`](./standards/) — cross-repository policy.
- [`profiles.yaml`](./profiles.yaml) — what each repository type additionally
  documents.
- [`templates/`](./templates/) — the generated agent baseline, the `CLAUDE.md`
  pointer, the decision record, the shared Renovate preset, and the initiative
  layout.
- [`decisions/`](./decisions/) — why this repository is shaped as it is.
- [`initiatives/`](./initiatives/) — cross-repository work and its durable
  state.
- [`tooling/universe`](./tooling/universe) — validation, audit, and baseline
  synchronization.
- [`skills/audit-universe/`](./skills/audit-universe/) — the one skill this
  repository owns.

## What it does not own

- Application source, of any repository.
- Deployment state. That is `deploys`.
- Live infrastructure variables or inventory. That is `orange-inventory`.
- Credentials, tokens, keys, or session material. Those live in OpenBao or in an
  ignored local directory, never in a repository.
- Reusable agent skills. Those live in `myskills`. The universe audit is the
  single named exception; see
  [decision 005](./decisions/005-audit-skill-lives-in-architecture.md).
- The governed repositories themselves. This is not a parent repository, a
  monorepo, or a submodule tree.

## Getting the picture

```bash
tooling/universe validate     # the catalogue against itself
tooling/universe audit        # every repository against the catalogue
```

The audit reports. It never fixes. Every fix it implies is ordinary work in the
owning repository, routed by
[`standards/work-routing.md`](./standards/work-routing.md).

## Developing and testing

```bash
python3 -m unittest discover -s tooling -p 'test_*.py'
ruff check .
```

The tests need `pyyaml` and `git`. Nothing else.

Documentation checks run in CI:

```bash
markdownlint-cli2 "**/*.md"
lychee --offline .
```

## Where things live

| Question | Answer |
| --- | --- |
| How do I work in a repository? | that repository's `AGENTS.md` |
| What rules apply everywhere? | [`standards/`](./standards/) |
| Which repositories exist? | [`universe/repositories.yaml`](./universe/repositories.yaml) |
| Where does a new change start? | [`standards/work-routing.md`](./standards/work-routing.md) |
| Why is it like this? | [`decisions/`](./decisions/) |

## Adding a repository

```bash
# 1. add the entry to universe/repositories.yaml
tooling/universe validate
tooling/universe sync-baseline <name>
tooling/universe audit <name>
```

Deliberately cheap.
