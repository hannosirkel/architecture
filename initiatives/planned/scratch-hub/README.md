# Scratch hub — planned initiative

This is the second independently useful AI Portal product. It starts after the portal/chat prefix proxy and identity path are verified. Its own contract, PR-sized plan, and gates must be approved before implementation; portal/chat publication does not wait for it.

Deliver a maintained Scratch-compatible editor with representative `.sb3` import, manual edit/run/debug, save/reopen/export, owner/editor/viewer grants, sharing, immutable revisions, optimistic concurrency, fork, and restore. Store whole content-addressed archives and revision metadata in PostgreSQL. Serve no individual uploaded assets from the shared origin. A feasibility spike must compare maintainable editor/debugger sources and prove project round trips before a large fork is adopted.

The application repository owns editor and hub source; `deploys` owns pinned workloads and backup-compatible policies; Orange owns its Argo CD Application, namespace enrollment, PostgreSQL backup target and monitoring; private inventory owns live values. Test ACL denial, stale saves, archive safety, import/export semantics, encrypted backup and isolated restore, and direct-navigation script payloads. Publication of `/scratch` needs its own operator gate and external-route evidence.
