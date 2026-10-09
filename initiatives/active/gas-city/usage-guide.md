# Gas City usage guide

Use this guide to install Gas City on devbox, start work in a new or an
existing repository, and stop the city afterwards. Every command marked
*verified* ran on devbox on 2026-10-09. The record is in
[`evidence/`](./evidence/2026-10-09-install-and-first-runs.md).

Read the [concept](./concept.md) first for the terms.

## Rules for the trial

| Rule | Reason |
| --- | --- |
| Run a live agent only in a repository under `~/gascity/rigs/`. | Agents run with permission bypass. `gc rig add` commits to the checked-out branch. |
| Never register a checkout under `~/app/` as a rig. | The agent-operation standard forbids a commit on a default branch and a write to a shared checkout. |
| Do not push from a rig before gate G3 is approved. | The trial stops before publication. |
| Stop the city when the trial ends. | A running city can start an agent on a schedule. |
| Give a task as a bead title or a formula variable. Do not paste untrusted text into a shell command. | Gas City treats bead text as untrusted data and configuration as trusted code. |

## Install

Devbox already has `tmux`, `git`, `jq`, `flock`, `pgrep`, Claude Code, and
Codex. Add the four tools below. *Verified.*

| Tool | Version | Source | Check |
| --- | --- | --- | --- |
| `gc` | 1.5.0 | `gastownhall/gascity` release | published SHA-256 |
| `bd` | 1.3.1 | `gastownhall/beads` release | published SHA-256 |
| `dolt` | 2.1.7 | `dolthub/dolt` release | none published; record the SHA-256 you got |
| `lsof` | Debian 13 package | `apt` | package signature |

```bash
mkdir -p ~/tmp/gc ~/tmp/bd ~/tmp/dolt

cd ~/tmp/gc
gh release download v1.5.0 -R gastownhall/gascity \
  -p gascity_1.5.0_linux_amd64.tar.gz -p gascity_1.5.0_checksums.txt
grep '  gascity_1.5.0_linux_amd64.tar.gz$' gascity_1.5.0_checksums.txt | sha256sum -c -
tar -xzf gascity_1.5.0_linux_amd64.tar.gz && install -m 755 gc ~/.local/bin/gc

cd ~/tmp/bd
gh release download v1.3.1 -R gastownhall/beads \
  -p beads_1.3.1_linux_amd64.tar.gz -p checksums.txt
grep '  beads_1.3.1_linux_amd64.tar.gz$' checksums.txt | sha256sum -c -
tar -xzf beads_1.3.1_linux_amd64.tar.gz && install -m 755 bd ~/.local/bin/bd

cd ~/tmp/dolt
gh release download v2.1.7 -R dolthub/dolt -p dolt-linux-amd64.tar.gz
sha256sum dolt-linux-amd64.tar.gz
tar -xzf dolt-linux-amd64.tar.gz && install -m 755 dolt-linux-amd64/bin/dolt ~/.local/bin/dolt

sudo apt-get install -y lsof

gc version && bd version && dolt version
```

Dolt needs an author identity before the first city starts:

```bash
dolt config --global --add user.name "$(git config --global user.name)"
dolt config --global --add user.email "$(git config --global user.email)"
```

These tools are installed by hand. The `orange` devbox role does not know
them, so a rebuilt devbox will not have them.

## Create the city

Create the city without starting it. Apply the safe settings. Then start it.
*Verified.*

```bash
gc init --template minimal --providers claude,codex --default-provider claude \
  --no-start ~/gascity/lab
cd ~/gascity/lab
```

Make three changes before the first start:

1. Replace `city.toml` with [`example/city.toml`](./example/city.toml). It
   lowers effort and skips the scheduled order that starts an agent.
2. In `pack.toml`, change the mayor session from `mode = "always"` to
   `mode = "on_demand"`. An always-on session starts an agent at every start.
3. Copy [`example/poc-change.toml`](./example/poc-change.toml) to
   `formulas/poc-change.toml`.

```bash
gc start
gc status
gc session list     # expect: No sessions found.
```

`gc start` installs and enables a `gascity-supervisor` user service.

## Start work in a new repository

*Verified.*

```bash
mkdir -p ~/gascity/rigs/hello-gc && cd ~/gascity/rigs/hello-gc
git init -b main && git commit --allow-empty -m "Initial commit"

cd ~/gascity/lab && gc rig add ~/gascity/rigs/hello-gc

cd ~/gascity/rigs/hello-gc
gc sling hello-gc/claude "Create hello.py that prints a greeting, run it once, \
and commit it on a new branch named poc/hello. Do not push."
```

