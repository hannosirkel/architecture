# Handoff

The managed universe is governed. Thirteen repositories are catalogued, twelve
are governed, and one is catalogued and deliberately left alone.

Read this to pick the work up. Read `state.yaml` for the record of how it got
here.

## Where everything is

| Question | Answer |
| --- | --- |
| Which repositories exist, and what are they | [`universe/repositories.yaml`](../../../universe/repositories.yaml) |
| How they relate | [`universe/relationships.md`](../../../universe/relationships.md) |
| What rules apply everywhere | [`standards/`](../../../standards/) |
| What a repository type additionally documents | [`profiles.yaml`](../../../profiles.yaml) |
| Why any of it is shaped this way | [`decisions/`](../../../decisions/) |
| How a change is checked | [`tooling/universe`](../../../tooling/universe) |

A repository is governed because it appears in the catalogue. Nothing inside a
repository declares membership, so there is nothing to keep in agreement.

## The three commands

```bash
cd ~/app/architecture

tooling/universe validate                  # the catalogue against itself
tooling/universe audit                     # every repository against the catalogue
tooling/universe sync-baseline <repo>      # regenerate what is generated
```

`audit` reads `origin/<default_branch>`, not the working tree. Fetch first; never
pull on another agent's behalf. It reports and never fixes.

Findings are marked. `fail` is a broken rule. `note` is a differing preference,
reported and passing.

Add `--path <dir>` to either to work against a worktree before pushing it.

## Adding a repository

Three steps. It took under ten minutes for `portfolio-bot`, including writing
its README.

1. Add the entry to `universe/repositories.yaml`.
2. `tooling/universe sync-baseline <name>`.
3. `tooling/universe audit <name>`.

Populate `languages` from evidence, not intent. A declared language with no
files is a check that never runs; a language present and undeclared has no gate
at all.

## How a repository stays current

`architecture` owns the baseline text. Each repository carries it inside
`<!-- BEGIN/END MANAGED ARCHITECTURE BASELINE -->` markers, with no version and
no digest anywhere.

Staleness is a diff: regenerate from `architecture` at HEAD and compare. Same
output means current.

**Never hand-edit inside the markers.** The audit detects it and names the
command that fixes it. `sync-baseline` only ever writes between them; a sweep
across twelve repositories was verified by hashing the content on each side of
the markers before and after, and it was byte-identical every time.

After changing anything under `standards/`, `templates/`, `universe/`,
`profiles.yaml`, or `tooling/`:

```bash
tooling/universe drift --before HEAD~1
```

It names the repositories that change just invalidated. `architecture`'s CI runs
it on every push to `main`.

## Where new work starts

[`standards/work-routing.md`](../../../standards/work-routing.md), and every
repository's own `AGENTS.md` states its answer.

| Situation | Starts in |
| --- | --- |
| Small routine change | the owning repository, branch and PR, no plan |
| Substantial single-repository change | that repository's `docs/working/` |
| One primary repository, light support elsewhere | the primary repository |
| Several peers, or no clear owner | `architecture/initiatives/active/` |

`orange` is the exception: its plans go to the private `orange-inventory`,
because an Orange plan routinely names live hosts and identities.

## What needs you

| Item | Why it is not done |
| --- | --- |
| **Branch-protection floor** on `deploys`, `plepic`, `robobook`, `mihkel`, `ai-portal` | The token gets HTTP 403 on `POST .../rulesets`. The app can read rulesets and not write them; it needs `Administration: write`, or the five go in through the UI. The exact payload and per-repository delta are in `state.yaml` under `branch_protection_floor`. |
| **Renovate dashboards** | Installed. Watch for the Dependency Dashboard issue in each repository — that is the confirmation the shared preset resolved. `architecture` is private and every repository extends a preset from it, so the app must have access to `architecture` or every other config fails silently. First dependency PRs wait for the Monday window by design; security fixes do not. |

## Exceptions, recorded

Two, both in `universe/repositories.yaml`, both with a reason and a decision
link. The audit prints them and does not fail on them, and reports one that
stops matching as stale.

- **`mihkel`, no ESLint gate.** It has no npm project, and adding one means a
  lockfile, 71 packages, and a Renovate stream on a repository holding
  credentialed access, to baseline four findings.
- **`servitium`, no ESLint gate.** `typescript-eslint` declares
  `peerDependencies.typescript ">=4.8.4 <6.1.0"`; `servitium` resolves
  `typescript@7.0.2`. Re-check when that changes; the exception ends there.

