# Security standard

No repository in this universe stores a secret. Every repository scans for one.
A repository declared public must be safe to publish today, whatever its current
GitHub visibility.

Those three rules carry most of the security value here. The controls below
enforce them.

## Secrets

Never commit a password, token, API key, private key, AppRole SecretID,
kubeconfig, rendered Kubernetes Secret, recovery JSON, or live export.

A private repository is not a secret store. `orange`, `orange-inventory`,
`myskills`, `entpass`, and `portfolio-bot` are private because their content is
not for publication. That is not the same as holding secret values, and none of them
does.

Credentials live outside every repository, in the ignored `.keys/` directory of
the Orange checkout or in OpenBao.

- Review every staged diff for secrets before committing. The hook is a
  backstop, not the review.
- Never paste secret-bearing command output into a commit message, document,
  issue, or CI artifact.
- Keep secret-bearing Ansible templates, diffs, and applies under `no_log: true`.
- Never redact a secret by renaming it to pass a check.

If you find a real credential in Git history, stop. Do not push, rewrite
history, or rotate anything. Remediation needs an operator decision, because it
may require rotation, a history rewrite, or public disclosure handling.

## Public and private boundaries

Track visibility as four separate facts in
[`universe/repositories.yaml`](../universe/repositories.yaml):

```yaml
declared_visibility: public | private
current_remote_visibility: public | private | unknown
public_safe_required: true | false
publication_status: published | currently-private | candidate | not-applicable
```

`declared_visibility` is the content policy. `current_remote_visibility` is what
GitHub reports. The two may differ. Today `orange` is the one repository where
they do.

**A repository with `public_safe_required: true` must pass public-content policy
even while its GitHub repository is private.** `orange` is declared public and
is currently private. Its content rules are the public ones.

Never change a repository's visibility without an explicit operator decision.
Never publish or unpublish a GHCR package as a side effect of other work.

Never copy private inventory material into a public or public-ready repository.

### Public-safe is wider than secret-free

A secret scanner finds credentials. It does not find everything that makes
content unsafe to publish, and passing gitleaks is not the same as being
public-safe.

In a repository requiring public safety, treat these as needing a decision
before they are committed:

- an internal hostname, a private IP range, or a network topology detail;
- a live resource identifier — an account number, a workflow ID, a channel name;
- a real person's name, address, or contact details;
- the shape of an internal process an attacker could use to social-engineer it.

None of these is a credential. Each narrows an attacker's search.

Where such content is deliberately published, record the decision. `mihkel` is
the live case: it is public and carries RFC1918 addresses, an internal hostname,
and a live n8n workflow ID. Nothing records that the exposure was considered,
which is the gap — not the content.

## Secret scanning

Use two mechanisms, because they catch different things.

| Mechanism | Where | Catches |
| --- | --- | --- |
| GitHub push protection | public repositories | the leak, before it lands |
| gitleaks | CI in every repository | what push protection does not recognise |

gitleaks runs in every repository's CI, over full history:

```yaml
      - name: Download pinned gitleaks
        env:
          GITLEAKS_VERSION: 8.30.1
          GITLEAKS_SHA256: >-
            551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb
        run: |
          set -euo pipefail
          archive="gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz"
          curl --fail --silent --show-error --location \
            --output "$archive" \
            "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/${archive}"
          echo "${GITLEAKS_SHA256}  ${archive}" | sha256sum --check --strict
          tar -xzf "$archive" gitleaks
          ./gitleaks git --redact --verbose
```

`gitleaks git` reads history, so the checkout step needs `fetch-depth: 0`.

Pin the version and verify the checksum. A supply-chain check that downloads an
unverified binary is not a check.

Repositories that also run a `.githooks/pre-commit` gitleaks scan keep it. Enable
it once per checkout with `git config --local core.hooksPath .githooks`. Never
bypass it.

**Do not demonstrate gitleaks by committing a fixture secret.** Pushing a
credential-shaped string at a public repository is the failure this control
exists to prevent. Demonstrate it locally with `gitleaks dir --no-git` against a
scratch file, then delete the file.

## Workflow hardening

Agents edit CI workflows constantly, and a workflow is the shortest path from a
pull request to a token.

1. **Pin every third-party action to a full commit SHA**, with a comment naming
   the version:

   ```yaml
         - name: Check out repository
           # actions/checkout v7.0.1
           uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
   ```

   Keep the comment true. A comment naming one version beside another version's
   SHA is worse than no comment.

2. **Set a least-privilege top-level `permissions:` block** in every workflow.
   Start at `contents: read`. Grant more at job level, on the job that needs it.

