# Architecture Repository Bootstrap and Managed-Universe Consolidation Contract

## Invocation

Run this work by telling the coding agent:

```text
implement architecture-bootstrap.md
```

After any interruption, tell it:

```text
resume implementing architecture-bootstrap.md
```

The invoking Claude Code or Codex session is the **orchestrator**. It must carry the work through discovery, approved planning, skill preparation, implementation, verification, repository updates, and handoff. It must not stop after writing another plan or merely describe what somebody else should do.

Use each runtime's native explicit skill invocation and subagent mechanisms, but keep all durable plans, state, decisions, evidence, commits, and handoff material vendor-neutral.

---

## 1. Mission

Establish the existing private repository named **`architecture`** as the governance and coordination layer for the complete managed engineering universe. The repository already exists and holds this contract; it is otherwise empty, so the work is to populate it, not to create it.

Then execute its first initiative: **audit the documentation and agent instructions of every governed repository, centralize genuinely universe-wide material in `architecture`, retain concise repository-owned material in each repository, and make every repository conform to the resulting engineering contract.**

The work must result in an operational governance system, not only a proposed folder tree.

### Scope of change in governed repositories

This initiative changes **documentation, agent instructions, and check configuration only**. It must not rewrite, reformat, or refactor existing application code in any governed repository.

Everything it writes follows the documentation rules in §5.9–§5.12: a minimal framework, Orange's documentation layout, Minto structure, MECE grouping, ASD-STE100 wording, and a short `AGENTS.md`. Those rules apply from the first document, including the standards themselves.

It must nevertheless leave behind *enforceable* engineering rules, not prose. All of it is defined centrally in `architecture`: linters and static analysis gate merges in each repository's CI, while Habit Hooks (<https://github.com/habit-hooks/habit-hooks>) coaches the agent during edits and is *instructed* per repository rather than installed there. Both are governed by a strict **new-work-first** rule — rules apply to code written or changed from the moment they land; pre-existing violations are baselined, not fixed in bulk. See §7.6.

The completed outcome must provide:

1. A complete but concise catalogue of governed repositories and logical components.
2. Clear ownership and source-of-truth boundaries between repositories.
3. Shared engineering standards with as little unmanaged duplication as reasonably possible.
4. Repository profiles that allow different repository types to conform without forcing identical layouts.
5. Small, self-contained local agent instructions in every repository.
6. A controlled mechanism for propagating the shared agent baseline while preserving repository-specific rules.
7. Durable cross-repository initiative state that can survive interruption and model/runtime changes.
8. Explicit rules for deciding whether new work starts in the owning repository or in `architecture`.
9. Auditable public/private boundaries and baseline security checks.
10. A first completed conformance pass across all accessible governed repositories.
11. The existing but unimplemented `ai-portal` repository registered in the managed universe, with its product work **not started by this initiative**.
12. Language-appropriate code-quality rules owned centrally: a CI gate in every governed repository and agent coaching instructions derived from its declared languages, both scoped to new and changed code.

This is a governance/documentation/conformance initiative. It must not change production application versions, Argo CD desired state, live infrastructure behavior, or repository visibility merely to complete the bootstrap.

---

## 2. Meaning of `architecture`

`architecture` is the private engineering-governance repository. It is not:

- an application monorepo;
- a replacement for repository-local architecture documentation;
- a deployment repository;
- an inventory or secret store;
- a universal issue tracker for every small task;
- a container for agent skills, apart from the single universe audit skill it owns (§12);
- a parent Git repository or Git-submodule tree containing the governed repositories.

It owns only universe-wide concerns:

- the managed-universe catalogue;
- cross-repository standards;
- repository profiles and contracts;
- cross-repository decisions;
- coordination of initiatives with several peer repositories or no clear single owner;
- durable state for those initiatives;
- shared templates and conformance tooling;
- references to approved reusable skills and their pinned versions.

The governing rule is:

> Each fact has one authoritative home. `architecture` owns the map, shared policy, and cross-repository state; each implementation repository owns its code, local architecture, local decisions, and repository-specific operating truth.

Private does not mean that secrets may be stored in `architecture`. Credentials, tokens, keys, session material, and secret values remain prohibited there.

---

## 3. Managed universe

Treat the following as the initial authoritative scope. Verify actual remote names, local paths, default branches, current GitHub visibility, and repository existence before changing anything.

The terms **public** and **private** below describe the intended content policy. Track actual GitHub visibility separately because some repositories intentionally differ today.

### `architecture`

- **Intended visibility:** private.
- **Current state:** already exists, locally and as a private GitHub repository, and already contains this contract. It is otherwise effectively empty. Populate it; do not recreate, re-clone, or re-initialize it.
- **Purpose:** governs all universe-wide engineering activity, including cross-repository standards, project coordination, repository catalogue, cross-cutting decisions, and durable state management.
- **Must not own:** application source, live deployment state, private infrastructure variables, credentials, or reusable skill implementations.

### `orange`

- **Intended visibility:** public/public-safe.
- **Current GitHub state:** currently private and not yet published; do not change visibility during this initiative.
- **Purpose:** reusable and publishable infrastructure implementation for Orange, including public-safe platform code, automation, architecture, operating patterns, and Orange-owned decisions.
- **Must not own:** live private variables, private inventory, secrets, or general cross-repository governance.

### `orange-inventory`

- **Intended visibility:** private.
- **Purpose:** private extension to `orange`; owns live Orange inventory, environment-specific variables and desired state, private operational evidence, environment-specific recovery information, and Orange-local working plans.
- **Special note:** it may be checked out under `orange/inventory`, but it is a separate Git repository. Detect and treat it as such.
- **Must not become:** the default plans repository for unrelated cross-repository initiatives.

### `deploys`

- **Intended visibility:** public.
- **Reason for current/public state:** a GitHub plan limitation, not an architectural preference. It is an operator decision, already made. Record it and move on; do not re-open it, propose alternatives, or document workarounds.
- **Purpose:** authoritative deployable desired state for Argo CD-reconciled applications, normally referencing immutable image digests and non-secret configuration.
- **Must never contain:** secret values, OAuth credentials, private keys, unrestricted tokens, private inventory, or material that is unsafe to expose.
- **Relationship:** application repositories build artifacts; approved promotion changes `deploys`; Argo CD reconciles it.

### `myskills`

- **Intended visibility:** private for now; may become public after deliberate sanitization.
- **Purpose:** reusable executable agent skills and plugins that apply across repositories or recurring operations.
- **Must not own:** project plans, universe governance, or dynamic initiative state.
- **Security position:** treat skill changes as executable-behavior changes requiring tests and review.

### `plepic`

- **Intended visibility:** public.
- **Purpose:** `plepicgames.com` Medusa store and its application-specific documentation, tests, build, and release code.
- **Current constraint:** repository status and GHCR images are public due to GitHub/free-tier limitations.
- **Must not contain:** store secrets, payment credentials, private customer data, environment secrets, or private deployment state.

### `robobook`

- **Intended visibility:** public.
- **Current state:** exists on GitHub; not present in the local workspace. Clone it into an isolated working location to audit it. Cloning is not creation.
- **Purpose:** bookkeeping workflow for Plepic Games OÜ
- **Must not contain:** secrets, actual company details, real names, customer data

### `servitium`

- **Intended visibility:** public.
- **Purpose:** source and application-specific documentation for `servitium.future.ee`.
- **Must not contain:** private environment variables or deployment credentials.

### `nomadtty`

- **Intended visibility:** public.
- **Purpose:** maintained fork of NomadTTY with a small number of local fixes and additions.
- **Profile:** public fork; preserve upstream provenance, license obligations, patch rationale, and an understandable delta from upstream.
- **Fork posture:** contributing changes back upstream is not expected. Optimize for maintaining it here, not for a clean upstream patch series — apply the full governance baseline. Provenance and license obligations still matter, for legal reasons and for pulling upstream fixes, not for contribution.
- **Must not contain:** Orange credentials or private host/inventory details unnecessary to the fork.

### `mihkel`

- **Intended visibility:** public.
- **Purpose:** OpenClaw-based Mihkel agent operating through Discord `#liivakast`, including public-safe source, prompts, tests, and integration code.
- **Must not contain:** Discord tokens, provider credentials, private conversation exports, or unrestricted Orange administration credentials.

### `ai-portal`

- **Intended visibility:** public.
- **Lifecycle at the start of this initiative:** the GitHub repository exists and is public, but the product is unimplemented. The local clone is empty: `main` has no commits and its upstream tracking ref is gone. Fetch before assuming anything, and expect that there may be no scaffold to bring into conformance — in which case wave 1 adds only `README.md`, `AGENTS.md`, and `CLAUDE.md`.
- **Purpose:** `ai.future.ee` and its subprojects/integrations, including LibreChat integration and the agentic/manual Scratch playground.
- **This initiative:** register it, record its intended ownership boundaries, and bring its existing scaffold to baseline conformance. Do not implement the AI Portal product here, and do not scaffold application structure for it.
- **Must not contain:** family identities, secret group membership, provider keys, OAuth sessions, or private infrastructure variables.

### `entpass`

- **Intended visibility:** private.
- **Lifecycle:** theoretical/new development for an LEI registration business.
- **Purpose:** business-sensitive research, architecture, source, and local plans for the EntityPass/LEI concept.
- **Must remain separate from:** universe-wide standards and unrelated Orange infrastructure state.

