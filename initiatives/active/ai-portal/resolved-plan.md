# AI Portal resolved plan — G1 draft

## Current state and routing

The current local `ai-portal` checkout contains governance files but no product code. `deploys` has no portal root. Orange has reusable Argo CD, Authentik, ESO, Cloudflare, backup, and monitoring patterns but no portal enrollment. The private inventory holds the original contract and no adjacent initiative state. `architecture` is the cross-repository coordination owner; application behavior still belongs to `ai-portal`.

The earlier planned initiative record is stale: the application repository now has commits. `architecture` and `deploys` local primary branches lag their local `origin/main` refs, so every implementation branch must start from a freshly fetched `origin/main`; absence and diff claims must be checked again there. `myskills` has an existing unrelated dirty file and must remain read-only unless isolated work is needed.

The original contract was too large for one release. Portal/chat is this active initiative; Scratch hub and Scratch AI are separate planned initiatives, each with its own later acceptance and publication gate. The hub depends on the portal prefix proxy; AI depends on the hub. There is no test environment. The portal production namespace is verified before portal DNS exists.

## Pattern choices

| Source pattern | Decision | Reason |
| --- | --- | --- |
| Plepic source-to-`deploys` digest promotion | ADOPT | Matches GitOps ownership; pin the image digest verified before DNS publication. |
| Orange role template plus contract test plus `docs/current/` | ADOPT | Orange's required change unit. |
| Orange OpenBao → ESO namespace-local Secret | ADOPT | Existing sanctioned credential path. |
| Orange tunnel `published=false` | ADOPT | Allows real production digest and Access verification while withholding portal DNS. |
| Orange PostgreSQL backup handler and generated alerts | ADAPT | Later hub data can reuse PostgreSQL; LibreChat MongoDB needs new dump and restore handlers now. |
| Plepic test and live environments | REJECT | No portal staging environment or resource budget is authorized. |
| Plepic shop-specific UI and commerce state | REJECT | Does not serve portal behavior. |
| Reusable skill from `myskills` | ADAPT | Inventory first; create only a missing reusable capability, never a one-off initiative skill. |

## Architecture and ownership

| Repository | Owns | Integration boundary |
| --- | --- | --- |
| `ai-portal` | Launcher/prefix proxy now; Scratch editor, hub, and AI source in later initiatives; tests and image builds | Emits immutable images and documented runtime contract. |
| `deploys` | Namespace workloads, NetworkPolicies, PVCs, pinned image digests | Accepts approved image digest; never carries secrets. |
| `orange` | Argo CD Applications, AppProject destination, namespace/ESO enrollment, Authentik integration, tunnel, monitoring, backup handlers | Ansible renders Applications; Argo CD reconciles workloads. |
| `orange-inventory` | Account list, group membership, private host and provider choices, non-secret site values | Private inventory is separate Git history; no secret values. |
| `architecture` | This cross-repository contract, gate and release evidence | No application source, inventory, or secret. |

Use a small Python ASGI portal service for routing and the launcher. It owns no family data. The portal proxy routes `/` and `/chat` now and reserves `/scratch` for the later hub on one application origin; Authentik has a distinct Access-gated origin. The proxy strips prefixes where required, rewrites the five known LibreChat auth cookies to `Path=/chat`, streams model responses without buffering, enforces request limits, applies per-path CSP, strips untrusted identity headers, and refuses unauthorized direct paths. LibreChat OIDC role claims come from Authentik; role sync cannot grant admin. The lowest built-in role is restrictive. OpenRouter is the only remote model provider and its key has a spend limit.

The later Scratch hub will store immutable whole `.sb3` archives and metadata in PostgreSQL, with owner/editor/viewer grants, optimistic concurrency, fork, and restore. It will serve no individual uploaded assets. The later AI initiative will produce a structured proposal, validate it, display affected blocks, wait for Apply, save a new revision, recheck behavior, and offer exact Undo. NuzzleBug/LitterBox are feasibility candidates, not preselected dependencies; a maintained TurboWarp-derived editor plus analysis side panel is the fallback if the former cannot build or remain supportable. Their detailed PR rows and feasibility test belong in their separate plans.

LibreChat's MongoDB needs an encrypted unified-runner backup, generated failure/missing alerts, and tested logical restore into an isolated copy. The namespace policy must admit backup and recovery database traffic and backup egress on 443. The later hub adds a PostgreSQL target. One Grafana dashboard and workload/database availability rules use Kubernetes state metrics; avoid user activity and spend telemetry. The OpenRouter key limit is the cost control.

## Namespace and Application layout