3. **Lint changed workflow files with `zizmor`.**

### Pre-authorised exception: `pull_request_target`

`plepic/.github/workflows/deploy-test.yml` and
`servitium/.github/workflows/deploy-test.yml` use `pull_request_target`
deliberately. Each has a `gate` job that verifies trusted pull-request metadata
before any later job checks out the head revision, by pinned SHA.

Both declare `permissions: {}` at the top level, so a job added later inherits
nothing rather than the repository default. `servitium`'s was missing and was
added; keep it that way.

`zizmor` flags that trigger by default. **This is an accepted, reviewed design.**
Suppress the finding for these two workflows. Do not restructure either pipeline
to silence the linter.

An agent that "fixes" a correctly designed pipeline has made the repository
worse. A first run that fails on intended design teaches everyone to ignore the
tool.

## Dependency automation

Install Renovate once as a GitHub App, **on every governed repository including
`architecture`**. A `local>` preset is fetched with the same installation token,
so a repository the app cannot read is a preset it cannot resolve — and every
repository extending it stops updating, with `Cannot find preset's package`.

**The preset repository must be public if any repository extending it is
public.** The hosted app scopes its token per repository, and Renovate's own
documentation is explicit: a preset in a private repository cannot be extended
by a public one. `architecture` is public for this reason among others.

Every repository extends the shared preset at
[`templates/default.json`](../templates/default.json):

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["local>hannosirkel/architecture//templates/default"]
}
```

**The path carries no file extension.** Renovate appends `.json` itself, so
`//templates/renovate.json` resolves to `templates/renovate.json.json` and
fails. The file is named `default.json` because `renovate.json` as a *preset*
filename is deprecated, and because a repository's own config is also called
`renovate.json` — one name for two different things invites exactly this
mistake.

Each repository holds a small `renovate.json` that extends the preset and adds
nothing else unless it must.

Renovate also pins digests, which `deploys` needs anyway.

## Branch protection floor

On a repository that supports rulesets, require:

- `deletion` — blocked;
- `non_fast_forward` — blocked;
- `pull_request`;
- `required_status_checks` on the repository's CI gate.

### Named exceptions and accepted risks

**Six private repositories cannot carry a ruleset.** `orange`,
`orange-inventory`, `myskills`, `entpass`, `portfolio-bot`, and `meeme` return HTTP 403
from the rulesets API: *"Upgrade to GitHub Pro or make this repository public to enable this
feature."* This is an accepted, named risk, not a silent gap. The
never-commit-to-a-default-branch rule in
[`agent-operation.md`](./agent-operation.md) stands in for it, and the audit
checks commit metadata against it.

**`deploys` takes no `pull_request` rule.** Its `main` receives automated image
digest pushes from the `plepic` and `servitium` release workflows. A
pull-request requirement breaks promotion. Its floor is `deletion`,
`non_fast_forward`, and `required_status_checks` on `Manifests`, `Shell`,
`Workflows`, and `Documentation`.

**A required status check blocks an automated push unless the pushing app
bypasses the ruleset.** A commit that has just been created has no check runs
against it, so the push is rejected with `GH013: 4 of 4 required status checks
are expected`. Dropping the `pull_request` rule does not help; the two rules
block a direct push independently.

Learned by breaking it: adding `required_status_checks` to `deploys` silently
stopped every promotion for two hours and ten builds. The pull requests were
green, because the failure is in the release workflow that runs *after* the
merge.

`deploys` therefore lists both deployer apps as bypass actors:

| App | ID | Mode |
| --- | --- | --- |
| `servitium-deployer` | 4345014 | `always` |
| `plepic-deployer` | 4614643 | `always` |

`always` rather than `pull_request`, because the push is direct. Note that a
bypass actor is exempt from the **whole** ruleset, not from one rule: both apps
can also delete `main` and force-push it. Accepted because each pushes a single
fast-forward commit from a workflow whose content is reviewed like any other
file, and the alternative — no status checks on `deploys` at all — is weaker.

Any repository that later takes an automated push to a protected branch needs
the same treatment. Verify it by watching the *post-merge* run, not the pull
request's checks.

## Manifest validation

For `deploys` and any repository shipping Kubernetes manifests, run a dry-run
render and then schema-check it:

```bash
kubectl kustomize <overlay> | kubeconform -strict -summary
```

`kubectl-validate` is the successor candidate if `kubeconform` stops being
maintained. Do not switch until it does.

## Recorded as candidates, not built

- OpenSSF Scorecard.
- Build provenance attestation for GHCR images.

Neither is part of the bootstrap.
