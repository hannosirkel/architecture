# Resolved plan — managed-universe bootstrap

**Status: awaiting Gate 1 approval.** Nothing has been written to a governed
repository. Only this initiative's own state exists.

## The answer first

Twelve repositories are catalogued. Ten already carry agent instructions; three
of those carry near-identical copies of the same documentation standard, and one
carries four rival instruction systems. Two repositories have no governance
files at all, and one is empty.

The plan centralizes eight bodies of duplicated text into seven standards plus
four language documents, generates a managed section into every `AGENTS.md`, and
lands the security and code-quality controls in three waves: five defect-catching
controls first, governance conformance second, gates third.

Three findings change the contract's own assumptions. Each is recorded, not
worked around:

1. **A `generic`-only Habit Hooks config scans nothing and prints a green tick.**
   The generator must emit an explicit `files` list. See
   `evidence/habit-hooks-verification.md`.
2. **`deploys` is not languageless.** It has three bash files carrying the
   manifest contract assertions.
3. **`deploys` cannot take a pull-request rule.** Its `main` receives automated
   digest pushes from two release workflows.

## 1. Repository catalogue

The full catalogue is `repositories.yaml`. Summary:

| Repository | Profile | Declared | Actual | Languages | Rulesets |
| --- | --- | --- | --- | --- | --- |
| architecture | `governance-private` | private | private | python | no |
| orange | `platform-public-ready` | public | **private** | ansible, python, shell | no |
| orange-inventory | `inventory-private` | private | private | ansible, shell | no |
| deploys | `gitops-public` | public | public | shell | yes |
| myskills | `skills-private` | private | private | shell | no |
| plepic | `application-public` | public | public | typescript, shell | yes |
| robobook | `application-public` | public | public | python | yes |
| servitium | `application-public` | public | public | typescript, shell | yes |
| nomadtty | `fork-public` | public | public | typescript, shell | yes |
| mihkel | `application-public` | public | public | typescript, python, shell | yes |
| ai-portal | `application-public` | public | public | none | yes |
| entpass | `research-private` | private | private | none | no |

One visibility mismatch: `orange` is declared public and is currently private.
§9.2 forbids changing it here. It is recorded, not acted on.

Rulesets are unavailable on all five private repositories. The GitHub API
returns HTTP 403 with *"Upgrade to GitHub Pro or make this repository public"*.
That is a named accepted risk, not a gap (§4 of the security baseline below).

Language evidence: `evidence/language-evidence.md`.

## 2. Profiles

Profiles are data in `profiles.yaml`, not directories (§5.9).

| Profile | Repositories | Adds beyond the baseline |
| --- | --- | --- |
| `governance-private` | architecture | catalogue, standards, profiles, initiatives, tooling, audit skill |
| `platform-public-ready` | orange | `docs/current/`, `docs/decisions/`, recovery and provisioning docs, publication gate |
| `inventory-private` | orange-inventory | environment operations, recovery evidence, `docs/working/` |
| `gitops-public` | deploys | promotion and rollback rules, manifest validation, public-secret constraints |
| `skills-private` | myskills | skill catalogue, skill tests, install procedure, security boundaries |
| `application-public` | plepic, servitium, mihkel, robobook, ai-portal | local architecture docs, ADRs, optional `docs/working/` |
| `fork-public` | nomadtty | upstream provenance, licence obligations, delta documentation, update process |
| `research-private` | entpass | nothing; baseline only, no deployable-application conventions |

`fork-public` is `application-public` plus three documents. It is not a reduced
tier (§5.5).

## 3. Source-of-truth matrix

| Subject | Authority | Local form |
| --- | --- | --- |
| Repository membership, profile, visibility, languages | `universe/repositories.yaml` | generated `AGENTS.md` section |
| Worktree rules, multi-agent safety, subagent delegation | `standards/agent-operation.md` | managed section plus local exceptions |
| Documentation layout and semantics | `standards/documentation.md` | link |
| Where work starts | `standards/work-routing.md` | link |
| Secret handling, public/private boundaries, workflow hardening | `standards/security.md` | managed section plus local constraints |
| Promotion, rollback, secrets delivery | `standards/gitops-and-deployment.md` | link, from deploys and the two publishers |
| Testing expectations, review cutoff, gates and coaching | `standards/code-quality.md` | link |
| Linters and coaching per language | `standards/languages/*.md` | generated links from `languages` |
| Repository contract and skills governance | `standards/repository-contract.md` | link |
| How a given application works | the repository | `README.md`, `docs/current/` |
| Local decisions | the repository | `docs/decisions/` |
| Live private variables and inventory | orange-inventory | — |
| Deployable desired state | deploys | — |
| Reusable executable skills | myskills | — |
| Active initiative state | the owning repository, or `architecture/initiatives/` | — |

