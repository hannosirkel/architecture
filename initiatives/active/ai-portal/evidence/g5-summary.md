# G5 publication summary

The operator explicitly approved portal DNS publication before G4 was complete,
with faults to be corrected after publication. This is a sequencing exception
to the [portal/chat contract](../../ai-portal.md), not a waiver of its
acceptance checks. The private [publication evidence](https://github.com/hannosirkel/orange-inventory/pull/79)
records the route observation.

The published DNS record resolved to Cloudflare edge addresses, and a public
HTTPS request passed certificate verification and received a redirect to
Cloudflare Access. The application was Synced and Healthy. The operator later
signed in with Google and confirmed the OpenRouter model selector is visible.

The external acceptance record still needs an unlisted-account denial check,
an independent public HTTPS status-code monitor, and a comparison of the
served digest with the [release manifest](../release-manifest.yaml). G5 remains
open. A fast exposure rollback withdraws the portal DNS record; workload
rollback uses the reviewed GitOps image pin.
