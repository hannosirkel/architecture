# Gas City proof of concept

Decide whether Gas City replaces enough hand-built orchestration to earn a
place in the software development lab. Run it on devbox against throwaway and
cloned repositories. Record one decision: adopt, keep as an option, or drop.

This initiative is the Gas City half of stage 0 in the factory workflow design.
That design lives in the private `orange-inventory` repository at
`docs/working/2026-09-28-ade-workflow.md`, on branch `ade-workflow`. It names
Gas City as approach B: adopt it only if it replaces more maintenance than it
adds.

## Invocation

```text
resume implementing gas-city.md
```

Read [`gas-city/state.yaml`](./gas-city/state.yaml) first. Continue from its
`next_action`.

## Outcome

| Deliverable | Location |
| --- | --- |
| Concept: what Gas City is and how it maps to the lab | [`gas-city/concept.md`](./gas-city/concept.md) |
| Usage guide: install, start work on a new or existing repository, stop | [`gas-city/usage-guide.md`](./gas-city/usage-guide.md) |
| Example city settings and a two-step formula | [`gas-city/example/`](./gas-city/example/) |
| Dated record of each trial run | [`gas-city/evidence/`](./gas-city/evidence/) |
| The adopt, option, or drop decision | a numbered record in `decisions/` |

## Limits

- The trial runs on devbox only. It deploys nothing and changes no production
  state.
- A live agent works only in a repository under `~/gascity/rigs/`. It never
  works in a checkout under `~/app/`.
- No trial agent pushes a branch or opens a pull request until gate G3 is
  approved.
- The city is stopped when no trial is in progress. The supervisor service
  stays disabled.
- Gas City owns no lab policy. It does not become a second task ledger for
  work that another record already tracks.
- Tool versions stay pinned. A version change is a new evidence record.

## Gates

Each gate needs operator approval before the next one starts. The exit
conditions come from stage 0 of the workflow design.

| Gate | Exit evidence | Status |
| --- | --- | --- |
| G0 Install and first run | Pinned tools installed. One task and one two-step, two-provider workflow complete on a throwaway repository. | Done 2026-10-09 |
| G1 Agent authority | Agents run without permission bypass, or under an account that cannot read operator credentials. | Open |
| G2 Recovery | An interrupted launch resumes without duplicate work. A task finishes after its provider is replaced. The work store exports and restores. | Open |
| G3 Stop at pull request | Three tasks across two repositories, in dependency order, each end at one open pull request and nothing merges. | Open |
| G4 Decision | A decision record compares the result with the CLI and tmux baseline and the GitHub Agentic Workflows trial. | Open |

Budget for G1 to G3: two working days and an LLM budget the operator states
before G1 starts.

## Repositories

| Repository | Role |
| --- | --- |
| `architecture` | This contract, its state, and the final decision. |
| `orange` | Owns devbox provisioning. Receives the tool pins only if G4 says adopt. |
| `orange-inventory` | Holds the workflow design this trial reports to. |

No governed repository is changed before G4. If G4 says adopt, each change is
an ordinary pull request in the owning repository.