## 4. Standards to write

Seven standards plus four language documents, as §6 specifies. Written in this
order, because each later one obeys the earlier:

1. `standards/documentation.md` — written first (§13 Phase 2 step 1).
2. `standards/repository-contract.md`
3. `standards/agent-operation.md`
4. `standards/security.md`
5. `standards/work-routing.md`
6. `standards/code-quality.md`
7. `standards/gitops-and-deployment.md`
8. `standards/languages/{typescript,python,ansible,shell}.md`

Every one of them has a named consumer: a generated `AGENTS.md` section links
it, or `architecture`'s own section does for the owner-facing two (§6).

### What each language standard defines

| Language | Formatter | Linter | Static analysis | CI gate | Baseline mechanism | Habit Hooks plugin |
| --- | --- | --- | --- | --- | --- | --- |
| typescript | `prettier`, changed files only | `eslint` | `tsc --noEmit` | existing `scripts/validate` | ESLint bulk suppressions | `typescript` |
| python | `ruff format`, changed files only | `ruff check` | `ruff` rule set | existing validate script or a new job | `ruff --add-noqa` | `python` |
| ansible | — | `ansible-lint`, `yamllint` | — | existing `scripts/validate` | `.ansible-lint-ignore`; `yamllint` via `reviewdog` | none — `generic` only |
| shell | `shfmt`, where the repository wants it | `shellcheck` | — | existing validate script or a new job | `shellcheck` directives, per finding | none — `generic` only |

`yamllint` has no baseline of its own. §7.6 says scope it with `reviewdog`
rather than custom code, and run it advisory-only if that is disproportionate.
For `orange`, which already runs `yamllint` over the whole tree and passes, it
stays as it is: there is no backlog to baseline.

### Resulting rule set per repository