### Membership

**The list above is the authority.** A repository is governed because it appears in this contract, and afterwards because it appears in `universe/repositories.yaml`, which this contract seeds. Membership does not depend on a file existing inside the repository, so the bootstrap can start when no repository carries a marker yet.

There is no second declaration inside the repository. What the agent needs locally — the profile, the languages, the publication constraints, the standards that apply — is materialized into the repository's `AGENTS.md` managed section, generated from the catalogue (§7.3). One home, one generator, nothing to keep in agreement.

Any repository outside the list is out of scope by construction — archived, legacy, or personal repositories under the same GitHub account included. Do not catalogue them, audit them, add files to them, or report them as conformance failures. The account listing is not the universe.

Adding a repository later is deliberately cheap: add the catalogue entry, run the baseline sync, run the audit (§7.7).

### Expected relationship model

Establish and document this general flow after validating it against reality:

```text
architecture
├── governs standards, repository contracts, and cross-repo initiatives
├── catalogues every repository and logical component
└── pins reusable skills from myskills

myskills
└── supplies tested reusable execution procedures to agents

orange
├── owns public-safe infrastructure implementation
└── is parameterized by private orange-inventory state

orange-inventory
└── owns live private Orange variables, inventory, and evidence

application repositories
├── plepic
├── servitium
├── nomadtty
├── mihkel
├── robobook
├── ai-portal
└── entpass where/when deployable
    │
    └── CI builds and verifies immutable artifacts/images
            │
            ▼
         deploys
            │
            ▼
         Argo CD
            │
            ▼
         Orange runtime
```

Do not force a repository into this exact flow when evidence shows a legitimate different lifecycle. Record exceptions explicitly rather than hiding them.

---

## 4. Authority and reconnaissance

This contract is the initial intent, not proof of the current implementation.

Before planning migrations, inspect:

1. Every available governed repository, including root documentation, `AGENTS.md`, `CLAUDE.md`, `README*`, `docs/**`, `.github/**`, scripts, checks, hooks, plans, ADRs, and repository metadata.
2. Current local worktrees, branches, dirty state, nested repositories, remotes, default branches, and open work that must not be disturbed.
3. The existing `orange/docs` and `orange-inventory/docs` structures described by the operator.
4. Existing conventions and durable-state patterns from the ongoing `plepic`/legacy shop work, including the material currently under `orange-inventory/docs/working/2026-08-08-legacy-vm-shop/` or its actual current equivalent.
5. Existing reusable skills and plugins in `myskills` before creating anything new.
6. Existing GitHub Actions, gitleaks configuration, dependency automation, branch/ruleset limitations, release workflows, and public/private safety controls.
7. Existing documentation or automation that already defines repository ownership, public/private boundaries, Argo CD promotion, testing, agent operation, or recovery.
8. Any existing `architecture` or engineering-plans repository or similarly named predecessor.

Repository evidence wins over assumptions. Correct typos and stale paths in the resolved plan, but do not silently change product ownership or visibility policy.

Read-only reconnaissance may run in parallel. No subagent may modify a repository during discovery.

---

## 5. Core design principles

### 5.1 Centralize policy, not repository truth

Move or consolidate material into `architecture` only when it genuinely governs several repositories or the managed universe as a whole.

Examples that normally belong in `architecture`:

- repository setup and ownership rules;
- public/private content boundaries;
- documentation semantics;
- how tasks are routed to local `docs/working` versus central initiatives;
- agent safety and multi-repository work rules;
- baseline testing and security expectations;
- GitOps promotion principles;
- reusable-skill governance;
- repository catalogue and relationships;
- common conformance profiles.

Examples that normally remain local:

- how a particular application works;
- local development commands;
- repository-specific architecture and ADRs;
- service recovery and operational runbooks;
- current deployment-specific behavior;
- application tests and release procedures;
- a substantial initiative clearly owned by one repository;
- active local working state.

Do not move Orange-specific ADRs to `architecture` merely because another repository might learn from them. Link to them where useful.

### 5.2 One authoritative home

For every migrated section, record:

- original repository and path;
- original commit;
- classification;
- new authoritative location;
- local replacement or reference;
- whether intentional generated duplication remains.

Do not leave two manually maintained copies that both appear authoritative.

### 5.3 Local instructions must remain usable

Agents frequently open only one repository. A local `AGENTS.md` must therefore remain concise but operationally sufficient.

Do not reduce local instructions to only “read the architecture repository.” Instead use:

- a small managed baseline materialized from `architecture`, delimited by begin/end markers and carrying no version or digest of its own (§7.3);
- a repository-specific section maintained locally;
- links to fuller central standards for cross-repository or exceptional work.

**Both files are required in every repository.** `AGENTS.md` holds the rules. `CLAUDE.md` is a pointer to it and nothing else — same content everywhere, generated from one central template, never a place where a rule lives. Requiring both regardless of what a given agent runtime reads natively costs one small generated file per repository and removes the question entirely: Codex and Claude Code cannot end up with different rules, because there is only one set of rules and one file holding it.

### 5.4 Controlled duplication is allowed

Avoid unmanaged duplication, not all duplication.

A generated, managed common section in each `AGENTS.md` is acceptable because it makes local agent behavior reliable. A manually copied six-page standard that can drift is not.

Do not use cross-repository symlinks, absolute local paths, or Git submodules merely to share agent instructions.

### 5.5 Profiles, not forced identical trees

Different repository types need different local structures. Define repository profiles rather than requiring every repo to contain empty copies of the same directories.

Likely initial profiles, subject to discovery:

- `governance-private` — `architecture`;
- `platform-public-ready` — `orange`;
- `inventory-private` — `orange-inventory`;
- `gitops-public` — `deploys`;
- `skills-private` — `myskills`;
- `application-public` — `plepic`, `servitium`, `mihkel`, `robobook`, `ai-portal`;
- `fork-public` — `nomadtty`;
- `research-private` — `entpass`.

`fork-public` is not a reduced conformance tier. It differs from `application-public` only in what it *additionally* documents — upstream provenance, license obligations, and the local delta. Because upstream contribution is not expected for `nomadtty`, it carries the same governance files, agent instructions, and code-quality gates as any other public application repository; the added files are simply recorded in the delta documentation so a later upstream merge sees them as intentional.

### 5.6 Public means public-safe

A repository classified as public must pass public-content policy even if its GitHub repository is temporarily private.

Track at least:

```yaml
declared_visibility: public | private
current_remote_visibility: public | private | unknown
public_safe_required: true | false
publication_status: published | currently-private | candidate | not-applicable
```

Do not change repository visibility during this initiative without an explicit operator gate.

### 5.7 Active work must survive unchanged

Do not relocate, rewrite, reformat, split, or rename active durable work records when doing so could break another agent's resume path or invalidate its references.

In particular, treat large active work under `orange-inventory/docs/working` as read-only unless its active orchestrator explicitly participates.

Register active initiatives centrally by link and metadata. Migrate or archive them only after completion or a separate approved migration.

### 5.8 Keep governance proportional

Do not require a central initiative for every issue.

The shared standard must state:

```text
small routine change
→ branch/issue/PR in owning repository; no working plan required

substantial single-repository change
→ owning repository docs/working

one clear primary repository with light support changes elsewhere
→ primary repository docs/working

several peer repositories, undecided boundaries, or no clear owner
→ architecture/initiatives/active
```

`architecture` must remain a small set of high-value cross-repository initiatives, not a universal task tracker.

### 5.9 Maximum benefit from a minimal framework

This governs the whole architecture layer, not only the coaching layer. Measure the framework by what it prevents, not by what it contains.

- Every artifact needs a named consumer: an agent, a check, or a person doing a specific task. If nobody reads it, do not create it.
- Prefer few files, but split a standard when an agent needs one part without the other. Documents are loaded selectively: relevance beats consolidation.
- Profiles are data, not directories. A profile is a short file; it does not require a matching tree in every repository.
- Add a schema only when it validates state that already exists.
- Delete stubs. A section that promises future content costs maintenance and has no reader.
- Prefer a link to a copy, a generated section to a manual one, and a check to a paragraph of advice.
- If a rule cannot be checked or reviewed, state it once. Do not build machinery around it.

### 5.10 Documentation structure

Orange already has the pattern. Reuse its semantics wherever a repository needs documentation:

```text
docs/
  current/     implemented behavior — how it works today
  decisions/   numbered ADR-style records for durable choices
  issues/      open correctness and operability issues, when any exist
  working/     active plans, one file or directory per initiative
```

- `current/` describes present state. It does not narrate history.
- `decisions/` records why, once, numbered and dated. Use the MADR format rather than inventing one: it is the common convention, costs nothing, and any future reader recognises it. Do not restate a decision in `current/`.
- `working/` holds active work. Archive it when the work completes. §5.7 protects it while it is active.
- No repository needs every directory. Create one when it has content (§5.9).
- Root documents stay few: `README.md`, `AGENTS.md`, `CLAUDE.md`.
- Repository boundaries and ownership belong in `README.md`.

### 5.11 Writing rules

Apply three sources. When they conflict, meaning wins over structure, and structure wins over wording.

**Minto — structure.** State the answer first. Then the supporting points, grouped. Then the detail. A reader who stops after the first paragraph still has the answer. Do not build up to a conclusion.