The existing Authentik deployment remains in its current namespace. The new application namespace is `ai-portal`. Orange enrolls that namespace in AppProject destinations and ESO/OpenBao projection. Orange renders one portal/chat Argo CD Application pointing to the `deploys/ai-portal` Kustomize root. That root holds the portal, LibreChat, MongoDB, Services, policies, and PVC. The later Scratch hub adds its own Application and database workload in the same namespace only after its separately approved manifest tests and capacity check. No public Service port is added; the tunnel reaches a private origin.

## Security and deployment sequence

1. Review the proposed Orange decision `docs/decisions/024-ai-portal-access-gated-authentik.md`. G1 approval explicitly authorizes one enumerated-account, Access-gated identity-provider route and its DNS publication for external OIDC tests. It precedes any manifest or route. Rejecting G1 leaves decision 012 in force.
2. Build small source and platform PRs. The interface provider is published before dependent consumers. The public application and manifest repositories contain no live identities or credentials.
3. Verify pinned images, rendered manifests, contracts, behavior, and publication policy. Merge-promote production digests into `deploys`; let Argo CD reconcile.
4. Create the gated identity-provider route and policy, inspect the Cloudflare application and enumerated account policy while DNS is withheld, then publish IdP DNS under G1. Immediately test an unlisted account; withdraw IdP DNS if it reaches origin. Configure the portal tunnel route and Access application with portal DNS withheld. Verify the actual production digest through WireGuard and the tunnel path, using an explicit test-only DNS override for the portal hostname where a browser needs it. The IdP hostname resolves normally. Verify cold-browser SSO, direct-path denial, forged headers, upload isolation, role tampering, backup and restore, and a fired/resolved availability alert.
5. Present G5 with exact digest, access list, evidence, limitations, and DNS-withdrawal rollback. Publish DNS only after approval. Recheck the external route and record handoff.

No secret value is stored in any repository. ESO is the only namespace-local Secret reconciler. The later Scratch hub must make every user-derived download an attachment with `nosniff` and sandbox CSP; scripts cannot run from uploaded project bytes under the chat origin. A cookie path is damage limitation and must never be described as an XSS boundary.

## Pull-request units

Each row names one repository, concrete files, and its verification. The rows are sized below 800 changed lines and at most 10 files; any row that cannot fit is revised before G1 plan approval. Paths in a new application tree are the chosen contract for that tree.

