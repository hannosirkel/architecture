# Open questions

Each question belongs to the gate that must answer it.

| # | Question | Gate |
| --- | --- | --- |
| 1 | Can Claude Code and Codex workers complete a task in a restricted permission mode, with an allowlist for `gc`, `bd`, and `git`? | G1 |
| 2 | Can the city run under a separate devbox account that cannot read the operator's credential directories? | G1 |
| 3 | Why do worker commits use the operating-system user and `localhost` instead of the configured Git identity, and which setting corrects it? | G1 |
| 4 | Does a per-task worktree (`gc worktree`) keep a worker out of the rig checkout? | G2 |
| 5 | Does `bd` export and restore a rig store completely, including open workflow state? | G2 |
| 6 | Why did a second worker session start after the only task had closed? | G2 |
| 7 | Can a formula end at an open pull request and wait there without a merge step? | G3 |
| 8 | Should the `.beads/` setup be merged into a governed repository, or stay in a local clone only? | G4 |
| 9 | `gh` on devbox is too old for `gh attestation verify`. Is a checksum enough for the pinned tools? | G4 |