**MECE — grouping.** Groups do not overlap, and together they cover the subject. Two documents that claim the same fact break §5.2. A gap between sections is a missing document, not an implicit rule.

**ASD-STE100 — wording.** Simplified Technical English:

- one word, one meaning; use the same term for the same thing everywhere;
- active voice; imperative mood for instructions;
- one instruction per sentence;
- at most 20 words in a procedural sentence, 25 in a descriptive one;
- at most 6 sentences in a paragraph;
- present tense for present truth;
- no synonyms for variety, and no jargon a new agent cannot resolve;
- keep articles and normal grammar; do not write telegraphic notes.

**Prose budget.** Write the shortest text that keeps the meaning and stays readable. Prefer a table, a list, or a command to a paragraph. Do not pad with restatement, motivation, or history. Do not compress into ambiguity: an agent that has to guess costs more than the words saved.

Automate only the mechanical part — layout, links, file budgets, terminology. Review the rest (§5.9).

Use existing tools rather than writing them; hand-rolling these in Python would violate §9.5:

- `markdownlint-cli2` for structure and layout;
- `lychee` for link checking, internal and external.

That is the whole automated set. Full ASD-STE100 conformance cannot be automated — the controlled vocabulary is a licensed specification and no certified open checker exists — and a prose linter with a hand-maintained terminology list would be abandoned within months, which is worse than not having one. Wording is a review concern. §5.11 is written knowing that.

### 5.12 `AGENTS.md` stays short

An agent reads `AGENTS.md` at the start of every task, so length there is a recurring cost.

- Target one screen of local content. Set the exact numbers at Gate 1: a soft target that is reported for review, and a hard ceiling — roughly two to three times the target — that fails conformance.
- Gate the outrage, coach the ideal. A hard failure at the ideal length would be gamed by compressing into ambiguity, which §5.11 names as the costlier error. This is the same reasoning that keeps Habit Hooks out of CI (§7.6).
- Keep the managed baseline small. A long shared rule belongs in `architecture`, linked.
- Move command catalogues to `docs/current/` or to a script that lists them. Name the few commands an agent needs first; link the rest. Orange's 481-line `AGENTS.md` is the case in point — most of it is a command catalogue.
- Do not restate central standards. Link them. §5.3 still binds: local instructions must stay operationally sufficient on their own.
- Every line earns its place: a rule an agent breaks without it, or a fact it cannot discover quickly.

---

## 6. Target `architecture` repository structure

Start with the smallest structure that supports the actual requirements. A suitable target is:

```text
architecture/
├── README.md
├── AGENTS.md
├── CLAUDE.md
│
├── universe/
│   ├── repositories.yaml
│   └── relationships.md
│
├── standards/
│   ├── repository-contract.md   # incl. skills and plugin governance
│   ├── documentation.md
│   ├── work-routing.md
│   ├── agent-operation.md       # incl. multi-repository work
│   ├── security.md              # incl. public/private boundaries
│   ├── gitops-and-deployment.md
│   ├── code-quality.md          # incl. testing expectations
│   └── languages/
│       ├── typescript.md
│       ├── python.md
│       ├── ansible.md
│       └── shell.md
│
├── profiles.yaml                # one entry per profile — data, not a directory (§5.9)
│
├── templates/
│   ├── renovate.json            # shared preset the repositories extend
│   ├── agent-baseline.md
│   ├── claude-md-pointer.md
│   ├── decision.md
│   └── initiative/
│
├── decisions/
│   ├── 001-architecture-repository-role.md
│   ├── 002-source-of-truth-and-documentation-ownership.md
│   ├── 003-myskills-remains-separate.md
│   ├── 004-conformance-tooling-in-python.md
│   └── 005-audit-skill-lives-in-architecture.md
│
├── initiatives/
│   ├── active/
│   │   ├── architecture-bootstrap.md        # this contract (canonical)
│   │   └── architecture-bootstrap/          # its durable state
│   │       ├── resolved-plan.md
│   │       ├── state.yaml
│   │       ├── migration-map.yaml
│   │       ├── repositories.yaml
│   │       ├── skills.lock.yaml
│   │       ├── open-questions.md
│   │       ├── decisions/
│   │       ├── journal/
│   │       └── evidence/
│   ├── planned/
│   │   └── ai-portal/
│   │       └── README.md
│   └── completed/
│
├── skills/
│   └── audit-universe/          # thin wrapper over the CLI below (§12)
│
├── tooling/
│   └── universe                 # one Python CLI: validate | audit | sync-baseline
│
└── schemas/                     # only once it validates state that exists (§5.9)
    └── repositories.schema.json
```

Seven standards plus the language documents, with four subjects deliberately folded in rather than given files of their own: skills governance into the repository contract, multi-repository work into agent operation, public/private boundaries into security, testing expectations into code quality. Each fold is a subject no agent needed to load without the document that now contains it.

The count is not a target in either direction. Split a standard when an agent needs one part without the other; otherwise leave it whole. And apply the same test that governs everything else here: **no standard exists unless some repository's generated `AGENTS.md` section links it.** A document nothing links is a document nothing reads. Owner-facing standards — `work-routing.md`, `documentation.md` — satisfy this through `architecture`'s own generated section, which is where the orchestrator reads them. Do not push owner-facing links into eleven application baselines to satisfy the rule; that inflates exactly the file §5.12 keeps short. This tree is a target, not permission to create empty scaffolding. Omit directories with no immediate use. Prefer a small executable system over an impressive but hollow hierarchy (§5.9).

This contract already lives in the repository. Its canonical location is:

```text
initiatives/active/architecture-bootstrap.md
```

Do not copy, move, rename, or date-prefix it: the invocation string, the resume path, and the file name must stay aligned. Durable state lives in the sibling directory `initiatives/active/architecture-bootstrap/`, which contains no second copy of the contract. Record the contract's content digest in `state.yaml` so drift between the approved contract and the running one is detectable. Do not create competing edited copies.

---

## 7. Per-repository conformance contract

Every governed repository must end with a profile-appropriate, tested minimum.

### 7.1 Required everywhere

Require, in every governed repository:

```text
README.md
AGENTS.md
CLAUDE.md   — a generated pointer to AGENTS.md, identical everywhere (§5.3)
```

**There is no local governance marker file.** Everything a marker would have carried — profile, declared visibility, public-safety requirement, languages, one-line description — lives in `universe/repositories.yaml` and is materialized into the repository's `AGENTS.md` managed section by the sync tool. The agent still learns it all without opening `architecture`; it reads it in the file it already opens first.

A separate `repository.json` was considered and dropped. It would have been a second copy of facts the catalogue already owns, kept in agreement by a check that exists only because the copy exists. For one owner and twelve repositories that is pure overhead (§5.9). If some later governance tool genuinely needs a machine-readable file inside each repository, add it then, generated from the catalogue like everything else.

**`languages` is the load-bearing field in the catalogue.** It is the set of languages the repository actually contains, and it determines:

- which `standards/languages/*.md` documents the generated `AGENTS.md` section links;
- which linters and static analysis gate its CI, and which Habit Hooks plugins its coaching instruction names (§7.6).

The permitted values are the universe's four languages — `typescript`, `python`, `ansible`, `shell` (§7.6) — and the list may be empty, as it is for `deploys`. Populate it from evidence, not expectation: a language listed but absent creates checks that never run. The languageless `generic` coaching plugin applies to every repository and is deliberately not declared.

### 7.2 `README.md` minimum

Each README should clearly say:

- what the repository owns;
- what it does not own;
- intended visibility/public-safety status;
- how to develop and test it;
- how it is built and/or deployed, when applicable;
- where repository-local architecture and decisions live;
- where cross-repository standards and initiatives live.

### 7.3 `AGENTS.md` minimum

Each `AGENTS.md` must have:

1. A generated/managed baseline section materialized from `architecture`.
2. Repository-specific purpose and boundaries.
3. Exact test/check commands or reliable discovery instructions.
4. Public/private and secret-handling constraints relevant to the repository.
5. Rules for plans, worktrees, commits, and changes to adjacent repositories.
6. Any local exceptions to central standards, linked to an explicit decision.
7. Links to the language standards that apply, generated from the catalogue's `languages` — a repository with `python` points at `standards/languages/python.md` rather than restating its rules.

Keep it short. §5.12 sets the budget and the reasons.

**One authority, and nothing stored twice.** `architecture` owns the baseline text. The managed section carries no digest and no version number, and the repository records neither. Staleness is a diff: regenerate the expected section from `architecture` at HEAD and compare it to what is in the file. Same output means current, different output means stale, and there is no third state to get wrong. If pinning a repository to an older baseline ever becomes necessary, add the version marker then — it is not needed while every repository tracks HEAD.

Use clear markers such as:

```text
<!-- BEGIN MANAGED ARCHITECTURE BASELINE -->
...
<!-- END MANAGED ARCHITECTURE BASELINE -->
```

The sync tool may modify only the managed region. It must refuse malformed or duplicate markers.

### 7.4 Documentation by profile

Use the layout in §5.10, and apply it by semantics rather than as an identical tree.

Typical expectations:

