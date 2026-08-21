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

These are Orange's, and Orange is the only repository with roles. They are
recorded here because a second Ansible repository would inherit them.

- Use fully qualified module names.
- Use two-space YAML indentation.
- Put reusable behaviour in public role defaults. Put live fleet and
  host-category choices in the private inventory's `group_vars/`, with a
  reserved structural counterpart in `inventory-example/`.
- Use `command` with `argv` when shell parsing is unnecessary.
- Mark an inspection or readiness task `changed_when: false`.
- Validate a nonstandard return code with `failed_when`.
- Before a server-side apply, run the matching `kubectl diff` and apply only
  when it returns `1`.
- Do not treat `serverside-applied` as proof of change. `kubectl` emits it for
  unchanged resources.
- Pin versions and checksums. Keep resource, storage, and exposure choices
  explicit.

## Verification

For an idempotency fix, run the focused playbook against unchanged state and
require one `changed=0` result.

A successful `--check` run is not a runtime health test. Kubernetes apply and
readiness commands are skipped in check mode.

## Coaching

`generic` supplies `line-count` and `jscpd`. `line-count` is built in.

Writing an `ansible` plugin is a recorded candidate, not current work.
