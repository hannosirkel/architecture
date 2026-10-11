# Gas City concept

Gas City is an orchestrator that runs coding agents against a durable work
graph. You write down how a job is done once, as a formula. Gas City turns it
into tasks, starts an agent for each ready task, and holds a task back until
the tasks it needs are closed.

This page covers version 1.5.0 as trialled on 2026-10-09. The upstream
reference is the
[Gas City documentation](https://github.com/gastownhall/gascity/blob/v1.5.0/docs/getting-started/how-gas-city-works.md).

## The six parts

| Part | Answers | What it is |
| --- | --- | --- |
| Agent | Who | A prompt, a provider such as Claude Code or Codex, and a scope. A running agent is a session in tmux. |
| Bead | What | One unit of work with an ID and a status. Tasks, mail, and sessions are all beads. |
| Formula | How | A TOML file of steps and the steps each one needs. |
| Rig | Where | A Git repository registered with the city. Each rig has its own bead store. |
| Pack | Configuration | A directory that declares agents, formulas, and scheduled orders. |
| Event | Observation | An append-only record of what happened. |

A **city** is the pack rooted at one directory on one machine, plus that
machine's settings. A **supervisor** process runs the city and starts and stops
sessions. The Beads CLI, `bd`, stores beads in a Dolt database inside each rig.

## How work moves

1. `gc sling <agent> "<task>"` creates a bead and routes it to an agent.
2. The supervisor sees routed work and starts a session for that agent.
3. The session reads its bead, does the work in the rig, and closes the bead.
4. Closing a bead makes the beads that needed it ready. The supervisor starts
   their sessions.
5. A session with no work left exits.

Slinging a formula does the same for a graph of beads. Progress lives in the
bead store, not in a session. A session that dies leaves its bead open for the
next session.

## How it maps to the lab design

The workflow design names its contract as prepare, claim, launch, observe,
finalize. This table compares that contract with what the trial showed.

| Lab need | Gas City part | Trial result |
| --- | --- | --- |
| Task with dependencies | Bead and formula `needs` | Works. A review step waited for its implement step. |
| Replaceable harness | Provider per agent or per step | Works. Claude Code implemented and Codex reviewed in one workflow. |
| Claim and resume | Bead assignment with a lease | Present. Not yet drilled; see gate G2. |
| Bounded dispatch | Pool size per agent | Present. A second idle session still started after the first task closed. |
| Workspace isolation | Rig directory | Weak by default. The worker edits the rig checkout and switches its branch. |
| Separate worker identity | None built in | Missing. Sessions run as the operator's account. |
| Review and merge gate | None built in | Out of scope for Gas City. The lab gate stays outside it. |
| Status view | `gc status`, `gc events`, a local dashboard | Works on devbox. |
| Cost record | `gc costs` | Reports token counts. It had no price for either model used. |

## What it does not own

Gas City supplies launch, ordering, and recovery. It does not supply policy.
These stay with their current owners:

- Standards and catalogue membership stay in `architecture`.
- Review independence, risk classes, and merge authority stay with the lab
  gate.
- Credentials and devbox provisioning stay with `orange`.

## Risks found in the trial

| Risk | Detail |
| --- | --- |
| Permission bypass is the default | Claude Code starts with `--dangerously-skip-permissions`. Codex starts with `--dangerously-bypass-approvals-and-sandbox`. |
| An agent starts without a request | A stock scheduled order started a maintenance agent one minute after the first `gc start`. Its open bead restarted it after a stop. |
| A rig is written to | `gc rig add` commits a `.beads/` setup to the checked-out branch and edits `.gitignore`. Sessions add untracked `.claude/`, `.agents/`, `.codex/`, and `.gc/` directories. |
| Commits use a new identity | Worker commits carried the operating-system user name and a `localhost` address, not the configured Git identity. |
| A provider can stall | Codex waited at its folder-trust prompt until a person pressed Enter. |

The [usage guide](./usage-guide.md) states the working rule for each risk. The
[open questions](./open-questions.md) list what the next gates must settle.
