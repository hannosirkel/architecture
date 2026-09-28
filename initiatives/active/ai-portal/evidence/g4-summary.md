# G4 verification summary

Portal/chat is published following the operator's explicit exception to the
planned G4-before-G5 sequence. Publication is not acceptance of the remaining
G4 checks. The private [release evidence](https://github.com/hannosirkel/orange-inventory/pull/79)
records operational observations without credentials or raw logs.

## Observed

- The published edge returned HTTPS and a Cloudflare Access redirect; the
  application was Synced and Healthy with the portal, LibreChat, OpenRouter
  proxy, and MongoDB workloads ready.
- The operator completed Google sign-in and later reported that chat seemed to
  work. After [deploys #63](https://github.com/hannosirkel/deploys/pull/63)
  and [Orange #159](https://github.com/hannosirkel/orange/pull/159), the
  operator confirmed the OpenRouter model selector is visible.
- The encrypted MongoDB backup and isolated restore drill are recorded in
  [private inventory #67](https://github.com/hannosirkel/orange-inventory/pull/67).
- The OpenRouter proxy failure alert fired and cleared in a controlled drill.

## Still required

- Record a cold browser text response and whether Google sign-in led to a
  second credential prompt.
- Verify Access denial for an unlisted account, direct-path authorization,
  profile enforcement, and group removal/revocation against the live release.
- Fire and clear the portal and MongoDB availability alerts.
- Establish and verify an independent public HTTPS status-code monitor.

G4 and G5 remain open until their behavior and external publication evidence
are recorded. The [release manifest](../release-manifest.yaml) pins the
currently deployed source, GitOps revisions, and images.
