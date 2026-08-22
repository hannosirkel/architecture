# AGENTS.md

<!-- BEGIN MANAGED ARCHITECTURE BASELINE -->
<!-- Generated from hannosirkel/architecture. Do not edit inside these markers.
     Regenerate with: tooling/universe sync-baseline architecture -->

Governed by [`architecture`](https://github.com/hannosirkel/architecture).

| | |
| --- | --- |
| Profile | `governance-private` |
| Visibility | declared private, currently private |
| Languages | python |

**Standards that apply here.** Read a standard before you change something it
governs. They live in a private repository: if a link does not open for you, the
rules stated below and this repository's CI are what bind.

- [Agent operation](https://github.com/hannosirkel/architecture/blob/main/standards/agent-operation.md) — worktrees, branches, multi-agent safety, delegation
- [Security](https://github.com/hannosirkel/architecture/blob/main/standards/security.md) — secrets, public and private boundaries, workflow hardening
- [Code quality](https://github.com/hannosirkel/architecture/blob/main/standards/code-quality.md) — gates, coaching, testing, review cutoff
- [Repository contract](https://github.com/hannosirkel/architecture/blob/main/standards/repository-contract.md) — required files, profiles, skills
- [Work routing](https://github.com/hannosirkel/architecture/blob/main/standards/work-routing.md) — where a change starts, and where a working plan belongs
- Language standards: [python](https://github.com/hannosirkel/architecture/blob/main/standards/languages/python.md)

**Never commit to a default branch.** Work in `~/app/.worktrees/architecture/<task>`.
Branch from `origin/main`. Open a pull request.

**A working plan for this repository goes in `docs/working/`.** A change
spanning several repositories with no clear owner starts in `architecture`
instead.

**This repository is private, which is not the same as secret.** Never commit a password, token, key, kubeconfig,
rendered Secret, or live export. No repository in this universe holds a secret
value, and a private one is no exception.

**Run `habit-hooks` before declaring an edit done.** If it is not on `PATH`:

```bash
uv tool install "habit-hooks[python,typescript]"
```

That command names every language plugin **this universe** uses, not this
repository's. Install it whole: a later install naming fewer extras silently
removes the rest.

<!-- END MANAGED ARCHITECTURE BASELINE -->

## What this repository is

Engineering governance for the managed universe. It owns the catalogue, the
shared standards, the profiles, the templates, cross-repository decisions,
cross-repository initiative state, and the conformance tooling.

It owns no application source, no deployment state, no inventory, and no
secrets. See [`README.md`](./README.md) for the full boundary.

## Commands

```bash
python3 -m unittest discover -s tooling -p 'test_*.py'   # before every handoff
ruff check .

tooling/universe validate                     # the catalogue against itself
tooling/universe audit [repo ...]             # conformance; reports, never fixes
tooling/universe sync-baseline <repo> [--path DIR]
tooling/universe drift --before <ref>         # what a change here invalidates
```

Use `--path` when the target repository is checked out in a worktree rather than
at its catalogued `local_path`.

## Rules specific to this repository

- **Edit a standard, then check what it broke.** Run
  `tooling/universe drift --before HEAD~1` after changing anything under
  `standards/`, `templates/`, `universe/`, `profiles.yaml`, or `tooling/`.
  Every generated section depends on all five.
- **A standard exists only if a generated `AGENTS.md` section links it**, or it
  is marked `owner_facing` in `standards/index.yaml` and linked below. A
  document nothing links is a document nothing reads. `tooling/universe
  validate` enforces this.
- **Durable initiative state under `initiatives/*/` commits to `main`
  directly.** It is a coordination record, not a code change, and gating it
  behind review would stall the resume path it protects. Everything else here
  goes through a pull request.
- **This repository is governed by the rules it defines.** It is in its own
  catalogue and the audit checks it.
- **Never store a secret here.** Private is not secret.
- Write to [`standards/documentation.md`](./standards/documentation.md).
  It governs itself.

## Owner-facing standards

Read these here. They are marked `owner_facing` in `standards/index.yaml` and
are linked from no generated section, because pushing an owner-facing link into
eleven baselines would inflate the file the budget keeps short.

- [`standards/documentation.md`](./standards/documentation.md) — layout,
  structure, wording, and the `AGENTS.md` budget.
- [`standards/work-routing.md`](./standards/work-routing.md) — where a change
  starts.

`standards/gitops-and-deployment.md` is **not** owner-facing. `deploys` and the
two repositories that promote digests into it link it from their generated
sections, because that is where the agent that needs it reads.

## Where work goes

A change that spans several peer repositories starts in
`initiatives/active/`. Anything owned by one repository starts there instead.
See [`standards/work-routing.md`](./standards/work-routing.md).