- [ ] `architecture`: add `initiatives/active/ai-portal.md`, `initiatives/active/ai-portal/{state.yaml,resolved-plan.md,access-matrix.md,acceptance.md,risks.md}`, update `initiatives/{README.md,planned/ai-portal/README.md}`, and add `initiatives/planned/{scratch-hub,scratch-ai}/README.md`; verify `python3 -m unittest discover -s tooling -p 'test_*.py'`, `ruff check .`, and `tooling/universe validate`.
- [ ] `architecture`: after the preceding PR merges, add the `initiatives/active/ai-portal.md` pointer in `universe/repositories.yaml`; verify `tooling/universe validate`. The catalogue checks the primary checkout, so the pointer cannot be in the first PR.
- [ ] `orange`: add `docs/decisions/024-ai-portal-access-gated-authentik.md`; verify `bash scripts/validate` and `python scripts/publication-gate --all`. This proposed record needs G1 acceptance before a route manifest.
- [ ] `ai-portal`: add `docs/current/README.md`, `docs/decisions/001-portal-boundaries.md`, `pyproject.toml`, and `.github/workflows/ci.yml`; verify the repository's Python gate and documentation check.
- [ ] `ai-portal`: add `src/portal/auth.py`, `src/portal/app.py`, and `tests/test_portal_auth.py` for Access/OIDC admission and direct-path checks; verify focused tests and then the repository gate.
- [ ] `ai-portal`: add `src/portal/proxy.py` and `tests/test_proxy.py` for prefix, cookie, header, streaming, upload, and CSP behavior; verify focused tests and then the repository gate.
- [ ] `ai-portal`: add `src/portal/launcher.py`, `src/portal/static/index.html`, and `tests/test_launcher.py`; verify entitlement-card and browser navigation behavior.
- [ ] `ai-portal`: add `Dockerfile`, `.github/workflows/release.yml`, `tests/test_container.sh`, and `docs/current/release.md`; verify a pinned-base image build, SBOM/scan results, immutable GHCR digest, and a dry-run promotion artifact before `deploys` consumes it.
- [ ] `orange-inventory`: add private portal account/group/model choices in `group_vars/orange.yml`; verify `inventory/scripts/validate` followed by `bash scripts/validate`. Publish the private interface before its Orange consumer.
- [ ] `orange`: add portal provider/group data in `roles/argocd/templates/authentik-blueprints.yaml.j2`, matching `tests/authentik_templates.yml`, and `docs/current/platform.md`; verify `bash scripts/validate` and publication gate.
- [ ] `orange`: add namespace/AppProject/ESO enrollment in `roles/argocd/{defaults/main.yml,tasks/namespaces.yml,templates/appprojects.yaml.j2,templates/openbao-external-secrets.yaml.j2}`, `inventory-example/group_vars/orange.yml`, `tests/test_argocd_namespace_coverage.py`, and `docs/current/cluster.md`; verify `bash scripts/validate` and publication gate.
- [ ] `orange`: add `roles/argocd/templates/ai-portal-application.yaml.j2`, `tests/ai_portal_argocd_templates.yml`, and `docs/current/platform.md`; verify `bash scripts/validate` and publication gate.
- [ ] `deploys`: add `ai-portal/base/{kustomization.yaml,namespace.yaml,portal.yaml,librechat.yaml,mongodb.yaml,networkpolicy.yaml}` and `ai-portal/tests/test_manifests.py`; verify Kustomize render, kubeconform, and manifest tests.
- [ ] `orange`: add MongoDB dump/restore rendering in `roles/argocd/templates/backups-application.yaml.j2` and schema checks in `roles/argocd/tasks/validate.yml`, with `tests/{backups_templates.yml,recovery_contract.yml}`; verify `bash scripts/validate`.
- [ ] `orange`: add the MongoDB target to `roles/argocd/defaults/main.yml`, update `tests/backups_templates.yml` and `docs/current/backups.md`; verify `bash scripts/validate`, publication gate, encrypted upload, and isolated restore drill.
- [ ] `orange`: document the OpenBao/ESO OpenRouter key deposit, spend-limit check, and rotation path in `docs/current/provisioning.md`; verify publication gate and a dry-run of the documented non-secret steps. The operator supplies the key without placing it in Git or chat.
- [ ] `orange`: add dashboard template `roles/argocd/templates/grafana-ai-portal-dashboard.yaml.j2`, rules in `roles/argocd/templates/prometheus-application.yaml.j2`, `tests/prometheus_templates.yml`, and `docs/current/observability.md`; verify render/JSON tests, host/PVC headroom panels, and a fired/resolved alert.
- [ ] `orange`: add a provider-failure Loki/Grafana alert in `roles/argocd/templates/prometheus-application.yaml.j2`, `tests/prometheus_templates.yml`, and `docs/current/observability.md`; verify that an intentionally invalid OpenRouter credential gives a clear user error and fires/resolves the alert without exposing the credential.
- [ ] `orange-inventory`: add the portal external status-code monitor declaration to `group_vars/orange.yml`; verify `inventory/scripts/validate` and an external reachability probe after portal G5.
- [ ] `architecture`: add `initiatives/active/ai-portal/{release-manifest.yaml,handoff.md,evidence/g4-summary.md,evidence/g5-summary.md}` and update `state.yaml`; verify linked PRs, image digests, backup/restore and external-route evidence before completion.

The later Scratch hub and AI initiatives own their own PR rows. Dependencies here are ordered: application runtime contract before manifests; private inventory interface before Orange consumer; Orange decision acceptance before identity-provider route; image build before digest promotion. The full user request remains open after portal/chat release until both Scratch initiatives complete.

## Acceptance and rollback

G1 requires independent review and explicit operator approval of the new identity-provider boundary and its DNS publication for OIDC testing. G2 verifies any skill additions. G3 closes portal/chat implementation. G4 requires portal/chat security, profile, backup/restore, and monitoring behavior against the unpublished production digest. G5 requires explicit approval to add portal DNS. A manifest or image rollback promotes a known-good digest through Git; fast exposure rollback withdraws the affected DNS record, with the identity-provider record withdrawn separately if necessary. Data restore is a separate explicit lifecycle action, never a side effect of routine reconciliation.

## Open decisions

- Exact private account list and Authentik groups are set in `orange-inventory/group_vars/orange.yml` and reviewed by the operator at G1/G5 without appearing here. G1 approval applies only to that reviewed list; a later enlargement requires a separate operator security decision.
- The IdP boundary requires G1 and the superseding decision record. Until then, no identity-provider tunnel route or manifests are created. G1 must explicitly approve the IdP DNS publication before it occurs; G5 covers the portal DNS only.
- The editor/debugger source is decided by the separate Scratch hub feasibility gate; a fallback that loses meaningful debugging, sharing, or controlled AI edits returns to the operator.
- Current remote refs, upstream component versions, image digests, and live cluster capacity must be refreshed before implementation. They are not inferred from this reconnaissance.