- Platform/infrastructure: `docs/current/`, `docs/decisions/`, recovery/operations material.
- Private inventory: environment operations, recovery evidence, and `docs/working/` for Orange-local work.
- Applications: local architecture/current-state docs, ADRs, and optional `docs/working/` for substantial local initiatives.
- Skills: skill catalogue, tests, installation/sync instructions, and security boundaries.
- Public fork: upstream provenance, update process, patch/delta documentation, and local test procedure.
- GitOps: deployment ownership, promotion/rollback rules, validation commands, and public-secret constraints.
- Governance: universe catalogue, standards, profiles, cross-repository initiatives, and conformance tooling.

### 7.5 Checks and hooks

The central policy defines expected outcomes; repositories enforce them locally through the lightest existing mechanism.

Prefer:

```text
fast optional local checks
+ authoritative CI checks
+ repository rules/branch protections where available
```

Do not rely on Git hooks alone. Do not introduce a new task runner or hook framework everywhere merely for visual uniformity.

At minimum, determine profile-appropriate handling for:

- gitleaks or equivalent secret scanning;
- formatting/linting already used by the repository;
- behavior-based tests;
- documentation/link validation;
- repository conformance validation;
- public/private boundary checks;
- container/dependency scanning where the repository builds deployable artifacts;
- manifest validation for `deploys` and infrastructure repositories.

Agents never commit to a default branch. They branch, open a PR, and self-merge only where policy allows. Where the GitHub plan does not offer branch protection, the rule itself is the enforcement — state it in `standards/agent-operation.md` and check it in the audit (§7.7) against commit metadata.

Two exceptions, both narrow and both named in the standard so the audit does not flag its own governance as a violation:

- durable initiative state under `initiatives/*/` in `architecture` commits to `main` directly — a coordination record is not a code change, and gating it behind review would stall the resume path it exists to protect;
- an empty repository needs an initial commit before any branch can exist. Push it directly, then work normally from the next commit onward.

The audit whitelists exactly these two cases and nothing else.

**Baseline security controls.** These are named concretely because "profile-appropriate handling" is not an instruction an agent can follow. `standards/security.md` owns them:

- **Workflow hardening.** Agents edit CI workflows constantly, and a workflow is the shortest path from a pull request to a token. Pin third-party actions to a commit SHA, set a least-privilege top-level `permissions:` block, and lint changed workflow files with `zizmor`.
  - Pre-authorize one exception before rollout: `plepic` and `servitium` run deliberate, commented `pull_request_target` deploy-test workflows, and `zizmor` flags that trigger by default. Record the exception in `standards/security.md` with the reasoning. An agent that "fixes" a correctly designed pipeline to silence a linter has made the repository worse, and a first run that fails on intended design teaches everyone to ignore the tool.
- **Dependency automation.** Renovate, installed once as a GitHub App, extending one shared preset held in `architecture/templates/`. It also pins digests, which `deploys` needs anyway.
- **Secret scanning.** gitleaks in CI everywhere, plus GitHub push protection wherever the plan allows it. Push protection stops the leak; gitleaks catches what push protection does not.
- **Branch protection floor.** On repositories that support rulesets, require a pull request and the CI gate as a required status check. Where the plan does not allow rulesets, record that as an accepted, named risk rather than leaving a silent gap — the PR rule above and the audit are what stand in for it.
- **Manifest validation.** `kustomize build` or `helm template` as a dry run, then `kubeconform`, for `deploys` and any repository shipping Kubernetes manifests. Note `kubectl-validate` as the successor candidate if `kubeconform` stops being maintained.
- **Secrets delivery.** `deploys` is public and must never carry secret values, so name the sanctioned path instead of leaving agents to improvise: External Secrets Operator reading from the OpenBao instance Orange already runs, with SOPS plus age as the fallback if that proves impractical. Write the chosen pattern into `standards/gitops-and-deployment.md`.

OpenSSF Scorecard and build provenance attestation for GHCR images are reasonable later additions. They are not part of this initiative; record them as candidates.

Use existing working patterns when sound. Record justified profile exceptions.

### 7.6 Code quality: central rules, agent-side coaching, CI gates on linters

The purpose is to make *future* changes compliant. It is not to clean up the existing codebases, and this initiative must not attempt that.

Two mechanisms with different jobs. Do not confuse them:

| Mechanism | Job | Where it runs | Gates a merge? |
| --- | --- | --- | --- |
| Habit Hooks | coaches the agent while it edits — turns a linter finding into an actionable guide | the agent's workstation, inside the edit loop | no |
| Linters and static analysis | verifies the result | repository CI, on changed files | yes |

**Four languages today.** `typescript` (including Node.js), `python`, `ansible`, and `shell`. Shell is easy to overlook and load-bearing here: `myskills` is entirely bash, every repository's CI funnels through a bash validate script, and some test harnesses are bats. Leaving it undeclared would leave `myskills` — the repository §12 says must treat changes as executable-behavior changes requiring tests and review — with no gate at all. Treat the set as current, not closed: discovery may find another, and a repository may acquire one later. Adding one is a small deliberate change — write `standards/languages/<language>.md`, declare it in the catalogue, add the gate. Do not write a document for a language nothing declares. Alongside them, Habit Hooks' languageless `generic` plugin — file length and duplication — applies to **every** repository, including those declaring no language at all, such as `deploys`. It is never declared anywhere; it is simply always on, and it carries most of the shipped coaching guides.

**Central definition.** `architecture` owns `standards/code-quality.md` plus `standards/languages/typescript.md`, `python.md`, and `ansible.md`. Each names the concrete formatter, linter, static-analysis tools, the Habit Hooks plugin where one exists, and the coaching instruction text. This is the single authoritative home: repositories link to it and never restate it (§5.1, §5.2).

Habit Hooks ships plugins for typescript and python. **Ansible and shell have none**, so those repositories run `generic` for coaching and gate on native tools in CI: `ansible-lint` and `yamllint` for ansible, `shellcheck` — and `shfmt` where a repository wants formatting — for shell. Writing custom plugins for either is out of scope; record it as a candidate follow-up if the gap proves to matter.

**Habit Hooks is instructed, not installed per repository.** A repository does not own the tool or its rules. What it owns is:

- one generated instruction in its `AGENTS.md` managed section, derived from the catalogue's `languages`, naming the plugins that apply and telling the agent to run Habit Hooks before declaring an edit done;
- a small generated `.habit-hooks/config.toml` — in practice a single `plugins = [...]` line — because the tool reads configuration only from inside the project. It is a generated artifact materialized from the central standard, marked as such and regenerable, exactly like the agent baseline (§5.4). It is never hand-maintained.

The tool itself is a workstation prerequisite, documented once in `architecture` as a single install command naming every language the universe uses. With `uv tool install`, extras replace rather than add, so a second install naming a different extra silently disables the first; name them all in one command. (`pip install` adds instead of replacing.)

**Make the instruction self-healing.** A prerequisite that lives only in a setup document is a prerequisite that is missing on the machine that needs it — Habit Hooks is not currently installed on this workstation, which is exactly the point. The generated coaching instruction therefore carries the remedy inline, not a pointer to it:

```text
Run `habit-hooks` before declaring an edit done.
If it is not on PATH, install it first:

    uv tool install "habit-hooks[python,typescript]"

Name every language in that one command — a later install with a different
extra silently replaces this one. Then re-run `habit-hooks`.
```

This is the whole mechanism. An agent that finds the command missing fixes it in one step and continues, instead of skipping the check and saying nothing. The exact command lives in `standards/code-quality.md` so it is changed in one place and regenerates everywhere; it names the plugin extras the universe actually uses, and gains a language only when the universe does (§7.6).

**Keep the coaching layer simple.** It is advisory by design. Do not track which workstation has it, do not build attestation, do not add machinery to prove an agent ran it. Conformance checks that the instruction and the generated config are present and correct; nothing more. The CI gate is what actually holds, and it does not depend on any of this.

The snooze baseline is the deliberate exception to central ownership: `.habit-hooks/snooze.json` names that repository's own files, so it is repository-owned truth rather than policy. Where a repository is worth baselining, run `habit-sensors --all | habit-snooze --snooze` once and commit the result. Do not invent a parallel baseline format.

**Coaching and the gate have different scopes, on purpose.** The snooze ratchet returns a file's whole backlog the moment the file is touched, so the agent *sees* more than the gate *blocks* on. That asymmetry is the design: the coach shows the neighbourhood, the gate judges the diff. An agent may fix what it was shown, but backlog fixes go in separate commits from the change that surfaced them, or are left for later without apology. Never mix a cleanup sweep into a feature diff (§9.5).

**CI gates on linters, never on coaching.**

- The gate is the repository's own linter and static analysis, run through the lightest mechanism the repository already has. Do not introduce a new task runner or package manager for uniformity.
- **The gate blocks on new work only, using each linter's own baseline.** ESLint bulk suppressions, `ansible-lint --generate-ignore` into `.ansible-lint-ignore`, `ruff --add-noqa`: record today's findings once, commit the file, and every later run reports only what the change introduced. Touching a file does not make its history your problem.
- Do not build a diff-hunk filter. Parsing linter output and mapping it onto git hunks is a bespoke harness for a problem the tools already solve, and §5.11's rule against hand-rolling applies here too. Where a tool has no baseline of its own — `yamllint`, for instance — scope it with `reviewdog` rather than custom code, and if even that is disproportionate, run it advisory-only and say so.
- **Never make Habit Hooks a required CI check.** A coach that fails builds becomes a target, and a target gets gamed — which is the exact failure mode it exists to prevent.
- Full-tree compliance is reached on demand, not by ratcheting the gate. Run the audit skill (§7.7) when you want the whole picture.
- Formatters run on changed files only. Repository-wide reformatting is prohibited by §9.5 and would destroy the review value of every later diff.
- A tool that cannot run — missing detector, bad config, unresolvable base ref — must fail loudly and distinctly, never be reported as a pass.
- Working the backlog down is ordinary follow-up work in the owning repository, routed by §5.8. It is not part of this initiative.

