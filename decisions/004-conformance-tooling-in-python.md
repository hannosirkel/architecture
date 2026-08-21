# 004. Write the conformance tooling in Python

- **Date:** 2026-08-21
- **Status:** accepted

## Context and problem statement

The conformance tool parses YAML, renders text templates, compares generated
output against files in other repositories, and reports. It needs a language.

## Considered options

- Bash, reusing the language `myskills` already uses.
- Python, which the agent-coaching toolchain already requires.
- A compiled language.

## Decision

Write `tooling/universe` in Python 3, as one CLI with three subcommands:
`validate`, `audit`, and `sync-baseline`.

## Rationale

Python suits a program that parses YAML and generates text. Bash does not: YAML
parsing in bash means either a dependency on `yq` or a hand-rolled parser, and
marker-delimited text replacement in `sed` is exactly the class of edit this
universe already bans elsewhere.

Habit Hooks is Python and is already a workstation prerequisite, so `uv` and a
Python 3 interpreter are present anyway.

**Name the cost.** `myskills` is entirely bash. This decision adds a second
language to the tooling surface rather than reusing the one that exists. That is
the trade being made. It is accepted because the two tools have different jobs
and neither imports the other.

One program with three subcommands, rather than three scripts, because all three
already needed the same catalogue parsing, profile resolution, and template
rendering.

## Consequences

- `architecture` declares `python` in its own catalogue entry and gates on
  `ruff`.
- The tool has behaviour-based tests. It does not become a package until
  something outside `architecture` needs to import it.
- No database, dashboard, web UI, event system, or daemon is built for
  repository governance.
- Do not relitigate this per script.
