# G1 risks and fallbacks

| Risk | Decision or fallback | Gate |
| --- | --- | --- |
| Exposing the Authentik login origin conflicts with decision 012 | Require G1 acceptance of the precise superseding decision, an enumerated `access=google` policy before DNS, outside-account denial, and a DNS withdrawal path | G1 and G4 |
| External OIDC test needs IdP DNS while portal DNS is withheld | G1 explicitly authorizes publishing the separate IdP DNS after its gate is verified; use a test-only portal DNS override for G4; G5 publishes portal DNS only | G1 and G4 |
| Single-origin uploaded content could execute script and use chat session | Never expose an individual project asset URL; whole archives download as attachment with `nosniff` and sandbox CSP; block Scratch publication until direct-navigation payload tests pass | Scratch hub gate |
| LibreChat subpath or MCP callback proves unsound at the pinned version | Test both before G4. A separate chat origin requires another Access application, route, DNS, OIDC callback, and operator exposure approval; do not silently switch | G4 |
| LibreChat role merge widens restricted access | Start with restrictive base role, enumerate endpoint/model permissions, and send tampered requests; refuse release on mismatch | G4 |
| OpenRouter credential fails or cost escapes intended bound | Operator sets spend limit before live model calls; ESO holds key; clear error and alert; pause provider traffic if limit cannot be verified | G4 |
| MongoDB backup handler or restore is unusable | Do not hold irreplaceable chat data until encrypted upload and isolated logical restore succeed | G4 |
| Single host lacks capacity for MongoDB and chat | Measure current capacity before manifest promotion; lower requests within tested limits or return to operator if core workload cannot fit | G3 |
| Stale local repository refs hide existing values or changes | Fetch and branch from `origin/main` per repository before trusting a diff; recheck both Orange and inventory refs | Before every PR |
| Public source or manifests leak private identity/topology | Keep live values in inventory, secret values only in OpenBao/local key path, run publication gates before each public PR | Every PR |

The Scratch hub and Scratch AI are independently useful later releases. Their editor feasibility, PostgreSQL storage, revision safety, backup, and AI patch risks belong in their own initiative records. No fallback may remove practical debugging, sharing, or controlled edits without operator approval.