| Repository | CI gate adds | Habit Hooks plugins | `files` in the generated config |
| --- | --- | --- | --- |
| architecture | `ruff`, `markdownlint-cli2`, `lychee`, gitleaks | python, generic | `**/*.py`, `**/*.md` |
| orange | `ruff` on `scripts/` and `statuspage/`; `ansible-lint`, `yamllint`, `shellcheck` | python, generic | `**/*.py`, `**/*.yml`, `**/*.yaml`, `**/*.sh` |
| orange-inventory | `shellcheck`; `ansible-lint` where roles are referenced | generic | `**/*.yml`, `**/*.sh`, `**/*.md` |
| deploys | `shellcheck`, gitleaks, `kubeconform` | generic | `**/*.sh`, `**/*.yaml` |
| myskills | `shellcheck`, gitleaks | generic | `**/*.sh`, `install`, `tests/run` |
| plepic | `eslint` already runs; add `shellcheck` | typescript, generic | `**/*.ts`, `**/*.tsx`, `**/*.sh` |
| robobook | `ruff`, gitleaks, first CI workflow | python, generic | `**/*.py` |
| servitium | `eslint` (none today), `shellcheck` | typescript, generic | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.sh` |
| nomadtty | `eslint` (none today); `shellcheck` widened past two files; gitleaks | typescript, generic | `**/*.js`, `**/*.mjs`, `**/*.sh` |
| mihkel | `eslint`, `ruff`, `shellcheck` | typescript, python, generic | `**/*.js`, `**/*.py`, `**/*.sh` |
| ai-portal | gitleaks only | generic | `**/*.md` |
| entpass | gitleaks only | generic | `**/*.md` |

`nomadtty`, `servitium`, and `mihkel` declare `typescript` for JavaScript. The
Habit Hooks typescript plugin scans `**/*.ts` and `**/*.tsx` by default, so the
generated `files` widens it to `.js`/`.mjs`. Without that the coach finds
nothing in three repositories.

`jscpd` is disabled in `architecture`, `orange-inventory`, `deploys`,
`myskills`, `entpass`, and `ai-portal` — no npm project to resolve it from.
`line-count` still runs. See open question Q2.

### Baselining pre-existing findings

Every gate blocks on new work only, using each linter's own baseline (§7.6). No
custom baseline format and no diff-hunk filter is written.

Baselines are generated in wave 2, committed in the same PR, and their counts
recorded in `state.yaml`. Habit Hooks snooze baselines are generated **after**
the sensor tools are installed, because `habit-snooze --snooze` otherwise
snoozes the `incomplete-run` warning itself.

## 5. `AGENTS.md` budget

Measured in lines of **local** content — everything outside the managed markers.
The managed section is central policy; a repository cannot shorten it, so
counting it would penalise repositories for something they do not control.

| | Lines | Behaviour |
| --- | --- | --- |
| Soft target | 60 | reported by the audit; passes |
| Hard ceiling | 150 | fails conformance |
| Managed section | 40 | central budget; a change that exceeds it is a standards bug |

Today: orange 481, robobook 227, orange-inventory 196, servitium 85, plepic 83,
nomadtty 58, mihkel 53. Two repositories are over the ceiling and one is far
over. `orange` reaches the target by moving its 59-line command catalogue to
`docs/current/commands.md` and its 139-line delegation policy to
`standards/agent-operation.md`.

Gate the outrage, coach the ideal (§5.12).

### Automated documentation checks

Two tools, no more (§5.11):

- `markdownlint-cli2` — structure and layout.
- `lychee` — links, internal and external.

Both run in `architecture`'s CI on every push to `main`, and in each
repository's CI from wave 2. Wording is a review concern; no prose linter is
written.

## 6. Migration map

`migration-map.yaml` holds 27 entries. The shape of it:

| Action | Entries | Largest |
| --- | --- | --- |
| centralize | 7 | orange's 139-line subagent delegation policy |
| reduce-and-link | 6 | orange-inventory's duplicated worktree rules |
| relocate-local | 4 | nomadtty's 843-line `mistakes.md` |
| keep | 4 | the active shop initiative under orange-inventory |
| generate | 3 | `CLAUDE.md`, the managed section, `.habit-hooks/config.toml` |
| decide | 8 | nomadtty's four rival instruction systems |

### Active work protections

Four bodies of active work are registered by link and left untouched (§5.7):

| Repository | Path | Why |
| --- | --- | --- |
| orange-inventory | `docs/working/2026-08-08-legacy-vm-shop/` | another orchestrator's resume path: `resume-state.md`, 613 KB `journal.md`, 474 KB `decisions.md`, `ledger.md` |
| orange-inventory | `docs/working/2026-08-08-legacy-vm-{mail,web}.md` | same initiative family |
| plepic | `docs/superpowers/plans/2026-08-21-transactional-email-lifecycle.md` | active; the primary checkout is on `feat/stripe-payment-methods` |
| entpass | `docs/working/` | the repository's only content |

The primary `orange-inventory` checkout is dirty and there is a pre-existing
worktree pair at `~/app/.worktrees/orange/smtp-tls-servername`. Neither is
touched. All work happens in worktrees this initiative creates, branched from
the remote default branch (§9.1, §9.6).

## 7. Reusable skills

`myskills` holds two skills today: `big-build` and `big-improve-ui`. Neither
covers anything this initiative needs. The inventory step of §12 is done.

**Proposed skill changes: none.**

The audit skill lives in `architecture/skills/audit-universe/` under the §12
exception, as a thin wrapper over `tooling/universe`. Everything else this
initiative needs — catalogue parsing, baseline sync, per-repository audit — is
that one CLI. Promoting any of it to `myskills` would split one behaviour across
two repositories and force a version bump there for every standards edit here.

`skills.lock.yaml` therefore records the `myskills` commit as pinned-unchanged:
`12c8092be4938f326fde48d3fcaee348cb61b541`.

`myskills` still receives wave 0 and wave 1 work as a governed repository. That
is conformance, not a skill change.

## 8. Rollout

Three waves. One branch and one PR per repository per wave.

### Wave 0 — controls that need no governance layer

Starts immediately after Gate 1, in parallel with Phase 2. Nothing here depends
on the catalogue, the generator, or the standards.

| PR | Repository | Content |
| --- | --- | --- |
| W0-1 | deploys | gitleaks in CI; `kubeconform` behind the existing dry-run build |
| W0-2 | myskills | first CI workflow: `shellcheck` plus gitleaks |
| W0-3 | nomadtty | pin five actions to commit SHAs; add `permissions:` to both workflows |
| W0-4 | robobook | first CI workflow: gitleaks |
| W0-5 | entpass | first CI workflow: gitleaks |
| W0-6 | architecture | CI with gitleaks and the documentation checks (part of Phase 2) |
| W0-7 | architecture | shared Renovate preset in `templates/renovate.json` |
| W0-8 | each of 11 | one small `renovate.json` extending the preset |

W0-8 is one commit per repository, folded into that repository's wave 1 PR to
avoid eleven trivial PRs. Installing the Renovate GitHub App is an operator
action (Gate 2).

`deploys` goes first: it is public and receives automated pushes.

These five controls would be worth doing even if the rest of this initiative
were abandoned. The governance layer that follows exists to keep them true and
to make the next repository cheap.

### Wave 1 — governance conformance

Begins after Phase 2 lands the standards, templates, catalogue, and generator.

| PR | Repository | Notes |
| --- | --- | --- |
| W1-1 | architecture | catalogues itself; governed by the rules it defines |
| W1-2 | orange | largest reduction: 481 lines to under 150 |
| W1-3 | orange-inventory | worktree rules reduce to the one genuinely local rule |
| W1-4 | deploys | first `AGENTS.md` and `CLAUDE.md` |
| W1-5 | myskills | first `AGENTS.md` and `CLAUDE.md` |
| W1-6 | plepic | branch from `origin/main`, not the checked-out feature branch |
| W1-7 | servitium | delete `docs/AGENTS.md` and `docs/CLAUDE.md` |
| W1-8 | robobook | replace the `CLAUDE.md` symlink with the generated pointer |
| W1-9 | mihkel | delete `docs/AGENTS.md`; record the root-documents exception |
| W1-10 | nomadtty | **the largest single job**; needs its own decision record |
| W1-11 | entpass | first `README.md`, `AGENTS.md`, `CLAUDE.md` |
| W1-12 | ai-portal | initial commit pushed directly under the §7.5 exception; three files only |

Each wave 1 PR carries: the generated `AGENTS.md` managed section, `CLAUDE.md`,
the README governance section, `.habit-hooks/config.toml`, `renovate.json`, and
that repository's approved migration entries. Nothing else. A governance PR that
also rewires CI is unreviewable.

### Wave 2 — code-quality and security enablement

One PR per repository, after that repository's wave 1 has merged. Roughly a
dozen small changes each, in one coherent PR rather than fourteen fragments.

Contents per repository: the CI lint and static-analysis gate on its declared
languages, linter baselines with counts, workflow hardening with `zizmor`, the
documentation checks, gitleaks confirmation, the branch-protection floor where
rulesets exist, and `kubeconform` for `deploys`. Each new gate is proved to fail
on a deliberate violation and the fixture reverted.

## 9. Security baseline

Which control lands where, and what cannot be carried.

| Control | Lands in | Cannot be carried by |
| --- | --- | --- |
| gitleaks in CI | all twelve | none |
| GitHub push protection | public repositories | private repositories, plan limitation |
| Workflow hardening: SHA pinning, `permissions:`, `zizmor` | the seven repositories with workflows, plus new ones | repositories with no workflows |
| Renovate | all twelve | none; the app install is an operator action |
| Branch-protection floor | the seven public repositories | **architecture, orange, orange-inventory, myskills, entpass** — rulesets return HTTP 403 on the current plan |
| `kubeconform` and dry-run build | deploys | none |
| Secrets delivery pattern | deploys | none |

### Named accepted risks

1. **Five private repositories cannot enforce branch protection.** The rule in
   `standards/agent-operation.md` — agents never commit to a default branch —
   is the enforcement, and the audit checks it against commit metadata (§7.5).
2. **`deploys` gets no pull-request rule.** Its `main` receives automated digest
   pushes from `plepic` and `servitium` release workflows. Its floor is
   `deletion`, `non_fast_forward`, and `required_status_checks` on `Validate`.
3. **`orange` is declared public and is currently private.** Public-safety
   checks apply to it regardless (§5.6). Publication is out of scope here.

### Pre-authorised `zizmor` exception

`plepic/.github/workflows/deploy-test.yml` and
`servitium/.github/workflows/deploy-test.yml` use `pull_request_target`
deliberately, with a gate job that verifies trusted pull-request metadata before
checking out the head revision. Both declare `permissions: {}`. `zizmor` flags
that trigger by default. The exception is recorded in `standards/security.md`
with its reasoning **before** wave 2 runs, so no agent "fixes" a correctly
designed pipeline to silence a linter.

### Secrets delivery for `deploys`

External Secrets Operator reading from the OpenBao instance Orange already runs.
SOPS with age is the recorded fallback. Written into
`standards/gitops-and-deployment.md` so agents do not improvise.

### Recorded as candidates, not built

OpenSSF Scorecard; build provenance attestation for GHCR images; Habit Hooks
plugins for ansible and shell.

## 10. Verification checks

§15 offers 31 candidates. Twenty-two survive. Each surviving check is
mechanical and would catch a real regression.

1. The universe registry parses and validates.
2. Every catalogued repository maps to exactly one profile.
3. The baseline updater changes only text inside its markers.
4. The updater refuses missing, nested, duplicated, or malformed markers.
5. Repository content outside the managed section survives sync byte-for-byte.
6. A managed section that no longer matches today's generated output is stale.
7. A hand-edited managed section fails, and the failure names the regeneration
   command.
8. gitleaks runs in every repository and fails on a fixture secret pattern.
9. Broken documentation links are detected, in `architecture`'s own CI.
10. Registered active working-plan paths still exist.
11. Running the conformance tool twice produces no second diff.
12. A repository absent from the catalogue is ignored entirely.
13. A declared language with no CI gate fails; a gate for an undeclared language
    also fails.
14. A newly introduced violation fails the gate; an identical baselined
    pre-existing one does not.
15. With Habit Hooks absent entirely, the CI gate still runs and still fails.
16. Regenerating Habit Hooks config and the coaching instruction produces no
    diff; changing `languages` changes both.
17. A tool that cannot run is reported as a tool failure, never as a pass.
18. An `AGENTS.md` over the hard ceiling fails; over the soft target it is
    reported and passes.
19. A documentation directory that exists but holds no content fails.
20. Every file in `decisions/` carries the decision-template header.
21. The shared Renovate preset is valid, and a repository extending it resolves
    as intended.
22. This initiative's `deploys` diff contains no manifest or image change.

### Dropped, with the reason

| § | Check | Why dropped |
| --- | --- | --- |
| 3 | planned/nonexistent repository representable | The contract names it a prune candidate. Every catalogued repository exists, `ai-portal` included. |
| 9 | private repositories still secret-scanned | Merged into check 8, which covers all twelve. |
| 12 | a documented exception passes only when explicit and valid | Not mechanical. "Valid" is a judgment, and machinery around it would assert its own shape rather than the exception's soundness. |
| 13 | work-routing worked examples exist | The mechanical half — the paths resolve — is check 9. The rest is review. |
| 20 | coaching and gate differ in scope | The contract names it a prune candidate. It tests a third-party tool's own behaviour, which is exactly the machinery §7.6 declines to build. |
| 22 | no-plugin languages run native linters | Duplicate of check 13, which already fails a declared language with no gate. |
| 28 | documentation checks run in architecture's CI | Folded into check 9, which is specified as running there. |
| 29 | unpinned action or missing `permissions:` fails the lint | That is `zizmor`'s own behaviour. §16 item 18 already requires each CI gate to be demonstrated failing on a fixture. |
| 31 | `kubeconform` rejects a bad manifest | Same reason: it is the wave 0 fixture demonstration, recorded as evidence rather than as a standing check. |

## 11. Exceptions and risks

| Item | Kind | Handling |
| --- | --- | --- |
| Five private repositories without rulesets | accepted risk | named in `standards/security.md`; the audit substitutes |
| `deploys` without a pull-request rule | exception | named, with the promotion reason |
| `plepic` and `servitium` `pull_request_target` | exception | pre-authorised before wave 2 |
| `orange` declared public, currently private | mismatch | tracked; §9.2 forbids acting |
| `mihkel`'s ten root documents | proposed exception | open question Q5 |
| `nomadtty`'s four instruction systems | largest risk | own decision record; W1-10 |
| `nomadtty`'s 1166-line `change-trace.md` | proposed deletion | open question Q6; default is keep |
| Habit Hooks `files` and `jscpd` | contract correction | open question Q2 |
| Top-tier review unavailable | blocking for §16 item 13 | open question Q1 |
| `plepic` primary checkout on a feature branch | operational | branch from `origin/main` in a worktree |
| `orange-inventory` primary checkout dirty | operational | never write to it (§9.1) |

## 12. What this plan does not do

- It does not change any repository's visibility.
- It does not change an image digest, an Argo CD manifest, or live state.
- It does not create a repository or scaffold application code.
- It does not implement AI Portal; it registers it.
- It does not rewrite, reformat, or refactor existing application code.
- It does not work the linter backlog down. That is ordinary follow-up work in
  each owning repository, routed by §5.8.

## 13. Decisions to record in Phase 2

1. `001-architecture-repository-role.md`
2. `002-source-of-truth-and-documentation-ownership.md`
3. `003-myskills-remains-separate.md`
4. `004-conformance-tooling-in-python.md` — including what it costs: `myskills`
   is entirely bash, so this adds a second language to the tooling surface.
5. `005-audit-skill-lives-in-architecture.md`
6. `006-habit-hooks-configuration-is-generated-with-explicit-files.md` — new,
   from the verification finding.
