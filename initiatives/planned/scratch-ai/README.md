# Scratch AI — planned initiative

This is the third independently useful AI Portal product. It depends on a verified Scratch hub with immutable revisions and optimistic concurrency. Its own contract, PR-sized plan, and gates must be approved before implementation; neither portal/chat nor the manual hub waits for it.

Deliver contextual explanation and debugging, a structured scoped proposal, validation, a visible preview of affected sprites/scripts/blocks, explicit Apply or Cancel, a new revision on Apply, behavior recheck, and one-click exact Undo. The browser never receives a provider key. All remote model traffic uses the approved OpenRouter path. Full-project opaque rewrites are not the normal change format.

Use deterministic mock-model behavior tests in CI and small budgeted live-provider checks during the unpublished verification window. An invalid proposal or Cancel must leave project state byte-for-byte unchanged; Apply must create a revision; Undo must recover the exact prior archive. A loss of meaningful controlled edits needs operator approval before any fallback is adopted.

## Retained behavior and provider requirements

The old portal contract's AI requirements survive its retirement on 2026-10-07.
They are future work, not an implemented capability. Extract selected project
context and static analysis; explanations must use that context. Checkpoint the
current revision before analysis and a proposal. Show the affected sprites,
scripts, and blocks before explicit Apply or Cancel. Never save an AI change
invisibly. Reanalyze and run a behavior check after Apply.

Test normal and invalid scoped patches with representative long-lived projects.
Unsupported extensions must produce a clear limitation. Validate before any
mutation, preserve exact archive bytes on invalid proposals and Cancel, and
restore the exact previous revision with one-click Undo. The hub's ACLs and
stale-save protection apply to AI changes too.

Enforce model/tool permissions, provider routing, and quotas server-side.
Use the approved OpenRouter route only, with an operator-set spend limit and
safe credential rotation. Never expose provider or unrestricted tool credentials
to the browser, logs, prompts, fixtures, or artifacts. A failed or expired
provider key must yield a clear user error and operator alert. Do not widen
permissions to make a test pass or collect per-user activity telemetry.

Pin the editor, analysis tools, and provider integration to a tested release;
do not upgrade them independently without behavior verification. The hub's
feasibility spike must demonstrate the minimal proposal/apply/undo loop before
a large editor fork is adopted. The AI release still needs its own reviewed
acceptance and publication gates; a successful spike does not implement it.
