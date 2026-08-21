# Code quality standard

Two mechanisms with different jobs. Do not confuse them.

| Mechanism | Job | Runs | Gates a merge |
| --- | --- | --- | --- |
| Habit Hooks | coaches the agent while it edits | the workstation, inside the edit loop | no |
| Linters and static analysis | verifies the result | repository CI, on changed work | yes |

The purpose is to make *future* changes compliant. It is not to clean up
existing code, and no initiative does that in bulk.

## The gate

The gate is the repository's own linter and static analysis, run through the
lightest mechanism the repository already has. Do not add a task runner or a
package manager for uniformity.

**The gate blocks on new work only, using each linter's own baseline.**

| Tool | Baseline mechanism |
| --- | --- |
| ESLint | bulk suppressions file |
| `ruff` | `ruff check --add-noqa` |
| `ansible-lint` | `ansible-lint --generate-ignore` into `.ansible-lint-ignore` |
| `shellcheck` | narrow `# shellcheck disable=SCxxxx` directives |
| `yamllint` | none; scope with `reviewdog`, or run advisory-only and say so |

Record today's findings once, commit the file, and every later run reports only
what the change introduced. Touching a file does not make its history your
problem.

**Do not build a diff-hunk filter.** Parsing linter output and mapping it onto
git hunks is a bespoke harness for a problem the tools already solve.

**Never make Habit Hooks a required CI check.** A coach that fails builds becomes
a target, and a target gets gamed. That is the exact failure it exists to
prevent.

Formatters run on changed files only. Repository-wide reformatting destroys the
review value of every later diff.

A tool that cannot run — missing detector, bad config, unresolvable base ref —
fails loudly and distinctly. Never report it as a pass.

Working the backlog down is ordinary follow-up work in the owning repository,
routed by [`work-routing.md`](./work-routing.md).

## The coach

Habit Hooks turns a linter finding into an actionable guide while the agent is
still editing. It is advisory by design.

Run `habit-hooks` before declaring an edit done.

Do not track which workstation has it. Do not build attestation. Conformance
checks that the instruction and the generated config are present and correct.
Nothing more. The gate is what actually holds, and it does not depend on any of
this.

### Workstation prerequisites

Habit Hooks is a workstation tool, not a repository dependency. Install it once:

```bash
uv tool install "habit-hooks[python,typescript]"
```

**Name every language in that one command.** `uv tool install` replaces extras
rather than adding them: a later install naming a different extra silently
removes this one. Verified against version 1.3.1.

The sensors spawn external tools. Without them a run reports `incomplete-run`,
never a pass:

| Plugin | Sensors | Needs |
| --- | --- | --- |
| `generic` | `line-count`, `jscpd` | `jscpd` — `line-count` is built in and needs nothing |
| `python` | `ruff`, `deptry` | `ruff`, `deptry`, `jq` |
| `typescript` | `eslint`, `knip`, `comment` | `node`, `eslint`, `knip`, `ts-morph`, `jq` |

`jscpd`, `eslint`, `knip`, and `ts-morph` resolve from the project's
`node_modules/.bin`. A repository with no npm project cannot supply them; see
the generated configuration below.

### Configuration is generated

A repository owns no Habit Hooks rules. It owns one generated file,
`.habit-hooks/config.toml`, materialised from the catalogue's `languages` plus
`generic`. It is never hand-maintained. Regenerate it with:

```bash
tooling/universe sync-baseline <repo>
```

The generated file always names `files` explicitly. This is not optional. The
`generic` plugin declares no `files` of its own, so a repository whose languages
bring no plugin scans nothing and prints:

```text
habit-sensors: no [files] are configured — nothing scanned
✅ Habit Hooks: automated checks passed.
```

A green tick for scanning nothing is a placebo. The generator prevents it.

The generated file disables `jscpd` where there is no npm project to resolve it
from. `line-count` still runs there, which is the part of `generic` that catches
oversized files in YAML and Markdown.

Three repositories declare `typescript` for JavaScript and hold no `.ts` file.
The generated `files` widens the plugin's default to `**/*.js` and `**/*.mjs`.
Without that the coach finds nothing in any of them.

### Snooze baselines

`.habit-hooks/snooze.json` names a repository's own files, so it is
repository-owned truth rather than policy. Where a repository is worth
baselining:

```bash
habit-sensors --all | habit-snooze --snooze
```

**Install the sensor tools first.** `habit-snooze --snooze` also snoozes the
`incomplete-run` warning, which permanently hides the fact that a run was
untrustworthy. Read `snooze.json` for `habit-sensors:` entries before committing
it.

Do not invent a parallel baseline format.

### Coaching and the gate differ in scope, deliberately

The snooze ratchet returns a file's whole backlog the moment the file is
touched. The agent therefore *sees* more than the gate *blocks* on. The coach
shows the neighbourhood; the gate judges the diff.

An agent may fix what it was shown. Put backlog fixes in a separate commit from
the change that surfaced them, or leave them for later without apology. Never
mix a cleanup sweep into a feature diff.

## Languages

Each language document names the concrete tools, the CI gate, and the coaching
plugin.

- [`languages/typescript.md`](./languages/typescript.md)
- [`languages/python.md`](./languages/python.md)
- [`languages/ansible.md`](./languages/ansible.md)
- [`languages/shell.md`](./languages/shell.md)

Ansible and shell have no Habit Hooks plugin. Those repositories run `generic`
for coaching and gate on native tools. Writing plugins for either is a recorded
candidate, not current work.

Adding a language is a small deliberate change: write
`standards/languages/<language>.md`, declare it in the catalogue, add the gate.
Do not write a document for a language nothing declares.

## Testing

Use the minimum testing that demonstrates the behaviour and protects against a
likely regression.

- Test durable behaviour, not file existence or incidental formatting.
- Add a focused test for new logic in the same commit.
- A documentation-only change needs static checks, not a new test.
- Remove a test that only repeats lintable syntax or an obvious implementation
  detail.
- Do not pursue exhaustive line or combination coverage.

A high-risk change needs verification proportional to its operational impact.

## Review cutoff

Prioritise what affects correctness or a decision.

### Must fix

- A contradiction between documentation and code.
- Incorrect ownership, exposure, secret, backup, or recovery behaviour.
- A statement that could cause an unsafe deployment.
- Missing information needed to operate or extend the system safely.
- A validation script that fails, or that passes without checking anything real.
- A credential or per-environment value committed to a repository.

### Optional

- An edge case that does not affect core operation.
- A wording improvement next to a required edit.
- An additional example with clear maintenance value.

### Do not fix

- A stylistic preference alone.
- Historical narration that belongs in Git.
- Detail directly discoverable from obvious code.
- An explanation that raises maintenance cost without changing a decision.

Stop when no must-fix issue remains.
