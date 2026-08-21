# Shell

Shell is easy to overlook and load-bearing here. `myskills` is entirely bash,
most repositories funnel CI through a bash validation script, and some test
harnesses are bats.

Shell has no Habit Hooks plugin. These repositories run `generic` for coaching
and gate on native tools.

## Tools

| Job | Tool | Scope |
| --- | --- | --- |
| Lint | `shellcheck` | the gate |
| Format | `shfmt` | optional, changed files only, where the repository wants it |
| Coach | Habit Hooks `generic` plugin | the edit loop |

## Finding the shell

Shell does not announce itself. It hides in `scripts/`, in `install`, and in
test harnesses.

Lint every file that is any of:

- named `*.sh` or `*.bats`;
- executable with a `bash` or `sh` shebang;
- named in a workflow as `bash <file>`.

A repository whose only shell is `scripts/validate` still declares `shell`.

## The gate

```bash
shellcheck <files>
```

Run it through the repository's existing validation script where one exists, and
as one CI step where none does.

`shellcheck` has no baseline file. Baseline a pre-existing finding with the
narrowest directive that silences it:

```bash
# shellcheck disable=SC2086
```

Record the count and the rule codes in the pull request. Say that they are
baselined pre-existing findings, not fixes.

Use `.shellcheckrc` only for a rule that is wrong for the whole repository. Do
not use it to hide a backlog.

**Do not change a script's behaviour to satisfy a newly introduced linter.**

## Conventions

- Start every script with `set -euo pipefail`.
- Quote every expansion unless you have a stated reason not to.
- Prefer `printf` to `echo` for anything but a fixed string.
- Resolve the script's own directory rather than assuming the caller's:

  ```bash
  root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
  ```

- Clean up a temporary directory with `trap ... EXIT`.
- Never edit a line containing JavaScript or a URL with `sed s///`.

## Coaching

`generic` supplies `line-count` and `jscpd`. `line-count` is built in and runs
without any external tool, which matters: several shell repositories have no npm
project and therefore no `jscpd`.

Writing a `shell` plugin is a recorded candidate, not current work.
