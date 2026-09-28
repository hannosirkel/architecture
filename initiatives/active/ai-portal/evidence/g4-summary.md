# G4 verification summary

Portal/chat is published following the operator's explicit exception to the
planned G4-before-G5 sequence. Publication is not acceptance of the remaining
G4 checks. The private [release evidence](https://github.com/hannosirkel/orange-inventory/pull/79)
records operational observations without credentials or raw logs.

## Observed

- The published edge returned HTTPS and a Cloudflare Access redirect; the
  application was Synced and Healthy with the portal, LibreChat, OpenRouter
  proxy, and MongoDB workloads ready.
- After [deploys #63](https://github.com/hannosirkel/deploys/pull/63) and
  [Orange #159](https://github.com/hannosirkel/orange/pull/159), the operator
  confirmed the OpenRouter model selector is visible.
- The first portal login required an extra Authentik password. [Orange #160](https://github.com/hannosirkel/orange/pull/160)
  assigned a Google-only source flow to the portal provider. Live Authentik
  state showed only identification and user-login stages, with no local
  password stage. The repeat focused reconcile returned `changed=0`.
- In a fresh private window, the operator then signed in with one credential
  prompt, opened `/chat`, and received a text reply. [Private inventory #81](https://github.com/hannosirkel/orange-inventory/pull/81)
  records the browser and runtime evidence.
- The encrypted MongoDB backup and isolated restore drill are recorded in
  [private inventory #67](https://github.com/hannosirkel/orange-inventory/pull/67).
- The OpenRouter proxy failure alert fired and cleared in a controlled drill.

## Still required

- Verify silent re-establishment after an Authentik session expires while the
  Google session remains valid.
- Verify Access denial for an unlisted account, direct-path authorization,
  profile enforcement, and group removal/revocation against the live release.
- Fire and clear the portal and MongoDB availability alerts.
- Establish and verify an independent public HTTPS status-code monitor.

G4 and G5 remain open until their behavior and external publication evidence
are recorded. The [release manifest](../release-manifest.yaml) pins the
currently deployed source, GitOps revisions, and images.
