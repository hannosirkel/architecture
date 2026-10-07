# Scratch hub — planned initiative

This is the second independently useful AI Portal product. It starts after the portal/chat prefix proxy and identity path are verified. Its own contract, PR-sized plan, and gates must be approved before implementation; portal/chat publication does not wait for it.

Deliver a maintained Scratch-compatible editor with representative `.sb3` import, manual edit/run/debug, save/reopen/export, owner/editor/viewer grants, sharing, immutable revisions, optimistic concurrency, fork, and restore. Store whole content-addressed archives and revision metadata in PostgreSQL. Serve no individual uploaded assets from the shared origin. A feasibility spike must compare maintainable editor/debugger sources and prove project round trips before a large fork is adopted.

The application repository owns editor and hub source; `deploys` owns pinned workloads and backup-compatible policies; Orange owns its Argo CD Application, namespace enrollment, PostgreSQL backup target and monitoring; private inventory owns live values. Test ACL denial, stale saves, archive safety, import/export semantics, encrypted backup and isolated restore, and direct-navigation script payloads. Publication of `/scratch` needs its own operator gate and external-route evidence.

## Retained feasibility and acceptance requirements

These requirements survive retirement of the old portal contract on 2026-10-07.
They describe future work, not implemented behavior. No anonymous publishing or
real-time co-editing belongs in v1. Keep return-to-portal navigation simple;
do not introduce an iframe shell or unnecessary persistent services.

Compare NuzzleBug/LitterBox with a maintained Scratch or TurboWarp-derived
editor and an analysis side panel. Before adopting a large fork, prove:

- A clean build with an empty dependency cache, immutable upstream pins, no
  embedded credentials or inaccessible private dependencies, configurable
  service URLs, and container deployment.
- Representative long-lived `.sb3` fixtures survive create, import, edit, run,
  stop, debug, save, reopen, export, and re-import. Preserve sprites, scripts,
  variables, broadcasts, costumes, and supported extensions; prove valid archive
  bytes and semantic preservation.
- Useful debugging and structured LitterBox or equivalent analysis work.
  Demonstrate a minimal OpenRouter explanation/proposal, visible block change,
  validation, apply, reanalysis, and exact undo to de-risk the later AI release.
- A minimal hub propagates owner/editor/viewer identity and rejects or safely
  forks stale concurrent saves. ACLs protect direct requests server-side.

Obtain focused review of feasibility evidence and fallback choice before a
large fork. Create a separate upstream-fork repository only if independent
history and upgrades require it. A fallback that loses sharing, meaningful
debugging, or practical controlled AI changes requires operator approval.

## Storage and recovery

Reuse Orange's pinned PostgreSQL workload, dump, and logical-restore contracts
in a dedicated application instance; never share Authentik's database instance.
Store each whole immutable archive with its SHA-256, parent revision, author,
and creation time. Enforce a declared per-object size cap before insertion.
Keep revision bytes and project metadata in the same consistent database dump;
do not create a separate loose-file store and backup pairing scheme.
`local-path` provides single-host storage requests, not quotas or replication.

Before storing irreplaceable projects, enroll the datastore in the existing
backup contract, verify encrypted upload, and restore representative state to
an isolated copy. Include backup-age/failure coverage, hub/database availability,
PVC and host-disk headroom, and one fired/resolved availability drill.
Use existing Kubernetes/log telemetry without per-user activity collection or
new exporters unless a concrete unanswered operational question requires one.
Guard migrations and prove rollback to a known-good release.

## Single-origin security and publication

- Keep `/scratch` closed until its own publication gate passes. Enforce direct
  path entitlement, trusted-proxy identity, group changes, and single-sign-in
  navigation, including desktop and mobile views.
- Serve whole project archives only. Expose no individually addressable costume,
  sound, or image URL. Any future individual assets require a separate origin.
- Every user-derived response uses `Content-Disposition: attachment`,
  `X-Content-Type-Options: nosniff`, and `Content-Security-Policy: sandbox`.
  Attempt direct navigation with HTML/SVG payloads and prove no script executes.
- Deny inline scripts by default with the Scratch path's CSP; constrain service
  workers to their own path. Use distinct application session cookie names.
  Chat cookies must not accompany Scratch requests. Cookie paths do not prevent
  an attacker executing same-origin script from calling authenticated chat APIs.
- Reject malformed archives, ZIP bombs, and oversized uploads safely. Proxy and
  hub enforce the same size threshold and return one complete, clear error.
- Prove assets remain under `/scratch/` without falling back to the origin root.
  For a TurboWarp build, verify the pinned upstream `ROOT=/scratch/` mechanism,
  including its mandatory trailing slash, rather than assuming compatibility.
- Keep provider keys server-side through OpenBao/ESO. Test network policies,
  render/schema validation, immutable promotion, and isolated recovery before
  publication. No separate staging environment is assumed: verify the Scratch
  release while its public application path remains unavailable, then publish
  the same tested digest with operator authorization and external-route evidence.
