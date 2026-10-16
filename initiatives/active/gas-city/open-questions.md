# Open questions

Only full-store recovery remains unverified. The trial is complete by operator
direction; this remaining verification belongs to `devbox`, not a reopened gate.
The [2026-10-16 audit](../../../docs/evidence/gas-city/2026-10-16-open-question-audit.md)
records the checks and their limits.

| # | Open verification | Original gate |
| --- | --- | --- |
| 5 | Can full-store backup and restore recover an open workflow and let GC resume it, including required ephemeral and city state? | G2 |

`bd export` is an issue interchange format, not a full backup. The supported
backup commands exist, but no restore-and-resume drill was verified in this audit.

## Answered questions

| # | Subject | Verified answer |
| --- | --- | --- |
| 3 | Worker commit identity | The deployed issue workflow sets the bot identity explicitly and rejects mismatched authors or committers before publication. A published change confirms both identities. This does not establish a fix to generic worker defaults. |
| 4 | Per-task worktrees | A disposable `gc worktree ensure`/`verify` probe kept task edits in an attached worktree and left the primary checkout clean. The deployed issue formula uses explicit Git worktrees. |
| 6 | Second worker after coding finished | Archived events show it started for the workflow's drain step. It had lifecycle work, although no further coding task. |
| 7 | Stop for pull-request review | The formula finishes locally; the publisher opens the PR and leaves operator-risk changes for a maintainer. A published change demonstrates the stop. A native formula waiting on a PR was not tested. |
| 8 | Beads setup in application repositories | The deployed setup keeps Beads state and bootstrap commits in dedicated rig clones. It does not merge them into application repositories. |
| 9 | Pinned-tool verification | Deployment verifies archive checksums and installed binary pins. This is the adopted verification path; attestation remains unavailable in the installed `gh`. |
