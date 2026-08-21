# Ansible

Ansible has no Habit Hooks plugin. These repositories run `generic` for coaching
and gate on native tools.

## Tools

| Job | Tool | Scope |
| --- | --- | --- |
| Lint | `ansible-lint` | the gate |
| YAML lint | `yamllint` | the gate, advisory where it has no baseline |
| Coach | Habit Hooks `generic` plugin | the edit loop |

## The gate

Run both through the repository's existing validation script.

```bash
bash scripts/validate
bash scripts/validate --since main    # narrow to what changed
```

Baseline pre-existing `ansible-lint` findings once:

```bash
ansible-lint --generate-ignore
```

That writes `.ansible-lint-ignore`. Commit it.

`yamllint` has no baseline of its own. Where a repository already passes it over
the whole tree, leave it as a full gate: there is no backlog to baseline. Where
one has a backlog, scope it with `reviewdog` rather than custom code, or run it
advisory-only and say so in the workflow.

Do not write a diff-hunk filter.

## Conventions

These are the portable ones. Apply them in any repository declaring `ansible`.

- Use fully qualified module names.
- Use two-space YAML indentation.
- Use `command` with `argv` when shell parsing is unnecessary.
- Mark an inspection or readiness task `changed_when: false`.
- Validate a nonstandard return code with `failed_when`.
- Pin versions and checksums. Keep resource, storage, and exposure choices
  explicit.

`orange` is the only repository with roles today, and its operational rules stay
with it rather than being copied here: the public/private split between role
defaults and the private inventory's `group_vars/`, the reserved
`inventory-example/` mirror, and the `kubectl diff` before a server-side apply.
Read them in
[`orange/AGENTS.md`](https://github.com/hannosirkel/orange/blob/main/AGENTS.md).

## Verification

For an idempotency fix, run the focused playbook against unchanged state and
require one `changed=0` result.

A successful `--check` run is not a runtime health test. Kubernetes apply and
readiness commands are skipped in check mode.

## Coaching

`generic` supplies `line-count` and `jscpd`. `line-count` is built in.

Writing an `ansible` plugin is a recorded candidate, not current work.
