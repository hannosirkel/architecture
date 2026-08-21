# TypeScript

Covers TypeScript and Node.js JavaScript. Three repositories declare
`typescript` and hold no `.ts` file; the rules below apply to their `.js` and
`.mjs` all the same.

## Tools

| Job | Tool | Scope |
| --- | --- | --- |
| Format | `prettier` | changed files only |
| Lint | `eslint` | the gate |
| Static analysis | `tsc --noEmit` | the gate, where a `tsconfig.json` exists |
| Coach | Habit Hooks `typescript` plugin | the edit loop |

## The gate

Run `eslint` and `tsc --noEmit` through the repository's existing validation
script. Do not add a task runner.

```bash
npm ci
bash scripts/validate
```

Baseline pre-existing findings with an ESLint bulk suppressions file. Generate
it once, commit it, and every later run reports only what the change introduced.

Do not reformat the repository to satisfy a newly introduced rule.

## Coaching

The `typescript` plugin runs `eslint`, `knip`, and a comment sensor. It needs
`node`, `eslint`, `knip`, `ts-morph`, and `jq`. `eslint`, `knip`, and `ts-morph`
resolve from the project's `node_modules`.

Its guides cover `explicit-any`, `loose-equality`, `non-const-binding`,
`non-null-assertion`, `redundant-type-annotation`, `test-only-dead-code`,
`unused-class-member`, and `var-declaration`.

The plugin scans `**/*.ts` and `**/*.tsx` by default. The generated
`.habit-hooks/config.toml` widens `files` to `**/*.js` and `**/*.mjs` for a
repository whose TypeScript is JavaScript.

## Version constraints

Check the peer-dependency range before bumping TypeScript. `typescript-eslint`
declares a supported range, and a repository with no ESLint configuration can
run a version that a repository with one cannot.

Record such a constraint in the repository's own `AGENTS.md`. It is local
operating truth, not universe policy.
