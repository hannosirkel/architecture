<!-- BEGIN MANAGED ARCHITECTURE BASELINE -->
<!-- Generated from hannosirkel/architecture. Do not edit inside these markers.
     Regenerate with: tooling/universe sync-baseline {{repo}} -->

Governed by [`architecture`]({{architecture_url}}).

| | |
| --- | --- |
| Profile | `{{profile}}` |
| Visibility | declared {{declared_visibility}}, currently {{current_remote_visibility}} |
| Languages | {{languages_display}} |

**Standards that apply here.** Read a standard before you change something it
governs.

{{standards_lines}}{{language_standards_line}}
**Never commit to a default branch.** Work in `~/app/.worktrees/{{repo}}/<task>`.
Branch from `origin/{{default_branch}}`. Open a pull request.

**A working plan for this repository goes in {{working_plans}}.** A change
spanning several repositories with no clear owner starts in `architecture`
instead.

**{{public_safety_line}}** Never commit a password, token, key, kubeconfig,
rendered Secret, or live export. No repository in this universe holds a secret
value, and a private one is no exception.

**Run `habit-hooks` before declaring an edit done.** If it is not on `PATH`:

```bash
uv tool install "{{habit_hooks_package}}"
```

That command names every language plugin **this universe** uses, not this
repository's. Install it whole: a later install naming fewer extras silently
removes the rest.

<!-- END MANAGED ARCHITECTURE BASELINE -->
