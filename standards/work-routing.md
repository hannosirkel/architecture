# Work routing standard

Start work in the repository that owns the outcome. Escalate to `architecture`
only when no single repository owns it.

## The four cases

| Situation | Where the work starts | Plan required |
| --- | --- | --- |
| Small routine change | branch, issue, and PR in the owning repository | no |
| Substantial single-repository change | that repository's `docs/working/` | yes |
| One primary repository, light support changes elsewhere | the primary repository's `docs/working/` | yes |
| Several peer repositories, or no clear owner | `architecture/initiatives/active/` | yes |

`architecture` holds a small set of high-value cross-repository initiatives. It
is not a task tracker.

## Worked examples

### Small routine change

Fix a typo in `servitium/docs/current/mtg.md`.

One repository, one file, no design. Branch in `servitium`, open a PR, merge. No
working document.

### Substantial single-repository change

Add a new frontend application to `servitium`.

The change touches routes, build configuration, tests, and documentation, but
nothing outside `servitium`. The plan goes in
[`servitium/docs/working/`](https://github.com/hannosirkel/servitium/tree/main/docs/working).
The decision, if there is one, goes in `servitium/docs/decisions/`.

### One primary repository with support changes

Ship a new `plepic` storefront feature that needs a new Kubernetes environment
variable.

`plepic` owns the outcome. `deploys` takes a small overlay change. The plan
lives in `plepic`. `deploys` gets an ordinary PR, referenced from the plan.

### Several peer repositories

This bootstrap. It changes documentation and checks in twelve repositories and
no single repository owns the result. Its contract and durable state live at
[`initiatives/active/architecture-bootstrap.md`](../initiatives/active/architecture-bootstrap.md)
and its sibling directory.

## Where working plans live

Most repositories keep `docs/working/` in the repository itself.

`orange` is the exception. Its working plans go to the private
`orange-inventory` at `docs/working/`, because Orange's plans routinely name
live hosts, addresses, and identities that must not reach a public repository.
That is a public/private rule, not a layout preference.

## Registering active work

Register substantial active work in
[`universe/repositories.yaml`](../universe/repositories.yaml) under
`notable_local_work`, by path and status.

Register it by link. Do not mirror a journal, ledger, or decision log centrally.
The owning repository keeps the canonical state.

The audit checks that every registered path still exists.
