# Top-tier review of the governance layer

Contract §11 sends repository ownership, public/private boundaries, migration of
shared standards, security policy, and exceptions that weaken a baseline to the
top tier. §16 item 13 says self-certification does not satisfy it.

Reviewer tier: top (Fable). Date: 2026-08-21. Scope: read-only.

Verdict: **approve conditionally**, blocking on the direct-push audit.

## Why it mattered

The review found six defects. Two of them would have been invisible to any
amount of self-checking, because the same agent wrote both the claim and the
evidence for it:

- `standards/security.md` asserted that both `pull_request_target` workflows
  declare a top-level `permissions:` block. `servitium` does not. The assertion
  came from `evidence/controls-baseline.md`, which the same agent wrote.
- The CLI's `render-baseline` subcommand crashed with an `AttributeError`. All
  66 tests passed, because none of them invoked the CLI.

## The six defects

| # | Defect | Severity |
| --- | --- | --- |
| M1 | The direct-push audit was mis-scoped, spoofable, and full of false positives | blocking |
| M2 | `standards/security.md` stated a false fact about a pre-authorised exception | high |
| M3 | `universe render-baseline` crashed; no test invoked the CLI | high |
| M4 | `standards/languages/ansible.md` copied Orange's rules instead of linking them | high |
| M5 | The `deploys` agent never met the sanctioned secrets path | high |
| M6 | Twelve unread copies of `owns` / `does_not_own` in the catalogue | medium |

### M1 in detail

The direct-push audit is the **sole** stand-in for branch protection on five
private repositories, and therefore the load-bearing member of the largest named
accepted risk. It was theatre:

- It whitelisted `initiatives/` in **every** repository, not only `architecture`.
  A direct push anywhere was exempt if its files sat under that path — including
  the approved contract itself.
- It exempted any commit whose subject began `Merge pull request`, which any
  agent can type.
- It misread squash-merged pull requests as violations. `servitium`, which has a
  `pull_request` ruleset, reported 14.
- It had no carve-out for the automated digest pushes to `deploys` that
  `standards/security.md` explicitly accepts: 41 findings against intended
  design, in a standard that twice says such a check teaches everyone to ignore
  the tool.
- It read a local branch the audit skill is forbidden to pull, so it described a
  stale ref.

## What was fixed

All six, before wave 1 generated anything from the templates. A template fix
landing after wave 1 would have marked every repository stale.

The direct-push exceptions now live in the catalogue as data, per repository. A
commit that mixes an exempt path with anything else is not exempt. Merge commits
are recognised structurally; squash merges by GitHub's own `(#N)` convention.
Pre-existing history is baselined per repository, exactly as every linter gate
here baselines pre-existing findings.

**Direct-push findings across twelve repositories: 90 to 0. A newly introduced
one still reports.**

`validate` gained two checks the review implied: a standard linked from no
generated section fails unless marked `owner_facing`, and `publication_status`
is cross-checked against declared and observed visibility.

The decision-record check was relaxed. It demanded the new template of 26
pre-existing records in three older formats, with no baseline — noise nobody
would act on, in a framework built on new-work-first. It now catches what the
standard actually names: current-state prose filed as a decision, which declares
no status.

## One defect the fixing introduced

Widening the generated `files` list, so a mostly-Markdown repository stops
scanning only its code, handed Markdown to `ruff`: 2592 parse errors. Language
sensors are now scoped to their own language, with the root list left as the
union so `line-count` still covers everything.

Habit Hooks caught it. That is the coaching layer doing the job §7.6 describes,
on the first change where it mattered.

## The six exceptions, judged

| Exception | Verdict |
| --- | --- |
| Five private repositories cannot carry a ruleset | accepted risk in principle; real only once M1 was fixed |
| `deploys` takes no pull-request rule | accepted risk, genuinely held |
| `plepic` and `servitium` keep `pull_request_target` | accepted risk; the design is real, the supporting claim was not (M2) |
| Habit Hooks is never a CI gate | holds |
| `jscpd` disabled in six repositories | holds |
| `mihkel` keeps ten root documents | holds, conditional on the decision record landing in wave 1 |

## Confirmed sound

- The gitleaks fixture trade: demonstrating locally rather than pushing a
  credential-shaped string at a public repository is correct. A pushed fixture
  is itself the incident class the control prevents.
- Both deliberate omissions. A JSON Schema beside the Python validator would be
  a second copy of its rules, and nothing in this initiative is reusable beyond
  this universe.
- `tooling/universe`'s size. No scheduler, no dashboard, no packaging, one
  shared catalogue parser.
- `universe/relationships.md` against the repositories themselves.

## Deferred to wave 2

- Add the top-level `permissions:` block to `servitium/.github/workflows/deploy-test.yml`.
- Correct the three "actions/checkout v4.2.2" comments that sit beside a v7.0.1
  SHA. `standards/security.md` calls a wrong comment worse than none, so the
  universe currently violates its own standard, knowingly.
- Pin `kubeconform`'s `-kubernetes-version`; it currently resolves schemas from
  `master`, so the gate's strictness can drift with upstream.

## Not verified by the reviewer

Anything GitHub-side: ruleset responses, push protection, the open PRs and their
CI. The gitleaks checksum and the action SHA-to-version mappings. The Habit
Hooks behavioural claims. `zizmor`'s actual findings. Whether the wave 0 fixture
demonstrations occurred as recorded.