**`nomadtty` is catalogued and not governed.** It is a fork of
`shifulegend/nomadtty`, and every file this universe would add is a divergence a
later upstream merge has to reconcile. `sync-baseline` refuses to write into it;
`audit` names it as skipped and never reports it clean. See
[`decisions/007`](../../../decisions/007-nomadtty-is-governed-by-upstream.md).

## Accepted risks

- **Five private repositories cannot carry a ruleset** — `architecture`,
  `orange`, `orange-inventory`, `myskills`, `entpass`, `portfolio-bot` — the
  plan returns 403. The written rule plus the direct-push audit stand in, with
  history baselined per repository so only new violations report.
- **`deploys` takes no pull-request rule.** Its `main` receives automated digest
  pushes from two release workflows.
- **`plepic` and `servitium` keep `pull_request_target`**, pre-authorised
  against `zizmor` in `standards/security.md`.

## Work waiting in the owning repositories

Routed rather than done here, most serious first.

1. **`deploys`: two assertions cannot fail.** In
   `servitium/tests/manifests.sh`, both written `! grep -q …`, which exempts the
   command from `errexit`. One guards against a placeholder digest reaching
   Argo CD. The other guards against the test overlay mounting the **live**
   secret. Verified empirically. Baselined, not fixed, because repairing an
   assertion changes behaviour.
2. **`deploys`: 3,376 lines of undeclared Ruby.** Inside `<<'RUBY'` heredocs in
   the manifest tests. `shellcheck` gates the file and lints 19 lines of 3,246.
   Both defects above live in the part no gate can see. Declaring `ruby` means a
   language standard and a gate; it is a deliberate change, not an oversight to
   quietly fix.
3. **`robobook`: the skill adapters may not resolve their references.**
   `.claude/skills/` and `.opencode/skills/` are symlinks to
   `skills/<name>/SKILL.md` — deliberate, one source of truth. But only
   `SKILL.md` is linked, and every one ends by telling the agent to read
   `references/<name>.md`, relative to the skill directory. Invoke one skill
   through each runtime and watch whether that file is read. Money-sensitive
   logic.
4. **`nomadtty`: releases are blocked.** `docs/issues/mtls-tests-need-openssl-3.5.md`.
   Its `Publish` workflow gates on `CI`, and two mTLS tests use OpenSSL 3.5
   flags the runner lacks. Surfaced by its first-ever CI run.
5. **`mihkel`: `WORKFLOWS.md` contradicts its own baseline** on whether to push
   to `main`. The governance merge did not update it.
6. **`orange`: the documentation never mentions Plepic**, despite it being the
   dominant recent work.
7. **`orange`, `orange-inventory`: `docs/` layout.** Seven current-state
   documents sit at `docs/` root. Reported as advisory, not failed — a
   repository may keep a document where its usage needs it. `orange-inventory`'s
   three are additionally pinned by `scripts/validate`'s `required_paths` and by
   three active working plans that script those paths.
8. **`servitium`: documents three frontend applications and serves four.**
   `/ludus` is missing. Also does not ignore the `public/assets/` build output.
9. **`plepic`: the `Toolchain` note is stale in tense** — the storefront has
   landed.
10. **`architecture`: four Habit Hooks coaching findings** on `tooling/`,
    deliberately not snoozed.
11. **`deploys`: `kubeconform` schema version** is pinned to Kubernetes 1.36.2;
    change it when the cluster changes.
12. **`mihkel` is public** and carries RFC1918 addresses, an internal hostname,
    and a live n8n workflow ID. None is a secret value. Nothing records that the
    exposure was considered and accepted; it deserves a decision either way.

## Starting the AI Portal initiative

Read [`initiatives/planned/ai-portal/README.md`](../../planned/ai-portal/README.md)
first. It records the intended boundary, the owning repository, and the
supporting ones.

Then decide whether it belongs in `architecture` at all. A build owned by one
repository starts in that repository. It belongs here only if the boundaries
between `ai-portal`, `deploys`, `orange`, and `orange-inventory` are genuinely
undecided.

If it does:

```bash
cp -r templates/initiative initiatives/active/ai-portal
# write initiatives/active/ai-portal.md as the contract
```

`ai-portal` currently holds three governance files and a CI workflow. It has no
product and no scaffolding, deliberately.

## One thing that will bite

**The audit reads the branch; your checkout is not the branch.**

Three cold tests each opened one repository with a clean `git status` and found
themselves several commits behind, with the governance layer invisible. All
three named it as the highest-impact problem they hit, and no mechanical check
would have caught it — the audit was right while the workstation was wrong.

Before reading a repository's instructions:

```bash
git -C ~/app/<repo> fetch origin && git -C ~/app/<repo> status -sb
```
