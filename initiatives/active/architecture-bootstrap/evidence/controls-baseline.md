# Security and code-quality controls: what exists today

Observed 2026-08-21. `–` means absent.

## Per repository

| Repository | CI | gitleaks in CI | gitleaks hook | Actions pinned | `permissions:` | Dependency automation | Rulesets available | Linter gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| architecture | – | – | – | n/a | n/a | – | no (plan) | – |
| orange | `validate.yml` | yes | pre-commit, pre-push | yes | yes | – | no (plan) | `yamllint`, `ansible-lint` in `scripts/validate` |
| orange-inventory | `validate.yml` | yes | pre-commit, pre-push | yes | yes | – | no (plan) | `yamllint` in `scripts/validate` |
| deploys | `validate.yml` | **no** | pre-commit | yes | yes | – | yes | – |
| myskills | **none** | – | – | n/a | n/a | – | no (plan) | **none** |
| plepic | `validate`, `release`, `deploy-test` | yes | pre-commit | yes | yes | – | yes | `eslint`, `tsc` in `scripts/validate` |
| robobook | **none** | – | – | n/a | n/a | – | yes | **none** |
| servitium | `validate`, `release`, `deploy-test`, `notify` | yes | pre-commit | yes | yes | dependabot | yes | `tsc`, `node --check` |
| nomadtty | `ci.yml`, `publish.yml` | – | – | **no** (`@v7`, `@v4`) | **no** | dependabot | yes | `shellcheck` on two files |
| mihkel | `validate.yml` | yes | pre-commit, pre-push | yes | yes | – | yes | – |
| ai-portal | none (empty) | – | – | n/a | n/a | – | yes | – |
| entpass | **none** | – | – | n/a | n/a | – | no (plan) | – |

## Rulesets and the plan limitation

`GET /repos/{owner}/{repo}/rulesets` returns HTTP 403 —
*"Upgrade to GitHub Pro or make this repository public to enable this feature"* —
for every private repository: `architecture`, `orange`, `orange-inventory`,
`myskills`, `entpass`. Rulesets are available on the seven public repositories.

Existing rulesets:

| Repository | Rules |
| --- | --- |
| deploys | `deletion`, `non_fast_forward` |
| plepic | `deletion`, `non_fast_forward`, `pull_request` |
| robobook | `deletion`, `non_fast_forward`, `pull_request` |
| servitium | `deletion`, `non_fast_forward`, `pull_request`, `required_status_checks` |
| nomadtty | none |
| mihkel | none |
| ai-portal | none |

`servitium` is the only repository at the full §7.5 floor.

**`deploys` must not gain a `pull_request` rule.** Its `main` receives automated
digest pushes from `plepic` and `servitium` release workflows. Requiring a pull
request there breaks promotion. Its floor is `deletion` + `non_fast_forward` +
`required_status_checks`, and that is a named exception, not a gap.

## Wave 0 targets, confirmed against evidence

The contract's five Wave 0 items all check out:

1. **Renovate** — dependency automation exists in 2 of 12 repositories
   (`servitium`, `nomadtty`, both dependabot). Confirmed.
2. **gitleaks in CI** — missing in `deploys`, `myskills`, `nomadtty`, `robobook`,
   `entpass`, `ai-portal`, `architecture`. `deploys` is public and receives
   automated pushes; it goes first. Confirmed.
3. **`kubeconform` in `deploys`** — the `Validate` workflow runs
   `kubectl kustomize` for four overlays and stops there. Nothing schema-checks
   the output. Confirmed.
4. **`shellcheck` in `myskills`** — the repository is entirely bash, has no CI
   workflow directory at all, and its only check is `tests/run`. Confirmed, and
   worse than the contract states.
5. **`nomadtty` pinning and `permissions:`** — `ci.yml` uses `actions/checkout@v7`,
   `docker/setup-buildx-action@v4`, `docker/build-push-action@v7`,
   `actions/setup-node@v4`, `actions/upload-artifact@v4`, and declares no
   `permissions:` block in either workflow. Confirmed; it is the only CI
   repository in that state.

## The `pull_request_target` exception

`plepic/.github/workflows/deploy-test.yml` and
`servitium/.github/workflows/deploy-test.yml` both use `pull_request_target`
deliberately, with a commented gate job that verifies trusted pull-request
metadata before checking out the head revision. Both declare
`permissions: {}` at the top level. `zizmor` flags `pull_request_target` by
default. Pre-authorise this exception in `standards/security.md` before wave 2,
as §7.5 requires.
