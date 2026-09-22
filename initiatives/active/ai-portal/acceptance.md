# Portal/chat behavior acceptance matrix

This matrix is the G1 test contract for the first release. Each result needs an executable test or dated operational evidence. The later Scratch hub and AI initiatives own their own matrices.

| Boundary | Required observation | Evidence gate |
| --- | --- | --- |
| Edge | An enumerated Google account reaches the IdP and portal; an unlisted account is denied by Access before origin | G4 and external G5 |
| Identity | Cold browser enters a Google credential once, then reaches launcher and `/chat`; a renewed Authentik session needs no second prompt while Google is valid | G4 browser test |
| Entitlement | Direct `/chat` request is checked; launcher card visibility matches group; Access-list removal and Authentik-group removal each revoke their own capability | G4 browser/API tests |
| Proxy | Forged `Cf-Access-*` headers on a non-tunnel path fail; origin port is unreachable from outside approved paths | G4 network tests |
| Subpath | OIDC redirects land under `/chat` without doubled prefix; MCP OAuth callback works; assets never fall back to `/` | G4 browser tests |
| Session | All five LibreChat auth cookies have `Path=/chat`; no portal cookie shares their names | G4 response tests |
| Stream and body | Model output arrives incrementally; request/upload limit gives a complete error | G3/G4 integration tests |
| Profiles | Restricted, user, and separately assigned admin receive approved model/tool lists; tampered hidden selections fail server-side; group change takes effect on next sign-in | G4 API tests |
| Provider | All remote model requests use OpenRouter; expired key gives a clear user error and operator alert; the key has an operator-set spend limit | G4 trace/config evidence |
| Recovery | Encrypted MongoDB backup is verified; logical restore to an isolated copy recreates representative chat state without touching production | G4 drill |
| Monitoring | Portal, chat, and database availability alerts render; one deliberately unavailable workload fires and resolves | G4 alert evidence |
| Headroom | Dashboard shows MongoDB PVC and host disk capacity; host disk alert protects local-path storage | G4 dashboard and alert evidence |
| Reachability | External status-code monitor checks the portal route after publication; Access and Cloudflare views show the expected gate | G5 monitor evidence |
| GitOps | Manifests render/schema-check, immutable digest is recorded, and Git revert/known-good digest restores the prior application | G4 release evidence |
| Publication | The digest tested before portal DNS is the one serving after DNS; external route and unlisted-account denial are rechecked | G5 evidence |

The first release leaves `/scratch` closed or returns a deliberate unavailable response. Uploaded project archive tests and user-derived response controls become mandatory before the Scratch hub is exposed on that path.