**Evidence.** A check nobody has seen fail is not a check. For every repository, demonstrate that the CI gate executes and fails on a deliberate violation, then revert the fixture. For coaching, confirm the generated instruction and config are present and name the right plugins — that is the whole check. Record the evidence per §10.

### 7.7 Staying true after the bootstrap

A conformance pass proves the universe was true once. Nothing in the phases below keeps it true afterwards, so the audit is a first-class deliverable rather than a leftover script.

**The audit skill lives in `architecture/skills/audit-universe/`** and is invoked explicitly by the operator. It is a thin wrapper over one Python CLI, `tooling/universe`, with subcommands for validation, per-repository audit, and baseline sync. One program, one place for shared logic, three entry points that already needed the same catalogue parsing (§5.9). It is manual by choice: no scheduler, no cron, no daemon, no watcher (§9.5). A single owner running one command when they want the answer needs no automation around it.

It reports, and it does not fix. Every fix it implies is ordinary work, routed by §5.8.

It answers, across the catalogue:

- which repositories lag the central agent baseline;
- which contain a language they do not declare, or declare one they no longer contain;
- where observed GitHub visibility differs from declared visibility;
- which governance files are missing, extra, or hand-edited inside a generated region;
- which registered working-plan paths have disappeared;
- where commits reached a default branch without a PR, excluding the two whitelisted cases (§7.5);
- what full-tree code-quality compliance looks like behind the baselines the gate tolerates (§7.6).

Run it after any change to the central baseline or standards, before starting a cross-repository initiative, when a repository joins the universe, and otherwise whenever the operator wants the picture.

Part of it runs in `architecture`'s own CI on **every push to `main`**: catalogue validity, internal link checking, layout, and — the useful one — regenerating every repository's expected `AGENTS.md` section at the push's parent and at its head, then reporting which repositories the change just invalidated. That comparison is between two generated outputs, so it needs no clones and no token.

Do not filter that job by path. The generated section depends on the standards, the catalogue, the templates, `profiles.yaml`, **and the generator itself** — and a path filter goes blind exactly where breakage is most likely, in the generator. The job is cheap; run it on everything.

Comparing against what those repositories actually contain does need clones, five of them private, and stays in the manual audit. None of this is a scheduler and none of it weakens the manual-invocation decision: it means a policy change tells you what it just invalidated, at the moment you make it.

Scheduling the full audit later is a one-line change — a workflow with a cron. Do not build that now, and do not build a dashboard for it ever.

---

## 8. First initiative scope: managed-universe bootstrap

The first initiative is complete only when it has performed the following work across all accessible governed repositories.

### 8.1 Inventory and classification

Create a machine-readable inventory of documentation and instruction files, including at least:

- repository and path;
- current branch and commit;
- purpose/summary;
- current authority status;
- likely classification;
- duplicate or overlap references;
- active/inactive status;
- public-safety sensitivity;
- proposed authoritative home;
- proposed action: keep, centralize, reduce-and-link, generate, archive-later, or leave-active.

Classify content as one of:

```text
universe-wide standard
cross-repository architecture/decision
repository-specific current truth
repository-specific decision
private environment state/evidence
active working state
completed historical evidence
generated local baseline
stale or conflicting duplication
uncertain — requires decision
```

Use subagents to audit repositories in parallel, but require a high-tier synthesis/review before accepting centralization decisions.

### 8.2 Migration map

Before editing repositories, produce `migration-map.yaml` and a readable resolved plan covering every proposed move or reduction.

For each item include:

```yaml
source_repo: orange
source_path: docs/AGENTS.md
source_commit: "..."
classification: universe-wide-standard
action: centralize-and-generate-local-baseline
target_path: standards/agent-operation.md
local_replacement: concise-managed-section-plus-local-rules
risk: medium
active_reference_risk: low
```

Do not mass-edit before the plan gate.

### 8.3 Preserve provenance

Cross-repository moves cannot preserve ordinary Git file history. Preserve provenance in the migration map and, where valuable, in a short source note containing original repository/path/commit.

Do not retain giant copied historical files in `architecture` solely for provenance.

### 8.4 Consolidate shared material

Centralize shared standards only after resolving conflicts and selecting one clear authoritative version.

When several repositories contain variants:

1. Compare current behavior and not just prose.
2. Determine whether one version is more current or whether the difference is repository-specific.
3. Ask a high-tier reviewer to resolve material policy conflicts.
4. Record the decision.
5. Keep local exceptions explicit and narrow.

### 8.5 Reduce local duplication

After central standards exist:

- Replace duplicated generic prose with concise local rules, managed baseline content, and links.
- Keep exact commands, ownership boundaries, safety constraints, and local architecture in the repository.
- Ensure agents can work safely from the local repository alone.
- Do not replace useful operational documentation with vague references.

### 8.6 Register active work without disrupting it

Catalogue current substantial work, including the ongoing shop/legacy migration, but leave active durable state in place.

The architecture catalogue may contain:

```yaml
notable_local_work:
  - repository: orange-inventory
    path: docs/working/2026-08-08-legacy-vm-shop
    status: in_progress
    canonical_state: local
```

Do not mirror journals, ledgers, or decision logs centrally.

### 8.7 Register AI Portal without implementing it

Add `ai-portal` to the universe with its discovered current state: the repository exists and is public, the product is unimplemented.

Create only a concise planned-initiative record describing:

- intended product boundary (`ai.future.ee`, LibreChat integration, agentic/manual Scratch);
- owning application repository;
- likely supporting repositories (`deploys`, `orange`, `orange-inventory`, `myskills`);
- that implementation must start as a separate approved initiative;
- the location of any existing AI Portal implementation contract.

Do not begin the AI Portal build in this initiative.

---

## 9. Hard constraints

### 9.1 No interference with ongoing work

- Never write into a dirty or shared worktree.
- Never stash, reset, clean, rebase, amend, force-push, switch another session's branch, or delete another agent's state.
- Use isolated initiative worktrees and dedicated branches.
- One writer per worktree.
- Record every worktree and branch in durable state.
- Read active work records without editing them unless their owner explicitly joins this initiative.

### 9.2 No visibility changes

- Do not make `orange` public.
- Do not make `myskills` public.
- Do not change any repository from public to private or private to public.
- Do not publish or unpublish GHCR packages.
- Record mismatches between intended and actual visibility for later deliberate action.

### 9.3 No runtime changes

- Do not change application image digests or live Argo CD manifests.
- Do not deploy AI Portal.
- Do not alter live Authentik groups, OpenBao secrets, Cloudflare routes, or production services.
- Changes to `deploys` during this initiative must be documentation, validation, or conformance-only unless the operator explicitly approves otherwise.

### 9.4 Secrets and sensitive material

- Never expose secret values while auditing.
- Do not copy private inventory material into public/public-ready repositories.
- Do not assume a private repository is an acceptable secret store.
- Do not commit scan reports containing actual secrets; record sanitized findings and remediation references.
- Stop at an operator gate if a real credential is discovered in Git history and remediation would require rotation, history rewriting, or public disclosure handling.

### 9.5 Avoid overengineering

- Build only the tooling required to keep the contract enforceable.
- Write conformance tooling in **Python** (ADR 004). The agent-coaching toolchain already requires it, and it suits a CLI that parses YAML and generates text better than shell does. Note what it is *not*: `myskills` is entirely bash, so this adds a second language to the tooling surface rather than reusing one. That is the trade being made, and ADR 004 should say so. Record the decision once; do not relitigate it per script.
- Prefer small scripts with tests over a new service. No packaging ceremony until something outside `architecture` needs to import it.
- Do not create a database, dashboard, web UI, event system, or central daemon for repository governance.
- Do not add extensive schema machinery until it validates actual state.
- Do not rewrite working repository tooling solely to make names uniform.
- Do not bulk-reformat, refactor, or auto-fix existing code to satisfy newly introduced linters (§7.6).
- Comments should explain invariants, security boundaries, or non-obvious behavior—not narrate straightforward code.

### 9.6 No creation of repositories or scaffolding

- Do not create GitHub repositories. Every governed repository already exists.
- Do not scaffold application code, packages, services, or placeholder directories anywhere, including `ai-portal`.
- Cloning an existing governed repository that is absent from the local workspace is allowed; that is not creation.
- Do not change any repository's checked-out branch or HEAD state, including empty, unborn, or detached ones. Work from isolated worktrees based on the remote default branch, and leave the primary checkout exactly as found.

---

## 10. Durable state and resume protocol

`architecture` already exists, so state is canonical from the first step. No temporary external state directory is needed. The canonical location is:

```text
initiatives/active/architecture-bootstrap/
```

Maintain at least:

```text
resolved-plan.md
state.yaml
migration-map.yaml
repositories.yaml
skills.lock.yaml
open-questions.md
decisions/
journal/YYYY-MM-DD.md
evidence/
```

