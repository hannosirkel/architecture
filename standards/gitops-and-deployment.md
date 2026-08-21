# GitOps and deployment standard

An application repository builds an immutable artifact. An approved promotion
writes its digest into `deploys`. Argo CD reconciles `deploys` into the Orange
runtime.

Each step has one owner. Never skip a step by changing live state directly.

## The flow

```text
application repository
  └─ CI builds and verifies an immutable image
       └─ approved promotion updates deploys
            └─ Argo CD reconciles
                 └─ Orange runtime
```

| Stage | Owner | Holds |
| --- | --- | --- |
| Source, tests, image build | the application repository | code and release procedure |
| Deployable desired state | `deploys` | manifests, overlays, pinned digests |
| `Application` objects and cluster bootstrap | `orange` | Ansible-managed Argo CD state |
| Live private values | `orange-inventory` | inventory and variables |

`deploys` is a shared repository with one top-level directory per application.
The repository root is not a deployable Kustomization.

## Promotion

Promote by digest, never by tag. A tag moves; a digest does not.

- A live promotion is merge-promoted.
- A test promotion is label-promoted and its overlay is replaceable.
- The promoting workflow mints a repository-scoped token and checks out only the
  GitOps state it will change.

Roll back by promoting a known-good digest. Do not edit live cluster state.

Never make a lasting manual change to an Argo CD-owned resource. Change its
owning template, defaults, or overlay.

## Validation

Every manifest change renders and schema-checks before it can reach Argo CD:

```bash
kubectl kustomize <overlay> | kubeconform -strict -summary
```

Run the application root's own manifest test alongside it. Those tests carry the
environment boundary, non-root container, default-deny policy, and egress
assertions. They are behaviour tests, not formatting checks.

`kubectl-validate` is the successor candidate if `kubeconform` stops being
maintained.

## Secrets in a public GitOps repository

`deploys` is public. It must never carry a secret value: no OAuth credential, no
private key, no unrestricted token, no private inventory.

**The sanctioned path is External Secrets Operator reading from the OpenBao
instance Orange already runs.** Ansible declares the stores and the
`ExternalSecret` resources; ESO reconciles the namespace-local Kubernetes
Secrets from them.

SOPS with age is the recorded fallback, if that proves impractical.

Name the path rather than leaving agents to improvise. An improvised secret path
in a public repository is the worst failure available here.

## Constraints during governance work

A governance or conformance initiative changes documentation, validation, and
checks only. It does not change an image digest, an overlay's desired state, or
Argo CD behaviour.
