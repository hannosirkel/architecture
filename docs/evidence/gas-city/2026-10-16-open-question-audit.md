# Gas City open-question audit — 2026-10-16

Six remaining trial questions have answers in the deployed setup or retained
events. One recovery verification remains open. This audit does not approve
unrun trial gates or reopen the completed initiative.

The [question list](../../../initiatives/active/gas-city/open-questions.md)
holds the resulting status. The [closeout](2026-10-15-closeout.md) establishes
that `devbox` owns runtime work after the trial.

## Commit identity — question 3

The deployed issue formula commits with explicit `user.name` and `user.email`
values. Its bot wrapper also exports author and committer identity. The publisher
checks both commit emails against the configured bot address before pushing.

The GitHub commit API for [Lunar Base PR 35](https://github.com/plepicgames/lunar-base/pull/35)
confirmed that its commit author and committer use the bot identity. Coauthor
trailers were not treated as the commit author.

This answers the operational question for the issue workflow. The cause of the
original generic-worker default was not reconstructed or claimed fixed.

## Worktrees — question 4

A disposable Git repository tested the installed `gc worktree ensure` and
`gc worktree verify` commands. The probe supplied the required ownership,
generation, bead, store, branch, base, and path arguments. Both commands passed.

A file written in the linked worktree did not appear in the primary checkout.
The linked branch stayed attached; the primary branch remained `main` and clean.
The probe used no live rig or work bead.

The deployed issue formula uses `git worktree add` from `origin/main` and
requires implementation and verification in that worktree. It does not use
GC's native provisioning helper. Neither finding proves workers cannot edit
other paths.

## Full-store recovery — question 5

Installed `bd export --help` states that JSONL exports issue records, not a
full database. It excludes Dolt branches, commit history, working-set state,
and non-issue tables. `bd backup --help` identifies `backup init`, `sync`, and
`restore` as the supported Dolt-native backup flow.

Backup data exists, but this audit found no completed restore-and-resume drill
for an open workflow. A backup's existence does not establish recovery of its
dependent city or ephemeral records. This verification remains open for `devbox`.

No live store was restored or changed during this audit.

## Second worker — question 6

The archived trial event log explains the second worker at 22:31 on 2026-10-09.
The coding task had closed, but its workflow still contained a drain step.

| Event sequence | Recorded fact |
| --- | --- |
| 134 | Defines `mol-do-work.drain`, dependent on the coding step. |
| 208 | Creates the second session with the drain bead as its trigger. |
| 242 | The second worker starts the drain step at 22:31:53 UTC. |
| 269 | The second worker stops with `drain acknowledged` at 22:32:20 UTC. |

The source is the retained full trial archive, member
`gascity/lab/.gc/events.jsonl`. Only that member was extracted for inspection.
No raw event log or store export is included here.

The [first-runs record](../../../initiatives/active/gas-city/evidence/2026-10-09-install-and-first-runs.md)
said the worker exited "with no work." More precisely, it had no further coding
task; it performed workflow lifecycle work. The original record remains intact.
Why the scheduler selected a new pool slot instead of reusing the first worker
was not established; that distinction does not leave the launch trigger unknown.

## Pull-request stop — question 7

The deployed issue formula closes with a reviewed local branch. The publisher
opens its PR separately and leaves features and operator-risk changes unmerged.
This meets the operational stop-for-review requirement without an open formula
waiting on a PR.

[Lunar Base PR 35](https://github.com/plepicgames/lunar-base/pull/35)
received `needs-operator` at 18:48:43 UTC on 2026-10-13. It remained open until
18:59:22 UTC, when it merged. The runner's operator-risk branch returns after
flagging rather than reaching its automatic merge command.

This does not verify the original three-task, two-repository G3 exercise or a
native formula pause on a PR.

## Rig-local Beads state — question 8

The deployed provisioning role clones dedicated rigs and initializes them
locally. It leaves `.gc/`, `.beads/`, and runtime state outside its source copy.
The Lunar Base rig retains a local `bd init` bootstrap commit. The normal
Lunar Base and architecture checkouts contain no tracked `.beads` files.

The issue formula branches from `origin/main`, rather than carrying a rig's
local bootstrap commit into an application PR. This establishes the deployed
choice; it does not assert that no repository may ever track Beads configuration.

## Tool verification — question 9

The installed `gh` is still 2.46.0 and has no `attestation` command. Attestation
verification was not performed.

The deployed role checks archive SHA-256 values and asserts installed binary
pins. Fresh SHA-256 measurements of `gc`, `bd`, and `dolt` matched the binary
values in the [G0 evidence](../../../initiatives/active/gas-city/evidence/2026-10-09-install-and-first-runs.md).
The adopted deployment therefore already uses checksum and binary-pin
verification. This records the chosen mechanism, not a claim that checksums
provide provenance attestation.
