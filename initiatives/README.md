# Initiatives

Cross-repository work that no single repository owns. Work with one clear owner
starts in that repository instead — see
[`standards/work-routing.md`](../standards/work-routing.md).

Each initiative is a contract file plus a directory of durable state beside it.
The contract states the goal and the gates; `state.yaml` records what actually
happened, so a later session can resume without the conversation that produced
it.

## Completed

| Initiative | Completed | Outcome |
| --- | --- | --- |
| [`architecture-bootstrap`](./active/architecture-bootstrap.md) | 2026-08-23 | Established this repository as the governance layer and brought twelve repositories into conformance. State in [`active/architecture-bootstrap/`](./active/architecture-bootstrap/); start from its [`handoff.md`](./active/architecture-bootstrap/handoff.md). |

Completed initiatives stay under `active/` when moving them would break a
resume path that something still references. `architecture-bootstrap` is the
case: its `handoff.md` is linked from this repository's `AGENTS.md`, its
`state.yaml` records the exceptions the audit still reads back, and its
`evidence/` is cited from `standards/`. The status lives in `state.yaml`, not in
the path.

## Planned

| Initiative | Status |
| --- | --- |
| [`ai-portal`](./planned/ai-portal/README.md) | Not started. Read it before deciding whether it belongs here at all — a build owned by one repository starts in that repository. |

## Starting one

```bash
cp -r templates/initiative initiatives/active/<name>
# write initiatives/active/<name>.md as the contract
```

[`templates/initiative/README.md`](../templates/initiative/README.md) describes
what belongs in each file.
