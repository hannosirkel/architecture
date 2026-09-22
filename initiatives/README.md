# Initiatives

Cross-repository work that no single repository owns. Work with one clear owner
starts in that repository instead — see
[`standards/work-routing.md`](../standards/work-routing.md).

Each active initiative is a contract file plus a directory of durable state
beside it. The contract states the goal and gates; `state.yaml` records progress.

## Completed

| Initiative | Completed | Outcome |
| --- | --- | --- |
| [`architecture-bootstrap`](./active/architecture-bootstrap.md) | 2026-08-23 | Established this repository as the governance layer and brought twelve repositories into conformance. State in [`active/architecture-bootstrap/`](./active/architecture-bootstrap/); start from its [`handoff.md`](./active/architecture-bootstrap/handoff.md). |

Completed initiatives stay under `active/` when moving them would break a
resume path that something still references. `architecture-bootstrap` is the
case: its `handoff.md` is linked from this repository's `AGENTS.md`, its
`state.yaml` records the exceptions the audit still reads back, and its
`evidence/` is cited from `standards/`. The status lives in `state.yaml`.

## Active

| Initiative | Status |
| --- | --- |
| [`ai-portal`](./active/ai-portal.md) | Portal/chat plan at G1; new Access-gated identity-provider boundary needs operator approval. |

## Planned

| Initiative | Status |
| --- | --- |
| [`scratch-hub`](./planned/scratch-hub/README.md) | Follows portal/chat; independent manual Scratch release. |
| [`scratch-ai`](./planned/scratch-ai/README.md) | Follows Scratch hub; independent controlled AI-edit release. |
| [`build-feedback-loop`](./planned/build-feedback-loop/README.md) | Not started. Simplify Big Build state and promote real-use failures into future checks without adding an eval platform. |

## Starting one

```bash
cp -r templates/initiative initiatives/active/<name>
# write initiatives/active/<name>.md as the contract
```

[`templates/initiative/README.md`](../templates/initiative/README.md) describes
what belongs in each file.