Do not create one enormous append-only journal. Use dated files and concise evidence summaries.

### Minimum `state.yaml`

```yaml
schema_version: 1
initiative: managed-universe-bootstrap
status: DISCOVERING
contract_path: initiatives/active/architecture-bootstrap.md
contract_digest: "sha256:..."
current_phase: reconnaissance
current_gate: planning
last_completed_step: null
next_action: inventory-governed-repositories
last_run:
  runtime: codex-or-claude-code
  tier: mid
  model: "..."
  at: "..."
repositories: {}
worktrees: {}
skills_commit: null
explicit_skill_invocations: []
completed_steps: []
open_prs: []
blockers: []
operator_action_required: null
```

### Single owner, sequential execution

All governed repositories have one owner, and the initiative is advanced by one session at a time. Concurrent orchestration is not a concern here.

- Do not build lease, heartbeat, or takeover machinery. It would be ceremony protecting against a situation that does not occur.
- `last_run` is an audit trail, not a lock. Record which runtime and model last advanced the initiative and when.
- The protections that actually matter if two sessions ever do overlap are the mechanical ones in §9.1 — isolated worktrees, one writer per worktree, never writing into a dirty or shared checkout. Those hold regardless of who is running.
- Subagents never take ownership of state. The orchestrator records their bounded assignments, worktrees, and results.

### Resume behavior

On `resume implementing architecture-bootstrap.md`:

1. Read the contract and canonical state before taking action.
2. Verify contract digest, repo HEADs, worktrees, open PRs, CI state, and blockers.
3. Reconcile drift explicitly.
4. Continue from `next_action`.
5. Do not repeat completed audits or migrations unless evidence is stale or invalid.
6. Do not ask the operator to restate facts available in Git or state.

Commit durable state frequently enough that an interruption loses little coordination work, but do not commit raw transient logs.

---

## 11. Orchestration and model delegation

The managed universe is worked on from more than one LLM ecosystem — mainly OpenAI Codex and Anthropic Claude Code. This contract names tiers, not products:

| Tier | OpenAI | Anthropic |
| --- | --- | --- |
| top | Sol | Fable |
| mid | Terra | Opus |
| low | Luna | Sonnet |

Resolve a tier to whatever concrete model the running runtime currently exposes for it. If a named model is unavailable, substitute the nearest available model **in the same tier** and record the substitution in state. Never silently drop a review step to a lower tier; if only a lower tier is available, record it as an open item for the operator rather than treating the review as done.

The operator normally invokes orchestration using a capable mid-tier model such as **Opus or Terra**.

Use higher-tier models such as **Fable or Sol** for focused, high-impact review of:

- repository ownership and source-of-truth conflicts;
- public/private boundary decisions;
- migration of shared standards;
- security-policy changes;
- exceptions that weaken a baseline;
- recurring failures whose root cause remains unclear;
- final architecture and conformance review.

Use one-tier-lower agents such as **Luna or Sonnet** for bounded execution:

- read-only repository documentation inventories;
- link and duplicate analysis;
- mechanical managed-section updates;
- profile-specific conformance changes;
- writing tests for existing specified behavior;
- running and summarizing checks;
- preparing isolated PRs.

Give every subagent a focused assignment containing:

- exact repositories and allowed paths;
- read-only or write permissions;
- expected output format;
- acceptance criteria;
- prohibited actions;
- state/evidence destination;
- maximum scope.

Subagents must not make universe-wide policy independently. The orchestrator integrates their findings and owns durable state.

Parallelize repository audits and independent PRs. Serialize changes to shared standards, managed templates, registry schemas, and `myskills`.

---

## 12. Skills and `myskills`

Keep `myskills` separate from `architecture`.

`architecture` defines approved intent and pins skill versions. `myskills` contains reusable executable behavior.

**One exception: the universe audit skill (§7.7).** It lives in `architecture/skills/audit-universe/` because it is inseparable from the catalogue, profiles, and standards it audits. Housing it in `myskills` would split one behavior across two repositories and force a version bump there for every standards edit here. It is the only skill `architecture` owns, and it does not open a general skills tree (§2). Anything reusable beyond this universe still belongs in `myskills`.

### Required process

1. Inventory existing skills before creating new ones.
2. Map initiative needs to existing skills.
3. Reuse or compose existing skills where they fit.
4. Create only missing reusable capabilities.
5. Test skill behavior and safety boundaries.
6. Commit skill changes in an isolated `myskills` worktree.
7. Record the exact `myskills` commit and selected skills in `skills.lock.yaml`.
8. Start fresh subagent sessions or explicitly reload skills before relying on newly added skills.
9. Invoke implementation skills explicitly and record each invocation in state.

Potential reusable capabilities, only if missing:

- audit a governed repository without modifying it;
- classify and reconcile documentation ownership;
- synchronize a marker-delimited agent baseline safely;
- validate a repository against a selected profile;
- materialize and verify code-quality configuration and CI gates for a declared language, including baselining pre-existing findings with each tool's native mechanism;
- audit public/private boundaries;
- coordinate isolated multi-repository worktrees;
- resume a durable cross-repository initiative.

Do not create a permanent one-off `implement-architecture-bootstrap` skill in `myskills`. Keep initiative-specific orchestration in this contract and its state. Promote only reusable procedures.

A skill may never silently widen permissions, modify unrelated repositories, rewrite history, or bypass an operator gate.

---

## 13. Gates and execution phases

### Phase 0 — Safe startup

1. Locate every governed repository and determine existence/accessibility.
2. Detect nested repositories and shared/dirty worktrees.
3. Initialize durable state in `initiatives/active/architecture-bootstrap/`.
4. Create isolated read-only discovery contexts or worktrees where needed, and clone any governed repository that is absent locally.
5. Record remote, branch, commit, intended visibility, actual visibility, accessibility, and observed languages.
6. Do not edit yet.

### Phase 1 — Discovery and synthesis

1. Audit all governed repository documentation and instructions.
2. Review ongoing shop work patterns without modifying active state.
3. Review current `myskills` capabilities.
4. Produce the content inventory and duplicate/conflict analysis.
5. Draft the repository catalogue, profiles, target standards, architecture layout, and migration map.
6. Map each repository to its declared languages from evidence, drawn from the set in §7.6: `typescript`, `python`, `ansible`, `shell`, or none. Look for shell explicitly — it hides in `scripts/`, `install`, and test harnesses rather than announcing itself.
7. Verify Habit Hooks against the installed version before any standard depends on it: the config file it reads, the snooze pipeline, plugin availability per language, and the install-extras behavior. Record the version and what was observed. The contract states these as fact; confirm them (§4).
8. Identify missing repositories and ambiguous ownership.
9. Obtain focused Fable/Sol review of the proposed authority boundaries and public/private classifications.
10. Resolve findings and create `resolved-plan.md`.

### Gate 1 — Planning complete

This is a material governance change. Stop for operator approval when all of the following are ready:

- complete repository catalogue, limited to opted-in repositories;
- target architecture layout;
- source-of-truth matrix;
- repository profile definitions;
- per-repository declared languages and the resulting code-quality rule set, including the baselining approach for pre-existing findings (§7.6);
- the four language standards — typescript, python, ansible, shell — and the CI gate each defines;
- migration map with active-work protections;
- proposed reusable-skill changes;
- the two-wave rollout plan, with the expected PR list for each wave;
- the agreed `AGENTS.md` soft target and hard ceiling, and the documentation checks that will be automated (§5.11, §5.12);
- the pruned §15 check list, with a line on each dropped check saying why;
- the security baseline: which controls land in which repository, which repositories cannot enforce branch protection, and the sanctioned secrets-delivery pattern for `deploys` (§7.5);
- empirical confirmation of Habit Hooks behavior against the installed version (§7.6);
- known exceptions and risks.

Ask for approval of the plan as a whole, not a series of routine implementation choices.

Do not begin mass documentation migration before this gate is approved.

### Wave 0 — the controls that need no governance layer

Start this immediately after Gate 1, in parallel with Phase 2. Nothing in it depends on the catalogue, the generator, the standards, or the profiles, so none of it should wait for them.

Five items carry most of the defect-catching value of this entire initiative:

1. **Renovate** — install the app, add the shared preset, one small config per repository. Dependency automation currently exists in two repositories out of twelve.
2. **gitleaks** in CI for every repository lacking it, and push protection wherever the plan offers it. Do `deploys` first: it is public and receives automated digest pushes.
3. **`kubeconform`** in `deploys`, behind the dry-run build it already has.
4. **`shellcheck`** in `myskills` — today it holds executable behavior and has no gate at all.
5. **Pin `nomadtty`'s actions and add its `permissions:` block** — it is the one CI repository still unpinned.

One PR per repository, merged before wave 2 begins.

State the reason in the plan, because it changes how the rest is judged: these five would be worth doing even if everything else in this initiative were abandoned. The governance layer that follows exists to keep them — and the instructions around them — true over time, and to make the next twelve repositories cheap. The value lands here first.

### Phase 2 — Populate `architecture`

The repository already exists locally and remotely and already holds this contract. After approval:

