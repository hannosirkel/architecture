# Python

## Tools

| Job | Tool | Scope |
| --- | --- | --- |
| Format | `ruff format` | changed files only |
| Lint | `ruff check` | the gate |
| Dependency hygiene | `deptry` | coaching only |
| Coach | Habit Hooks `python` plugin | the edit loop |

`ruff` replaces `black`, `isort`, `flake8`, and `pyupgrade`. Do not add them.

## The gate

Run `ruff check` through the repository's existing validation script, or as one
CI step where the repository has no script.

```bash
ruff check .
ruff format --check <changed files>
```

Baseline pre-existing findings once:

```bash
ruff check --add-noqa .
```

Commit the result. Every later run reports only what the change introduced.
Record the count of added directives in the pull request.

Do not reformat the repository to satisfy a newly introduced rule.

## Tests

Use the runner the repository already uses. `unittest` and `pytest` are both
present in this universe; do not convert one to the other as a side effect of
other work.

## Coaching

The `python` plugin runs `ruff` and `deptry`. It needs `ruff`, `deptry`, and
`jq` on `PATH`.

Its guides cover `high-complexity` and `swallowed-exception`. The `generic`
plugin supplies the rest.

`deptry` runs in coaching only. It is not a merge gate: an unused declared
dependency is worth knowing about and is not worth blocking a merge for.
