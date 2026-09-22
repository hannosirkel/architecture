# Scratch AI — planned initiative

This is the third independently useful AI Portal product. It depends on a verified Scratch hub with immutable revisions and optimistic concurrency. Its own contract, PR-sized plan, and gates must be approved before implementation; neither portal/chat nor the manual hub waits for it.

Deliver contextual explanation and debugging, a structured scoped proposal, validation, a visible preview of affected sprites/scripts/blocks, explicit Apply or Cancel, a new revision on Apply, behavior recheck, and one-click exact Undo. The browser never receives a provider key. All remote model traffic uses the approved OpenRouter path. Full-project opaque rewrites are not the normal change format.

Use deterministic mock-model behavior tests in CI and small budgeted live-provider checks during the unpublished verification window. An invalid proposal or Cancel must leave project state byte-for-byte unchanged; Apply must create a revision; Undo must recover the exact prior archive. A loss of meaningful controlled edits needs operator approval before any fallback is adopted.