1. Write `standards/documentation.md` from §5.9–§5.12 first. Every later document obeys it, including the standards.
2. Add the minimal useful structure, not empty ceremonial directories.
3. Commit durable initiative state alongside the contract, without duplicating the contract.
4. Add the universe catalogue, standards, profiles, templates, initial ADRs, and conformance tooling.
5. Add `standards/code-quality.md` and a language document for each declared language.
6. Catalogue `architecture` itself; it is governed by the rules it defines.
7. Add the audit skill in `skills/audit-universe/` (§7.7), with tests, and run it once to establish the starting picture.
8. Add CI for the architecture repository itself, including the documentation checks.
9. Commit durable initiative state directly to `main`; open PRs for standards, tooling, and the audit skill. `architecture` has no CI or branch protection to discover yet — this is the workflow until it does.

### Phase 3 — Prepare reusable skills

1. Create isolated `myskills` worktree/branch.
2. Implement only missing reusable capabilities from the approved plan.
3. Add behavior-based skill tests and misuse/failure tests.
4. Run the repository's own required checks.
5. Obtain review for any skill that can write several repositories.
6. Merge or otherwise approve the skill changes according to the normal workflow.
7. Pin the resulting commit in `skills.lock.yaml`.
8. Explicitly invoke the approved pinned skills for the remaining work.

### Phase 4 — Wave 1: governance conformance

The rollout runs in two waves, each with its own branch and PR per repository. Wave 1 establishes ownership, instructions, and membership. Do not mix wave 2 work into these PRs — a governance PR that also rewires CI is unreviewable.

For each repository:

1. Create an isolated worktree and branch based on the repository's remote default branch — never on whatever the primary checkout happens to have checked out.
2. Revalidate that the target paths have not changed since planning.
3. Apply only that repository's approved migration map entries.
4. Add/update the local `AGENTS.md` with its generated managed section, `CLAUDE.md`, the README governance section, and the generated `.habit-hooks/config.toml`, written to §5.9–§5.12 and within the `AGENTS.md` budget. The config ships with the instruction that references it: an `AGENTS.md` telling an agent to run a tool whose project config does not exist yet is a broken instruction, and the self-healing text in §7.6 cures a missing binary, not a missing config.
5. Keep local architecture, current-state docs, ADRs, operational procedures, and active working state in place.
6. Remove duplicated shared material only after the central authority exists and local usability is verified.
7. Run repository-native tests and existing checks; do not add new ones here.
8. Review the diff for accidental private-data movement, and confirm it contains no reformatting or refactoring of existing code.
9. Open a focused PR with migration provenance and behavior evidence.
10. Do not merge unrelated repository changes into one branch or PR.

Parallelize independent repositories only after shared templates and standards are stable.

### Phase 5 — Wave 2: code-quality and security enablement

Begin only after wave 1 has merged for a repository and the central standards are stable. Wave 2 is where §7.5's remaining baseline controls and §7.6's gates land, one branch and PR per repository, separate from wave 1. Controls already delivered in Wave 0 are verified here, not repeated — if one is missing or has drifted, that is a finding, not a re-run.

For each repository:

1. Verify the `.habit-hooks/config.toml` materialized in wave 1 still matches what the central standard generates for its declared languages plus `generic`; regenerate if the standard moved since.
2. Verify the coaching instruction in `AGENTS.md` names the plugins that actually apply.
3. Add or extend the CI lint and static-analysis gate, reusing the repository's existing workflow rather than adding a new mechanism (§7.6).
4. Baseline pre-existing findings with each tool's native mechanism — ESLint bulk suppressions, `.ansible-lint-ignore`, `ruff --add-noqa`, Habit Hooks' snooze — commit the files, and record the counts in state. Write no custom baseline format.
5. Harden the workflows: pin third-party actions to commit SHAs, add the least-privilege `permissions:` block, and add `zizmor` over changed workflow files.
6. Add the documentation checks — `markdownlint-cli2` and `lychee` (§5.11).
7. Extend the shared Renovate preset, and confirm the app is enabled for the repository.
8. Confirm secret scanning: gitleaks in CI, and push protection wherever the plan allows it.
9. Apply the branch-protection floor where rulesets are available. Where they are not, record the named accepted risk rather than a silent gap (§7.5).
10. For `deploys` and any repository shipping Kubernetes manifests, add the dry-run build plus `kubeconform`.
11. Prove each new gate fails on a deliberate violation, then revert the fixture.
12. Confirm Habit Hooks is not wired in as a required CI check.
13. Record an explicit exception, with reasoning, for any repository or control with no applicable tooling. An empty config is not an exception.
14. Open a focused PR carrying the evidence from steps 4, 11, and 12.

A repository may not enter wave 2 without a merged wave 1: the language declarations wave 2 depends on are established there.

Wave 2 adds roughly a dozen small changes per repository. Land them in one PR per repository, not one PR per control — the operator reviews a coherent change to a repository, not fourteen fragments of policy (§13 Gate 2).

### Phase 6 — Integrated validation

Run an integrated managed-universe audit that verifies:

- every opted-in repository is registered, and no repository outside the universe was touched;
- each catalogued repository has a generated managed section matching what the catalogue produces for it;
- declared languages match what the repository actually contains, and each declared language has a CI gate and a coaching instruction;
- code-quality gates run, fail on a deliberate violation, and pass on the current tree via baselining rather than by having been disabled;
- no repository has Habit Hooks wired in as a required CI check;
- generated Habit Hooks configuration matches what the central language standard produces;
- no diff in this initiative reformats or refactors existing code;
- every `AGENTS.md` is within the agreed budget, and its command catalogue lives in `docs/` or a script (§5.12);
- documentation follows the §5.10 layout, with no stub directories and no current-state prose filed as a decision;
- local sections remain present and are not overwritten;
- local docs link to central standards where appropriate;
- central standards do not duplicate repository-specific truth;
- active initiative paths still exist and resume references remain valid;
- all intended-public repos pass public-safety checks;
- gitleaks or equivalent scans run successfully without hiding real findings;
- documentation links and referenced paths resolve;
- each repo exposes reliable check/test commands;
- repository-specific CI remains functional;
- no runtime/deployment manifests changed unintentionally;
- no repository visibility changed;
- the planned AI Portal entry is present but not implemented.

Use a Fable/Sol final review for source-of-truth coherence, overcentralization, and security boundary mistakes.

### Gate 2 — Merge and external side effects

Routine commits and PR creation may be autonomous when credentials and policy permit.

Stop only where operator involvement is genuinely required, including:

- protected-branch approval or merge requiring a human;
- repository ruleset changes requiring explicit authority;
- deletion of a disputed document;
- remediation of a real leaked credential or history rewrite;
- any repository visibility change;
- a material scope reduction or ownership decision not covered by Gate 1.

Group requested approvals so the operator can review coherent PRs rather than approving every file edit.

### Phase 7 — Completion and handoff

After all approved PRs are merged or the operator-approved equivalent is complete:

1. Re-run the integrated audit against final default branches.
2. Update repository commits, PRs, checks, and exceptions in durable state.
3. Mark the bootstrap initiative `COMPLETE`.
4. Move/archive it under `initiatives/completed/` only when doing so does not break the invocation/resume path; otherwise leave the canonical state in place with completed status and a completed index entry.
5. Produce a concise handoff covering:
   - repository purposes and relationships;
   - where standards live;
   - how local baselines are synchronized;
   - how conformance is checked, including the exact command that runs the audit skill;
   - how future work is routed;
   - open exceptions or deferred cleanup;
   - how to start the separate AI Portal initiative.

---

## 14. Repository-specific migration expectations

These are starting expectations, not substitutes for discovery.

### `orange`

- Keep Orange current-state docs, ADRs, recovery, provisioning, networking, observability, and other platform-owned material local.
- Extract only genuinely universe-wide agent, documentation, testing, public/private, or multi-repo policies.
- Preserve its public-ready posture even while GitHub visibility remains private.
- Ensure its local instructions clearly distinguish reusable/public implementation from `orange-inventory`.

### `orange-inventory`

- Keep private inventory, operations, recovery evidence, variables, and Orange-local working plans local.
- Do not move or restructure active `docs/working` initiatives.
- Replace only duplicated universe-wide policy with concise managed/local instructions.
- State clearly that cross-repository peer initiatives begin in `architecture`, while live Orange-local work remains here.

### `deploys`

- Preserve it as the public GitOps source of deployable desired state.
- Add strong public-secret and manifest-validation guidance: the dry-run build plus `kubeconform`, and the sanctioned secrets-delivery pattern — External Secrets Operator reading from OpenBao, SOPS with age as fallback (§7.5). Naming one path stops agents inventing their own.
- Keep runtime/application ownership in source repositories and promotion truth here.
- Do not alter image digests or Argo CD behavior during this initiative.

### `myskills`

- Keep executable skills, plugin code, catalogue, tests, and installation procedures local.
- Move only universe policy about when/how skills are governed into `architecture`.
- Add a clear distinction between reusable skills and initiative-specific orchestration.
- Preserve a path toward later public sanitization without making it public now.

### `plepic`

- Keep Medusa/store architecture, development, legal implementation, tests, and release procedures local.
- Use its ongoing work as evidence for durable-state and orchestration patterns, not as content to copy wholesale.
- Do not disturb active shop migration state.
- Ensure public repository and image boundaries exclude secrets and private customer/operational data.

### `robobook`

