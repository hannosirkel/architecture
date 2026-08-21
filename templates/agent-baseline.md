<!-- BEGIN MANAGED ARCHITECTURE BASELINE -->
<!-- Generated from hannosirkel/architecture. Do not edit inside these markers.
     Regenerate with: tooling/universe sync-baseline {{repo}} -->

Governed by [`architecture`]({{architecture_url}}).

| | |
| --- | --- |
| Profile | `{{profile}}` |
| Visibility | declared {{declared_visibility}}, currently {{current_remote_visibility}} |
| Public-safe required | {{public_safe_required}} |
| Languages | {{languages_display}} |

**Standards that apply here.** Read a standard before you change something it
governs.

{{standards_lines}}{{language_standards_line}}
**Never commit to a default branch.** Work in `~/app/.worktrees/{{repo}}/<task>`,
branch from `origin/{{default_branch}}`, and open a pull request.

**{{public_safety_line}}** Never commit a password, token, key, kubeconfig,
rendered Secret, or live export. No repository here holds a secret value, and a
private one is no exception.

**Run `habit-hooks` before declaring an edit done.** If it is not on `PATH`:

```bash
uv tool install "{{habit_hooks_package}}"
```

Name every language in that one command. A later install naming a different
extra silently replaces this one. Then re-run `habit-hooks`.

<!-- END MANAGED ARCHITECTURE BASELINE -->