`gc sling` prints the bead ID. The supervisor starts a Claude Code session
within seconds. The session closes the bead and exits when it finishes. This
task took about one minute.

Address a worker as `<rig>/<provider>`. Each provider in `city.toml` gives
every rig one worker of that name.

## Start work in an existing repository

Register a dedicated clone. Do not register the `~/app/` checkout.

```bash
cd ~/gascity/rigs
git clone https://github.com/hannosirkel/<repo>.git <repo>
cd ~/gascity/lab && gc rig add ~/gascity/rigs/<repo> --start-suspended
```

*Verified to this point with `architecture`.* The clone's `main` is now one
commit ahead of `origin/main`, with a commit named "bd init: initialize beads
issue tracking". Leave that commit local.

The next steps are **not yet verified** on an existing repository. They follow
the commands that worked on the new one.

```bash
gc rig resume <repo>
cd ~/gascity/rigs/<repo>
gc sling <repo>/claude "<task>. Work on a new branch named poc/<name>. Do not push."
```

A fresh clone holds only tracked files. Create the ignored local state the
repository's `AGENTS.md` names, such as a virtual environment, before the task
needs it.

Take the result out of the rig with Git. Fetch the branch into a normal
worktree and continue there under the usual rules:

```bash
git -C ~/app/<repo> fetch ~/gascity/rigs/<repo> poc/<name>:poc/<name>
git -C ~/app/<repo> worktree add ~/app/.worktrees/<repo>/<name> poc/<name>
```

Check that the fetched branch does not contain the `bd init` commit before you
open a pull request from it. A worker that branches from the rig's local
`main` carries that commit.

## Run a multi-step workflow

The example formula has two steps. Claude Code implements a change on a
branch. Codex then reviews it and commits a `REVIEW.md` with a verdict. The
review step waits for the implement step. *Verified.*

```bash
cd ~/gascity/rigs/hello-gc && git checkout main
gc sling hello-gc/claude poc-change --formula \
  --var task="Add greet.py with a function greet(name)" \
  --var branch=poc/greet
```

A step names its worker with `metadata = { "gc.run_target" = "codex" }`. A step
names its prerequisites with `needs = ["implement"]`. Preview a formula
without creating work:

```bash
gc formula show poc-change --var task=x --var branch=y
```

## Watch and intervene

| Need | Command |
| --- | --- |
| City and agent state | `gc status` |
| Running sessions | `gc session list` |
| One bead | `gc bd show <bead-id>` |
| All beads in the current rig | `gc bd list --all` |
| Event trail | `gc events` |
| Token use per run | `gc costs` |
| A worker's screen | `tmux -L lab capture-pane -p -t <session-name>` |
| Scheduled orders | `gc order list` |

The tmux socket name is the city name. `gc session list` shows each session
name in its `TARGET` column.

## Stop

```bash
cd ~/gascity/lab
gc stop
gc supervisor stop
systemctl --user disable gascity-supervisor.service
```

*Verified.* `gc stop` ends every session and unregisters the city. Run
`gc start` in the city directory to bring it back; it re-enables the service.

Use `gc suspend` to keep the city registered but start no new session. In the
trial, a session that was already running continued after `gc suspend`.

## Known problems

| Symptom | Cause | Action |
| --- | --- | --- |
| A `bd.dog` session starts by itself. | The `mol-dog-stale-db` order is enabled, or an open bead from it remains. | Add the order to `[orders] skip`. Close the bead with `gc bd close <id> --force` before you start or resume the city. |
| A Codex step stays open and its bead never starts. | Codex waits at "Trust this folder?" in a directory it has not seen. | Press Enter in the session: `tmux -L lab send-keys -t <session-name> Enter`. This adds the directory to `~/.codex/config.toml`. |
| `gc bd close` refuses with an assignee error. | The bead is assigned to a session that no longer runs. | Add `--force`. |
| The rig is on an unexpected branch. | The worker switched branches in the rig checkout. | Check out the default branch before the next task. |
| `gc init` stops at "Dolt author identity". | Dolt has no global identity. | Run the two `dolt config` commands above, then `gc start`. |

## Remove

```bash
cd ~/gascity/lab && gc stop && gc supervisor stop
gc supervisor uninstall
rm -rf ~/gascity ~/.gc
rm ~/.local/bin/gc ~/.local/bin/bd ~/.local/bin/dolt
```

Move any repository you want to keep out of `~/gascity/rigs/` first. This
sequence is **not yet verified**. It also leaves `~/.beads`, `~/.dolt`,
the `lsof` package, and the trust entry in `~/.codex/config.toml`.
