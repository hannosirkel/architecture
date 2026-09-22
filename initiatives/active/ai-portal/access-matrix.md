# Access matrix for G1 review

Live account addresses and group membership belong only in `orange-inventory`. The names below are structural roles, not a list of people.

| Boundary | Restricted | User | Admin | Unlisted account |
| --- | --- | --- | --- | --- |
| Cloudflare Access | Enumerated account required | Enumerated account required | Enumerated account required | Deny before origin |
| Portal and direct application path | Entitled card and direct path only | Entitled card and direct path only | Entitled card and direct path only | Deny |
| Authentik | Group claim for restricted role | Group claim for user role | Separately assigned admin role | No application session |
| LibreChat | Explicit approved model/tool list | Broader approved list | Administration by separate assignment | Deny |
| Scratch hub | ACL-controlled projects | ACL-controlled projects | Admin operations only where defined | Deny |

The exact Authentik group names, enumerated Access addresses, and per-profile model/tool lists are private configuration. Before G1 authorizes identity-provider DNS publication, the operator reviews the exact private account list in `orange-inventory/group_vars/orange.yml`; the same list must gate both hostnames. G4 must test removal from the Access list and an Authentik group independently, allowing for Access session revocation where a cached identity assertion would otherwise remain valid, and prove a cold-browser session needs only one Google credential prompt.
