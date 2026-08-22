---
name: audit-universe
description: Use when the operator asks for the state of the managed universe — which repositories lag the central agent baseline, which declare a language they no longer contain, where observed visibility differs from declared, which governance files are missing or hand-edited, which registered working plans have disappeared, or where commits reached a default branch without a pull request. Invoke explicitly; it never runs on a schedule and it never fixes anything.
---

# Audit the managed universe

Report the state of every catalogued repository. Report only. Every fix this
audit implies is ordinary work, routed by
[`standards/work-routing.md`](../../standards/work-routing.md).

This skill is a thin wrapper over `tooling/universe`. The logic lives there, so
the skill stays short and the CLI stays testable.

## When to run it

- After any change to the central baseline, the standards, or the templates.
- Before starting a cross-repository initiative.
- When a repository joins the universe.
- Whenever the operator wants the picture.

There is no scheduler, cron, daemon, or watcher, by decision. See
[`decisions/005`](../../decisions/005-audit-skill-lives-in-architecture.md).

## Steps

1. **Go to the architecture repository.** Every command below runs from its
   root.

   ```bash
   cd ~/app/architecture
   ```

2. **Validate the catalogue first.** A finding here invalidates everything
   after it.

   ```bash
   tooling/universe validate
   ```

   Exit code 2 means the tool could not run. Stop and report that; never treat
   it as a pass.

3. **Fetch every repository, without touching a working tree.** The audit reads
   local checkouts, so a stale checkout produces a stale answer.

   ```bash
   python3 - <<'EOF'
   import os, subprocess, yaml
   catalogue = yaml.safe_load(open("universe/repositories.yaml"))
   for name, entry in catalogue["repositories"].items():
       path = os.path.expanduser(entry["local_path"])
       if os.path.isdir(os.path.join(path, ".git")):
           subprocess.run(["git", "-C", path, "fetch", "--quiet", "origin"])
       else:
           print(f"{name}: no checkout at {entry['local_path']}")
   EOF
   ```

   Never `pull`, `checkout`, `stash`, `reset`, or `clean`. Another agent may be
   working in that tree, and the audit does not need it to be current.

   A repository the audit cannot export reports `cannot-read-branch`. That is a
   finding, never a pass.

4. **Run the audit.**

   ```bash
   tooling/universe audit
   ```

   Add repository names to narrow it. A name outside the catalogue is refused
   with exit code 2, not reported as a failure: a repository outside the
   catalogue is out of scope by construction.

   Add `--path <dir>` to audit a worktree instead of the branch, before pushing
   it. That is the only mode that reads uncommitted work.

   A catalogued repository this universe does not govern — a fork following
   upstream's conventions — prints `not governed; conformance skipped` and is
   counted out of the total. It is never reported as clean.

5. **Compare declared visibility against GitHub.** The CLI reads the catalogue,
   not the API.

   ```bash
   python3 - <<'EOF'
   import json, subprocess, yaml
   catalogue = yaml.safe_load(open("universe/repositories.yaml"))
   for name, entry in catalogue["repositories"].items():
       out = subprocess.run(
           ["gh", "repo", "view", f"hannosirkel/{name}", "--json", "visibility"],
           capture_output=True, text=True)
       if out.returncode:
           print(f"{name}: could not read visibility"); continue
       actual = json.loads(out.stdout)["visibility"].lower()
       recorded = entry["current_remote_visibility"]
       if actual != recorded:
           print(f"{name}: GitHub says {actual}, catalogue says {recorded}")
   EOF
   ```

   A difference between `declared_visibility` and `current_remote_visibility` is
   not a finding on its own. `orange` is declared public and is currently
   private, deliberately. A difference between the catalogue and GitHub is a
   finding: the catalogue is out of date.

6. **Report.** Group the findings by repository. For each one give the check,
   the detail, and the fix the tool named. Say plainly which repositories were
   clean.

## What it does not do

- It does not fix anything.
- It does not change a branch, a checkout, or a visibility.
- It does not open a pull request.
- It does not run on a schedule.

## What runs in CI instead

`architecture`'s own CI runs part of this on every push to `main`: catalogue
validity, link checking, layout, and a regeneration of every repository's
expected managed section at the push's parent and at its head, reporting which
repositories the change just invalidated.

That comparison is between two generated outputs, so it needs no clones and no
token. Comparing against what those repositories actually contain needs clones,
five of them private, and stays here in the manual audit.
