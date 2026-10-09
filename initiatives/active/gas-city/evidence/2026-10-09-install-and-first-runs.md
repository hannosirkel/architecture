# 2026-10-09 — install and first runs

Gas City 1.5.0 was installed on devbox and completed two pieces of work on a
throwaway repository. Gate G0 is met. One agent started without a request and
was stopped after about one minute.

## Installed

| Tool | Version | Installed to | SHA-256 of the installed binary | Verification |
| --- | --- | --- | --- | --- |
| `gc` | 1.5.0 (`f66474617d2b`) | `~/.local/bin/gc` | `02d9cac82babe4f0316c4764cdb5faadd40c3cae85796c8acbfdcf34b9258376` | archive matched the published checksum |
| `bd` | 1.3.1 (`c1c4b642a`) | `~/.local/bin/bd` | `a8f48d771b9e11eccfced4aed72923b59eda746f7a9b425e7ca1af7a51251653` | archive matched the published checksum |
| `dolt` | 2.1.7 | `~/.local/bin/dolt` | `277bf8fa57b498704fd729b589470a92fa8601318fd2fb88ecf92ac9724243f2` | no published checksum; archive SHA-256 `15983e811341ed94e5d47fbfc41d2f57d8c7aa65eee511d25a3c3fd5477e28e7` |
| `lsof` | 4.99.4 | system package | — | Debian 13 `apt` |

`gh attestation verify` was not run. The `gh` on devbox does not have that
command.

`lsof` was installed with `apt` by hand. The `orange` devbox role does not
list it.

## Other changes to devbox

| Change | Where |
| --- | --- |
| Dolt global author identity set to the configured Git identity | `~/.dolt` |
| City created | `~/gascity/lab` |
| Throwaway rig created | `~/gascity/rigs/hello-gc` |
| Clone of `architecture` registered as a suspended rig | `~/gascity/rigs/architecture` |
| Supervisor user service installed, then stopped and disabled | `~/.local/share/systemd/user/gascity-supervisor.service` |
| Pack cache and supervisor state | `~/.gc` |
| Codex trust entry for the throwaway rig | `~/.codex/config.toml` |

`~/.claude/settings.json` did not change. Gas City keeps its Claude Code hooks
in the city's `.gc/settings.json`.

## Runs

All times are UTC.

| Time | Action | Result |
| --- | --- | --- |
| 22:17 | First `gc start`, stock settings except an on-demand mayor | City started. |
| 22:18 | No action | A `bd.dog` session started by itself for the scheduled order `mol-dog-stale-db`. It ran Claude Code with permission bypass at max effort. |
| 22:19 | `gc stop` | The session ended after five tool calls. All read state or wrote a script to its own scratch directory. |
| 22:25 | Settings changed: Sonnet at medium effort, Codex at medium effort, `mol-dog-stale-db` skipped. City restarted, then resumed from suspension. | The order no longer appears in `gc order list`. |
| 22:28 | No action | The same `bd.dog` session resumed, because its bead was still open. It ran the stale-database scan it had prepared. The scan reported `orphans=0, applied=0, escalated=0`, closed its bead, and the session exited after 21 seconds. Nothing was removed. |
| 22:30 | `gc sling hello-gc/claude "<create hello.py on poc/hello>"` | Bead closed at 22:31. One commit on `poc/hello`. Session exited. |
| 22:31 | No action | A second Claude Code session started for the same pool and exited 33 seconds later with no work. |
| 22:33 | `gc sling hello-gc/claude poc-change --formula ...` | Claude Code closed the implement step at 22:34 with one commit on `poc/greet`. |
| 22:34 | No action | The Codex review session started and waited at its folder-trust prompt. |
| 22:38 | Enter sent to the Codex session | Codex committed `REVIEW.md` with verdict ACCEPT at 22:39. The workflow closed. |
| 22:40 | `gc stop`, `gc supervisor stop`, service disabled | No session, no registered city, service inactive and disabled. |

The two `bd.dog` runs are the only sessions nobody requested. Stopping the city
did not cancel the first one's work: its open bead brought the session back at
the next resume. Close or reassign the bead before a restart.

Launch commands recorded in the event log:

```text
claude --dangerously-skip-permissions --effort medium --model claude-sonnet-5 --settings <city>/.gc/settings.json
codex --dangerously-bypass-approvals-and-sandbox --model gpt-5.5 -c model_reasoning_effort=medium
```

`gc costs` counted 12 invocations, about 5,200 output tokens, and about
628,000 cache-read tokens for the whole trial. It had no price for either
model, so it gave no cost.

## Findings

1. `gc rig add` committed "bd init: initialize beads issue tracking" to the
   checked-out branch. It left `.beads/config.yaml` and `.gitignore` modified.
   In the `architecture` clone, `main` became one commit ahead of
   `origin/main`.
2. Sessions left untracked `.claude/`, `.agents/`, `.codex/`, and `.gc/`
   directories in the rig.
3. The worker worked in the rig checkout and left it on its task branch.
4. Worker commits carried the operating-system user name and a `localhost`
   address. The configured Git identity is the worker bot.
5. The `prune-branches` order fired at start. Its definition says it removes
   stale `gc/*` branches from every rig. No such branch existed.
6. `gc bd close` refused a bead assigned to a dead session until `--force` was
   given.

## Not tested

Recovery after an interrupted launch, store export and restore, work in an
existing repository, a restricted permission mode, and a stop at a pull
request. Gates G1 to G3 cover them.
