# Declared languages: the evidence

Counts exclude `.git`, `node_modules`, `.venv`, and `.next`. Collected
2026-08-21.

| Repository | typescript | python | ansible | shell | Declared |
| --- | --- | --- | --- | --- | --- |
| architecture | – | planned | – | – | `python` |
| orange | – | 37 `.py` | `roles/`, 403 YAML | 16 bash | `ansible`, `python`, `shell` |
| orange-inventory | – | – | `hosts.yml`, `group_vars/`, `host_vars/` | 5 bash | `ansible`, `shell` |
| deploys | – | – | – | 3 bash | `shell` |
| myskills | – | – | – | 3 bash, bats tests | `shell` |
| plepic | 687 `.ts`/`.tsx` | – | – | 4 bash | `typescript`, `shell` |
| servitium | 28 `.ts`/`.tsx`/`.js` | – | – | 5 bash | `typescript`, `shell` |
| robobook | – | 32 `.py` | – | none | `python` |
| nomadtty | 33 `.js`/`.mjs` | – | – | `install.sh`, `docker-entrypoint.sh` | `typescript`, `shell` |
| mihkel | 6 `.js` | 2 `.py` | – | `scripts/validate`, bats | `typescript`, `python`, `shell` |
| ai-portal | – | – | – | – | none |
| entpass | – | – | – | – | none |

## Notes on individual calls

**`deploys` is not languageless.** The contract uses it as the example of an
empty `languages` list. Evidence contradicts that: `plepic/tests/manifests.sh`,
`servitium/tests/manifests.sh`, and `.githooks/pre-commit` are bash, and the
manifest tests carry the environment-boundary and non-root assertions. Leaving
`shell` undeclared would leave those files with no gate.

**`nomadtty` and `mihkel` declare `typescript` for JavaScript.** §7.6 defines
`typescript` as including Node.js. Neither repository has a `.ts` file. This
matters for the gate: `eslint` covers `.js`, but the Habit Hooks typescript
plugin scans `**/*.ts` and `**/*.tsx` only, so its coaching finds nothing in
either repository until the generated config widens `files`. See
`habit-hooks-verification.md`.

**`orange` YAML is ansible, not a fourth language.** `yamllint` and
`ansible-lint` both come from the ansible standard, so 403 YAML files need no
separate declaration.

**`architecture` declares `python` ahead of evidence.** `tooling/universe` lands
in Phase 2, which precedes every repository's wave 2. Re-check at Phase 6.

**`mihkel` uses bats.** `tests/pre_push.bats` is exercised by `scripts/validate`
and CI installs bats for it. Shell is load-bearing there, not incidental.
