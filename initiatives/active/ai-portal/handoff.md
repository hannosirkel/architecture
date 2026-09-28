# AI Portal handoff

Portal/chat is published and serves the first text-chat release. The operator
authorized publication before G4 verification was complete. This initiative
remains open; the Scratch hub and Scratch AI are separate planned initiatives.

## Release references

The [release manifest](release-manifest.yaml) records source commit, four image
references, and GitOps revisions. The last application source change was
[AI Portal #21](https://github.com/hannosirkel/ai-portal/pull/21); the current
workload revision is [deploys #63](https://github.com/hannosirkel/deploys/pull/63),
pinned by [Orange #159](https://github.com/hannosirkel/orange/pull/159).
[Orange #160](https://github.com/hannosirkel/orange/pull/160) added the portal-only
Google login flow; the operator's fresh browser check needed one credential
prompt and received a chat reply.
The operator's account and group choices, release observations, and restore
evidence remain in private inventory [#79](https://github.com/hannosirkel/orange-inventory/pull/79)
and [#67](https://github.com/hannosirkel/orange-inventory/pull/67), with the
single sign-in result in [#81](https://github.com/hannosirkel/orange-inventory/pull/81).

## Resume verification

Use the [G4 evidence summary](evidence/g4-summary.md),
[G5 publication summary](evidence/g5-summary.md), and
[acceptance matrix](acceptance.md) to close the remaining browser, access,
profile, alert, and monitor checks. The published route, one-prompt sign-in,
text response, and visible OpenRouter selector are partial evidence;
they do not prove an unlisted account is denied or that every profile is
enforced. Record the exact final observations in private inventory and link the
evidence here. G5 remains open for external route checks after publication.

## Operational limits and recovery

Only the OpenRouter custom endpoint is available for the first text release.
The user and restricted profiles allow the same two text models; admin may use
the configured OpenRouter catalog. File, speech, skills, and conversation
imports are blocked. `/scratch` awaits its own initiative.

Orange's [current commands](https://github.com/hannosirkel/orange/blob/main/docs/current/commands.md)
and [provisioning guide](https://github.com/hannosirkel/orange/blob/main/docs/current/provisioning.md)
own reconciliation and credential lifecycle. Renew an expired OpenBao operator
login with `scripts/openbao-login`; use direct callback mode when the browser is
remote. Do not put credential values into Git or this handoff. Roll back a bad
workload through the pinned GitOps revision or known-good image digest; withdraw
the portal DNS record to stop public exposure quickly. Database restore uses
the explicit guarded lifecycle, never routine reconciliation.