- Clone it for audit; it is not present in the local workspace.
- Keep sensitive data ignored and local, and verify the ignore rules actually hold in the public repository's history-visible state.
- Apply baseline conformance and the code-quality rules for its declared languages; do not restructure the bookkeeping workflow.

### `servitium`

- Keep application architecture, features, development commands, and tests local.
- Add only the minimum shared-governance integration.

### `nomadtty`

- Keep upstream relationship, local patches, build/test instructions, and fork decisions local.
- Add profile-specific requirements for tracking upstream and maintaining a readable delta.
- Apply the full baseline. Governance files and code-quality gates are not waived because the tree came from upstream, and upstream contribution is not a goal (§5.5).
- Expect a second, rival instruction system, not a bare fork. It carries `.claude/rules/*`, `docs/ai/` with `mistakes.md` and `decision-log.md`, a self-updating "dynamic file rule", and a sync policy for Copilot and Antigravity adapter files. Every other repository uses a plain `CLAUDE.md` pointer to `AGENTS.md`.
- Reconcile rather than delete. Decide per file whether it becomes local `AGENTS.md` content, moves under `docs/`, or stays as a tool-specific adapter; keep the hard-won `mistakes.md` content, which is exactly the local operating truth §5.1 says stays local. Record the outcome as a decision, and treat this as the largest single wave-1 job.
- List the added governance files in the delta documentation so a future upstream merge reads them as intentional local additions.

### `mihkel`

- Keep agent behavior, OpenClaw integration, tests, and public-safe runtime architecture local.
- State clearly which credentials/configuration are external.
- Do not move provider- or Discord-specific implementation details into shared standards unless they genuinely apply across repositories.

### `ai-portal`

- Register the existing public application repository and its future cross-repository initiative.
- Bring only its current scaffold and docs into baseline conformance.
- Do not invent implementation architecture or create empty complexity; record lifecycle and planned ownership.
- Leave its empty local checkout as found (§9.6); fetch from the remote rather than reading the working tree.
- Its remote `main` has no commits, so there is nothing to branch from and nothing to open a PR against. Push the initial commit directly under the §7.5 exception, then work by branch and PR from the next commit onward.

### `entpass`

- Keep business-sensitive research and development local and private.
- Apply baseline agent/security/documentation rules without forcing deployable-application conventions before the project reaches that stage.

---

## 15. Behavior-based verification

Tests must verify durable behavior, not only file existence.

At minimum provide automated checks that demonstrate:

1. The universe registry parses and validates.
2. An existing governed repository maps to exactly one profile.
3. A planned or nonexistent repository can be represented without causing false failure. (Prune candidate: every catalogued repository now exists. Keep only if the catalogue gains a genuinely planned entry.)
4. The managed baseline updater changes only text inside its markers.
5. The updater refuses missing, nested, duplicated, or malformed markers.
6. Repository-specific content survives baseline synchronization byte-for-byte outside the managed section.
7. A repository whose managed section no longer matches what `architecture` generates today is detected as stale.
8. Public repositories fail conformance when fixture secret/private patterns are introduced.
9. Private repositories are still secret-scanned.
10. Broken central/local documentation links are detected.
11. Active working-plan paths registered in the universe still exist.
12. A repository with a documented exception passes only when the exception is explicit and valid.
13. The work-routing standard carries at least one worked example per routing case, and every path those examples name exists.
14. Running the conformance tool twice is idempotent and produces no second diff.
15. No production manifest/image changes are present in this initiative's `deploys` diff.
16. A repository absent from `universe/repositories.yaml` is ignored entirely — not audited, and never reported as a conformance failure.
17. A catalogued repository whose managed section was hand-edited fails conformance, and the failure names the regeneration command that fixes it.
18. A language declared in the catalogue with no CI gate fails conformance, and a gate configured for an undeclared language also fails.
19. A violation introduced by a change fails the gate, while an identical baselined pre-existing violation in the same file does not.
20. Coaching and the gate differ in scope as specified: touching a file resurfaces its snoozed backlog to the agent, while the gate still blocks only on new findings. (Prune candidate: this tests a third-party tool's own behavior, which is machinery around the coaching layer that §7.6 declines to build.)
21. The merge gate does not depend on Habit Hooks: with the coaching tool absent entirely, the CI gate still runs and still fails on a deliberate violation.
22. A repository whose languages have no Habit Hooks plugin still runs its native linters, and its exception is explicit rather than implied by silence.
23. Regenerating a repository's Habit Hooks configuration and coaching instruction produces no diff, and changing its `languages` in the catalogue changes both.
24. A tool that cannot run — missing detector, bad config, unresolvable base ref — is reported as a tool failure and never as a pass.
25. An `AGENTS.md` over the hard ceiling fails conformance; one over the soft target is reported but passes.
26. A documentation directory that exists but holds no content fails conformance (§5.9).
27. Every file in `decisions/` carries the decision-template header — number, date, status. A current-state document filed there fails on the missing header.
28. Documentation checks run in `architecture`'s own CI and fail on a broken link and on a layout violation.
29. A workflow referencing a third-party action by tag rather than commit SHA fails the workflow lint, as does a workflow with no top-level `permissions:` block.
30. The shared Renovate preset is valid, and a repository extending it resolves to the intended configuration.
31. A manifest that `kubeconform` rejects fails the `deploys` gate before it can reach Argo CD.

**Prune this list at Gate 1.** It is a menu, not a quota. Keep the checks that are mechanical and would catch a real regression; drop the rest and record why. Roughly twenty surviving checks is a healthy outcome — a smaller executable set beats a longer aspirational one (§5.9).

Use each repository's native tests for its own code. Do not add low-value tests that assert literal prose or incidental formatting.

---

## 16. Definition of done

The initiative is complete only when all of the following are true and evidenced:

1. The private `architecture` repository — which already existed at the start — contains the populated governance system on its default branch.
2. `architecture` contains the approved universe catalogue, repository relationships, standards, profiles, templates, decisions, and durable initiative state.
3. Every opted-in repository is represented with intended and actual visibility tracked separately, and no repository outside the universe was catalogued or modified.
4. Every governed repository has a profile-appropriate local contract and agent instructions, with its managed section generated from the catalogue.
5. Shared material has one authoritative central home; local duplicated material is either removed, intentionally generated, or explicitly excepted.
6. Repository-specific current truth, ADRs, operations, recovery, and active work remain in their owning repositories.
7. No active initiative's durable state or resume path was broken.
8. `myskills` remains separate and contains only reusable executable skills/plugins, with any new skill changes tested and pinned.
9. Conformance tooling runs across the managed universe and is idempotent.
10. Public/public-ready repositories pass secret and private-boundary checks.
11. No repository visibility, production deployment, application image, or live runtime behavior changed unintentionally; no repository or scaffold was created; and no repository's primary checkout was left on a different branch or commit than it started on.
12. No diff produced by this initiative rewrote, refactored, or reformatted existing application code.
13. Every document this initiative wrote or rewrote passes the mechanical checks — layout, links, budgets. The judgment part — Minto, MECE, wording — passed a top-tier review for the three load-bearing documents: `standards/documentation.md`, the agent baseline template, and `standards/security.md`. The rest is ordinary review. Self-certification satisfies neither.
14. Every declared language has a CI gate, built on its linter's native baseline, demonstrated to fail on a newly introduced violation and to pass on baselined pre-existing ones, plus a coaching instruction generated from the central standard. No merge gate depends on Habit Hooks, and no bespoke baseline or diff-filtering code was written.
15. AI Portal is registered with its actual lifecycle and has not been implemented or scaffolded here.
16. Final default-branch CI and repository-native tests pass, or every approved exception is documented.
17. Durable state records final commits, PRs, checks, decisions, exceptions, and handoff instructions.
18. The baseline security controls of §7.5 are present in every repository that can carry them. Each control that is a CI gate was demonstrated to fail on a deliberate violation; the rest — Renovate, push protection, the branch-protection floor — are verified by configuration, since fixture-failing them means pushing credential-shaped strings at public repositories. Every repository that cannot carry a control has a named accepted risk rather than a silent gap.
19. The audit skill (§7.7) exists in `architecture`, runs across the catalogue, and its first full run is recorded in state.
20. Verified by cold test, not by assertion: for three repositories of deliberately dissimilar profiles — take `deploys`, `nomadtty`, and one application — a fresh session with no prior context opens only that repository and answers the questions below from the repository alone. Three samples catch a systemic failure; eleven would only cost ten more sessions to learn the same thing. The questions:
    - what the repository owns;
    - what it must not own;
    - how to test it;
    - which language standards apply to changes it makes;
    - how to handle secrets/public content;
    - where local work plans belong;
    - when work must be escalated to `architecture`.

Do not claim completion based only on creating the `architecture` repository or generating standards without applying and validating them.

---

## 17. Final operator report

At completion, report concisely:

- repositories audited and their final profile;
- repositories absent or inaccessible;
- central standards created, including language standards and the code-quality rule set;
- code-quality gates and coaching instructions per repository, with the pre-existing baseline counts;
- security controls landed per repository, and every repository that could not carry one;
- significant material moved or reduced;
- active work deliberately left in place;
- reusable skills added or reused and pinned commit;
- PRs/commits merged or awaiting a human-only gate;
- conformance and security-test results;
- explicit exceptions and deferred cleanup;
- exact command/path for starting the separate AI Portal initiative.

Do not include secret values or dump raw logs.
