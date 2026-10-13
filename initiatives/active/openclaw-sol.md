# OpenClaw model configuration

Configure the Mihkel and Meeme bots to use `gpt-6.1-sol` with medium reasoning effort.
Verify that both runtimes use the latest stable OpenClaw release.

Orange owns the OpenClaw installation, configuration template, and service.
Its private inventory owns per-bot configuration values.
The Mihkel and Meeme repositories own bot workspace content and need no installation changes.

## Execution

The operator requested parallel subagents on 2026-10-13.
The primary agent coordinates rollout and verifies the result.
The `openclaw_upgrade` subagent prepares the Orange and inventory changes in isolated worktrees.
Existing dirty work, secrets, primary checkout branches, and unrelated settings stay protected.

## Pull requests

Prepare both changes before merging either. Merge Orange first, then its inventory consumer.

- [x] Orange: update `roles/openclaw/defaults/main.yml`, `roles/openclaw/templates/openclaw.json.j2`, `tests/openclaw_templates.yml`, and `docs/current/provisioning.md`. Set the supported model identifier and configurable medium reasoning default. Verify template contracts, native repository gates, and Habit Hooks. Open a pull request.
- [x] Orange inventory: inspect both bot selectors for model, version, and thinking overrides. No overrides exist on the fetched default branch. The shared Orange defaults supply both configurations; no inventory change is needed.

- [x] Orange compatibility: remove the retired `default` marker in `roles/openclaw/templates/openclaw.json.j2`; verify the sole-agent schema in `tests/openclaw_templates.yml`; update `docs/current/provisioning.md`. Full local and required CI checks passed in [PR 171](https://github.com/hannosirkel/orange/pull/171).

## Rollout verification

The latest stable upstream release observed on 2026-10-13 is `2026.10.3`.
Orange already pins that release. Verify the installed version before changing a pin.
Apply the reviewed owner configuration through the documented Ansible procedure.
Check both services, installed versions, model selectors, and reasoning defaults.
Record blocked runtime checks explicitly; configuration alone does not prove rollout.

## Completion

[PR 170](https://github.com/hannosirkel/orange/pull/170) and PR 171 are merged.
Both runtime probes and independent read-only checks passed.
The [dated evidence](../../docs/evidence/openclaw-sol-2026-10-13.md) retains the result.
Operational defaults remain in Orange. No row or rollout issue remains open.
