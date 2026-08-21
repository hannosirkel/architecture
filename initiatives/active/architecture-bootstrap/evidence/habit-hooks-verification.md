# Habit Hooks verification

Contract §7.6 states several facts about Habit Hooks. §13 Phase 1 step 7 requires
confirmation against the installed version. This is that confirmation.

## Version and installation

- Version observed: `habit-hooks 1.3.1`, with `habit-hooks-generic 1.3.1`,
  `habit-hooks-python 1.3.1`, `habit-hooks-typescript 1.3.1`.
- Installed on 2026-08-21 with `uv tool install "habit-hooks[python,typescript]"`.
- `uv` was absent and was installed first (`uv 0.12.5`). It is now a workstation
  prerequisite in its own right.
- Executables installed: `habit-hooks`, `habit-mapper`, `habit-sensors`,
  `habit-snooze`.

## Confirmed as stated in the contract

| Claim | Result |
| --- | --- |
| The tool reads configuration only from inside the project | Confirmed. `habit-hooks init` writes `.habit-hooks/config.toml`. |
| The config is in practice one `plugins = [...]` line | Confirmed. `habit-hooks init` wrote exactly `plugins = ["python", "generic"]`. |
| `habit-sensors --all \| habit-snooze --snooze` baselines a repository | Confirmed. It wrote `.habit-hooks/snooze.json`, a JSON array of issue keys. A snoozed `oversized-file` finding no longer appears in the next run. |
| Plugins exist for typescript and python; ansible and shell have none | Confirmed. PyPI extras are `all`, `java`, `php`, `python`, `typescript`. `habit-hooks-ansible` and `habit-hooks-shell` return 404. |
| `generic` applies everywhere and is never declared | Confirmed as an intent, with one correction below. `habit-hooks-generic` is a hard dependency of `habit-hooks`, not an extra. But it **is** named in `plugins`; `habit-hooks init` writes it into the list. It is not implicit. |
| `uv tool install` extras replace rather than add | Confirmed empirically. After `uv tool install "habit-hooks[python,typescript]"`, running `uv tool install "habit-hooks[python]"` printed `Uninstalled 1 package ... - habit-hooks-typescript==1.3.1`. Name every language in one command. |
| A tool that cannot run must fail loudly and never as a pass | Confirmed. A missing sensor command produces an `incomplete-run` smell and the message "this run did not complete — a tool broke, so a clean result cannot be trusted". |

## Findings that change the plan

### 1. A `generic`-only repository scans nothing and reports success

This is the most important finding. In a repository with no language Habit Hooks
has a plugin for, `habit-hooks init` writes `plugins = ["generic"]` and no
`files`. The next run prints:

```text
habit-sensors: no [files] are configured — name what to scan in .habit-hooks/config.toml; nothing scanned
✅ Habit Hooks: automated checks passed.
```

The `generic` plugin declares no `files` of its own; the language plugins do.
A repository that declares no language therefore gets a green tick for scanning
nothing. That is the exact placebo §7.6 exists to prevent.

**Consequence for the generator:** the generated `.habit-hooks/config.toml` must
carry an explicit `files` list for every repository whose declared languages
bring no plugin — `deploys`, `entpass`, `ai-portal`, `architecture`, and the
ansible/shell-only repositories. Adding `files = ["**/*.yaml", "**/*.md"]` to the
languageless fixture made `oversized-file` fire correctly on both files.

### 2. The prerequisite is not one command

§7.6 describes the install as a single command. The sensors additionally spawn
external tools, declared per plugin:

| Plugin | Sensors | External tools required |
| --- | --- | --- |
| `generic` | `line-count`, `jscpd` | `jscpd` (npm) |
| `python` | `ruff`, `deptry` | `ruff`, `deptry`, `jq` |
| `typescript` | `eslint`, `knip`, `comment` | `node`, `eslint`, `knip`, `ts-morph` (node module), `jq` |

`line-count` is built in and needs nothing. Everything else reports
`incomplete-run` until its tool is present.

Two of these are per-project, not per-workstation: `jscpd`, `eslint`, `knip`, and
`ts-morph` are resolved from the project's `node_modules/.bin` or as node
modules. A repository with no `package.json` — `deploys`, `entpass`,
`architecture`, `orange-inventory` — cannot satisfy `jscpd` that way.

**Consequence for the plan:** `standards/code-quality.md` must name the full
prerequisite set, and the generator must emit
`[sensors.jscpd] disabled = true` for repositories that have no npm project.
`line-count` still runs there, which is the part of `generic` that carries the
coaching value for a documentation or manifest repository.

### 3. `habit-snooze --snooze` also snoozes `incomplete-run`

Baselining a repository whose sensor tools are missing writes the "tool is not
installed" messages into `snooze.json`, permanently hiding the warning that the
run is untrustworthy. **Baseline only after the sensor tools are present**, and
review `snooze.json` for `habit-sensors:` entries before committing it.

## Commands used

```bash
uv tool install "habit-hooks[python,typescript]"
habit-hooks init
habit-hooks --all
habit-sensors --all | habit-snooze --snooze
```
