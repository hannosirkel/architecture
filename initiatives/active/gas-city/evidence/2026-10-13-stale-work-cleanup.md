# Gas City stale work cleanup, 2026-10-13

The cleanup checks every kept rig and preserves unfinished work. It does not
advance a trial gate or launch a worker.

## Initial inventory

Five primary Git repositories hold 55 nested worktrees. Worktrees share their
primary repository's Git directory; they are not independent rigs.

| Repository under `~/gascity/rigs/` | Registered name | Nested worktrees | Handling |
| --- | --- | --- | --- |
| `plepic` | `plepic` | 47 | Completed translation branches are merged. |
| `lunar-base-game` | `lunar-base` | 7 | Six fixes are merged; one worktree is dirty. |
| `lunar-base` | unregistered | 1 | Keep the build; its completed review is merged locally. |
| `architecture` | unregistered | 0 | Keep the dirty primary checkout. |
| `hello-gc` | unregistered | 0 | Keep the dirty trial repository and its branches. |

The city has no sessions, running agents, or in-progress claimed work. The
supervisor is running 21 housekeeping orders. The stock order that starts an
LLM worker is skipped.

## Checks and retained work

The check compares each candidate tip with the freshly fetched remote default
branch and verifies its work bead is closed. It rechecks clean state, tip SHA,
and open pull requests before removing a worktree without force.

Keep the dirty public game worktree `lu-cgc`. Keep every primary checkout and
the local-only build repository, its main, and its unmerged design branch.
Keep the real open Plepic glossary issue and ten human messages whose final
resolution is uncertain. Closed records keep their
history; age alone is never a closure reason.

Strict `bd --readonly` listing is unsupported by the proxied Dolt backend.
Ordinary list queries supply the inventory. The record contains no store export,
message bodies, credentials, or private task details.

## Result

| Change | Count |
| --- | --- |
| Clean merged worktrees removed | 54 |
| Their merged local branches removed | 54 |
| Resolved human messages closed | 4 |
| Completed synthetic input convoys closed | 3 |
| Empty startup-health episode closed | 1 |

The local-only review worktree has a closed ACCEPT outcome and a commit merged
into the kept local main. Its primary checkout and unmerged design branch stay.

Independent checks confirm all removed paths and branches are absent. All five
primary HEADs, checked-out branches, and dirty states are unchanged. The eight
closed records retain their explicit outcome reasons. Four message closures
needed the documented assignee override; no gate or unfinished task is closed.

The idle city is stopped and removed from the supervisor registration. The rig
registrations remain in the city configuration. The supervisor service is inactive
and disabled. No worker starts, no trial gate advances, and no store history is
deleted.
