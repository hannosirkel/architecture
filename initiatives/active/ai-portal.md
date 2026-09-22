# AI Portal initiative

## Purpose and authority

Deliver a family AI portal with one sign-in and managed chat. The full requested program also includes a shared Scratch-compatible project hub and controlled AI project edits. The earlier detailed draft remains in private `orange-inventory` history at `docs/working/2026-08-25-ai-portal.md`; this reconciled public contract is authoritative for portal and chat. Its binding requirements are stated here, without relying on private review findings.

The work is split into three independently useful and revertible initiatives, in order:

1. **Portal and chat:** launcher, prefix proxy, identity, and LibreChat with server-enforced profiles.
2. **Scratch hub:** a separate planned initiative for editor, import/export, ACLs, revisions, sharing, fork, restore, and stale-save protection.
3. **Scratch AI:** a separate planned initiative for contextual explanation, visible structured proposal, validation, explicit apply, behavior check, and exact undo. It depends on the hub.

The application repository owns source and image builds; `deploys` owns workload manifests and pinned image digests; `orange` owns Argo CD Applications and platform integration; `orange-inventory` owns live non-secret choices and identities. Reusable skills belong in `myskills` only if an existing skill cannot cover the job.

## Binding product and security behavior

- Cloudflare Access gates the portal and separate identity-provider hostname with enumerated Google accounts. Authentik federates to Google and supplies application groups. The user enters credentials once. Direct requests to each application path enforce entitlement independently of launcher-card visibility.
- The portal uses one application origin: `/` for navigation and `/chat` for LibreChat. The prefix proxy reserves `/scratch` for the later hub. The identity provider uses a separate Access-gated origin. Supersede Orange decision 012 before creating that identity-provider route or its manifests.
- LibreChat has `restricted`, `user`, and `admin` profiles derived from Authentik groups through its OIDC role validation and sync. Model, MCP/tool, sharing, and administration restrictions must hold server-side on tampered requests. Admin assignment remains separate from role sync.
- All remote model traffic goes through OpenRouter with a spend-limited key delivered through OpenBao and ESO. No subscription OAuth bridge or direct provider path is part of this release. A supported operator rotation procedure and failure alert are required.
- User project bytes are served only as whole `.sb3` attachments. No individually addressable costume, sound, or image route may exist on the shared origin. User-derived responses carry attachment disposition, `nosniff`, and sandbox CSP. The proxy enforces per-path CSP, cookie-path rewriting for chat, streaming, upload limits, and identity-header discipline.
- The later Scratch hub must preserve representative projects through import, manual edit, run, save, reopen, export, fork, and restore. Owner/editor/viewer checks are server-side; stale saves cannot silently overwrite newer revisions. The later AI initiative must make edits scoped, previewed, explicitly accepted, revisioned, validated, and exactly undoable. Neither is a portal/chat release condition.
- GitOps owns workloads; no durable manual edit to Argo CD resources. One production environment runs pinned digests. G1 covers publication of the separately gated identity-provider DNS record for real external OIDC verification. The portal's unpublished verification window has its tunnel route and Access policy but no portal DNS record. Publishing portal DNS requires G5 operator approval.
- Datastores need encrypted backups and a demonstrated isolated restore before storing irreplaceable user data. Monitoring covers workload and database availability, generated backup alerts, storage headroom, and external reachability without family activity telemetry.

## Gate sequence

| Gate | Evidence and decision |
| --- | --- |
| G1 — plan | Reconciled architecture, access matrix, repository ownership, risks, and independent review. Operator approval is required for the new Access-gated identity-provider boundary and superseding decision 012. |
| G2 — skills | Reuse existing skills; add only reusable missing capability, test it, and pin its version. |
| G3 — portal implementation | Launcher, prefix proxy, OIDC, LibreChat profiles, OpenRouter route, and platform integration pass their component checks. Scratch has its own later feasibility gate. |
| G4 — verified | Portal/chat production digest is deployed without portal DNS; security and profile behavior, database backup/isolated restore, and a fired/resolved availability alert pass. The separate identity-provider hostname already resolves under the G1-approved gate so OIDC can be tested from a cold browser. |
| G5 — publication | Operator reviews exact release, access list, digests, evidence, limitations, and rollback, then approves DNS publication. |

No gate may be inferred from compilation, a healthy Argo CD status, or elapsed time. Keep live identities, secret values, private addresses, and recovery logs out of this repository. Record one PR-sized implementation row per repository; push a provider interface before its consumer.

## Completion

This portal/chat initiative completes after G5 external-route tests, profile behavior evidence, immutable digest record, MongoDB backup and isolated restore evidence, monitoring evidence, rollback procedure, and a handoff naming all repositories, PRs, commits, limits, and credential-renewal steps without secret values. The requested overall program completes only when the separate Scratch hub and Scratch AI initiatives also meet their own acceptance gates.
