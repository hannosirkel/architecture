# AI Portal — planned

Registered, not started. The repository exists and is public; the product is
unimplemented and its `main` has no commits.

**Do not begin the build from this record.** Implementation starts as a separate
approved initiative.

## Product boundary

`ai.future.ee` and its subprojects, including LibreChat integration and the
agentic and manual Scratch playground.

## Ownership

| Role | Repository |
| --- | --- |
| Owning application repository | `ai-portal` |
| Deployable desired state | `deploys` |
| Cluster bootstrap and Argo CD `Application` objects | `orange` |
| Live private values | `orange-inventory` |
| Reusable agent skills, if any | `myskills` |

`ai-portal` must not hold family identities, group membership, provider keys,
OAuth sessions, or private infrastructure variables.

## Current state

- The GitHub repository exists and is public.
- `main` is unborn on both the remote and the local clone.
- The managed-universe bootstrap gives it `README.md`, `AGENTS.md`, and
  `CLAUDE.md`, pushed as an initial commit under the empty-repository exception
  in [`standards/agent-operation.md`](../../../standards/agent-operation.md).
- It declares no language, because it contains none.

## Starting the real initiative

1. Write the contract at `initiatives/active/ai-portal.md`, from
   [`templates/initiative/`](../../../templates/initiative/README.md).
2. Decide whether it belongs here at all. A build owned by one repository starts
   in that repository; see
   [`standards/work-routing.md`](../../../standards/work-routing.md). It belongs
   here only if the boundaries between `ai-portal`, `deploys`, `orange`, and
   `orange-inventory` are genuinely undecided.
3. Update the `ai-portal` catalogue entry's `languages` and `lifecycle` as the
   product acquires them.

## Existing implementation contract

None found during the bootstrap audit. If one exists outside these
repositories, record its location here before starting.
