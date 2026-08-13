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

Create and establish a private repository named **`architecture`** as the governance and coordination layer for the complete managed engineering universe.

Then execute its first initiative: **audit the documentation and agent instructions of every governed repository, centralize genuinely universe-wide material in `architecture`, retain concise repository-owned material in each repository, and make every repository conform to the resulting engineering contract.**

The work must result in an operational governance system, not only a proposed folder tree.

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
11. The planned `ai-portal` repository and initiative registered in the managed universe, but **not implemented by this initiative**.

This is a governance/documentation/conformance initiative. It must not change production application versions, Argo CD desired state, live infrastructure behavior, or repository visibility merely to complete the bootstrap.

---

## 2. Meaning of `architecture`

`architecture` is the private engineering-governance repository. It is not:

- an application monorepo;
- a replacement for repository-local architecture documentation;
- a deployment repository;
- an inventory or secret store;
- a universal issue tracker for every small task;
- a container for all agent skills;
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
- **Current state:** create it if it does not exist.
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
- **Reason for current/public state:** deployable GitOps state must be public under current GitHub/free-tier constraints.
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

### `servitium`

- **Intended visibility:** public.
- **Purpose:** source and application-specific documentation for `servitium.future.ee`.
- **Must not contain:** private environment variables or deployment credentials.

### `nomadtty`

- **Intended visibility:** public.
- **Purpose:** maintained fork of NomadTTY with a small number of local fixes and additions.
- **Profile:** public fork; preserve upstream provenance, license obligations, patch rationale, and an understandable delta from upstream.
- **Must not contain:** Orange credentials or private host/inventory details unnecessary to the fork.

### `mihkel`

- **Intended visibility:** public.
- **Purpose:** OpenClaw-based Mihkel agent operating through Discord `#liivakast`, including public-safe source, prompts, tests, and integration code.
- **Must not contain:** Discord tokens, provider credentials, private conversation exports, or unrestricted Orange administration credentials.

### `ai-portal`

- **Intended visibility:** public.
- **Lifecycle at the start of this initiative:** planned/new initiative; the repository may or may not already exist.
- **Purpose:** `ai.future.ee` and its subprojects/integrations, including LibreChat integration and the agentic/manual Scratch playground.
- **This initiative:** register it and its intended ownership boundaries. Do not implement the AI Portal product here. Do not create the repository merely to make the catalogue green unless the approved bootstrap plan explicitly chooses to scaffold it.
- **Must not contain:** family identities, secret group membership, provider keys, OAuth sessions, or private infrastructure variables.

### `entpass`

- **Intended visibility:** private.
- **Lifecycle:** theoretical/new development for an LEI registration business.
- **Purpose:** business-sensitive research, architecture, source, and local plans for the EntityPass/LEI concept.
- **Must remain separate from:** universe-wide standards and unrelated Orange infrastructure state.

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

- a small managed baseline materialized from `architecture`;
- a repository-specific section maintained locally;
- a source/version marker for the managed baseline;
- links to fuller central standards for cross-repository or exceptional work.

`CLAUDE.md` should import or point to `AGENTS.md` using the repository's current supported convention. Codex and Claude Code must receive materially equivalent rules.

### 5.4 Controlled duplication is allowed

Avoid unmanaged duplication, not all duplication.

A generated, versioned common section in each `AGENTS.md` is acceptable because it makes local agent behavior reliable. A manually copied six-page standard that can drift is not.

Do not use cross-repository symlinks, absolute local paths, or Git submodules merely to share agent instructions.

### 5.5 Profiles, not forced identical trees

Different repository types need different local structures. Define repository profiles rather than requiring every repo to contain empty copies of the same directories.

Likely initial profiles, subject to discovery:

- `governance-private` — `architecture`;
- `platform-public-ready` — `orange`;
- `inventory-private` — `orange-inventory`;
- `gitops-public` — `deploys`;
- `skills-private` — `myskills`;
- `application-public` — `plepic`, `servitium`, `mihkel`, `ai-portal`;
- `fork-public` — `nomadtty`;
- `research-private` — `entpass`.

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
│   ├── components.yaml
│   └── relationships.md
│
├── standards/
│   ├── repository-contract.md
│   ├── documentation.md
│   ├── work-routing.md
│   ├── agent-operation.md
│   ├── multi-repository-work.md
│   ├── testing.md
│   ├── security-baseline.md
│   ├── public-private-boundaries.md
│   ├── skills-and-plugins.md
│   └── gitops-and-deployment.md
│
├── profiles/
│   ├── governance-private.yaml
│   ├── platform-public-ready.yaml
│   ├── inventory-private.yaml
│   ├── gitops-public.yaml
│   ├── skills-private.yaml
│   ├── application-public.yaml
│   ├── fork-public.yaml
│   └── research-private.yaml
│
├── templates/
│   ├── agent-baseline.md
│   ├── repository-manifest.yaml
│   ├── decision.md
│   └── initiative/
│
├── decisions/
│   ├── 001-architecture-repository-role.md
│   ├── 002-source-of-truth-and-documentation-ownership.md
│   └── 003-myskills-remains-separate.md
│
├── initiatives/
│   ├── active/
│   │   └── 2026-08-13-managed-universe-bootstrap/
│   │       ├── contract.md
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
├── tooling/
│   ├── validate-universe
│   ├── audit-repository
│   └── sync-agent-baseline
│
└── schemas/
    ├── repository.schema.json
    └── initiative-state.schema.json
```

This is a target, not permission to create empty scaffolding. Omit directories with no immediate use. Prefer a small executable system over an impressive but hollow hierarchy.

The bootstrap contract may initially live outside the repository. Once `architecture` exists, place an exact canonical copy at:

```text
architecture/initiatives/active/2026-08-13-managed-universe-bootstrap/contract.md
```

Record both the original path and content digest in state. Do not create competing edited copies.

---

## 7. Per-repository conformance contract

Every governed repository must end with a profile-appropriate, tested minimum.

### Required everywhere

Normally require:

```text
README.md
AGENTS.md
CLAUDE.md
```

Also add a small machine-readable governance marker, unless an existing equivalent is clearly better:

```text
.architecture.yaml
```

It should contain only non-duplicative coordination data, for example:

```yaml
schema_version: 1
repository_id: orange
profile: platform-public-ready
architecture_repository: architecture
managed_agent_baseline: "sha256:..."
```

Do not duplicate the full repository purpose or standards in this file when those already have authoritative homes.

### `README.md` minimum

Each README should clearly say:

- what the repository owns;
- what it does not own;
- intended visibility/public-safety status;
- how to develop and test it;
- how it is built and/or deployed, when applicable;
- where repository-local architecture and decisions live;
- where cross-repository standards and initiatives live.

### `AGENTS.md` minimum

Each `AGENTS.md` must have:

1. A generated/managed baseline section from `architecture` with source digest.
2. Repository-specific purpose and boundaries.
3. Exact test/check commands or reliable discovery instructions.
4. Public/private and secret-handling constraints relevant to the repository.
5. Rules for plans, worktrees, commits, and changes to adjacent repositories.
6. Any local exceptions to central standards, linked to an explicit decision.

Use clear markers such as:

```text
<!-- BEGIN MANAGED ARCHITECTURE BASELINE -->
...
<!-- END MANAGED ARCHITECTURE BASELINE -->
```

The sync tool may modify only the managed region. It must refuse malformed or duplicate markers.

### Documentation by profile

Use semantics, not identical trees.

Typical expectations:

- Platform/infrastructure: `docs/current/`, `docs/decisions/`, recovery/operations material.
- Private inventory: environment operations, recovery evidence, and `docs/working/` for Orange-local work.
- Applications: local architecture/current-state docs, ADRs, and optional `docs/working/` for substantial local initiatives.
- Skills: skill catalogue, tests, installation/sync instructions, and security boundaries.
- Public fork: upstream provenance, update process, patch/delta documentation, and local test procedure.
- GitOps: deployment ownership, promotion/rollback rules, validation commands, and public-secret constraints.
- Governance: universe catalogue, standards, profiles, cross-repository initiatives, and conformance tooling.

### Checks and hooks

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

Use existing working patterns when sound. Record justified profile exceptions.

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

### 8.7 Register AI Portal as planned

Add `ai-portal` to the universe with lifecycle `planned` or its discovered current state.

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
- Prefer small scripts with tests over a new service.
- Do not create a database, dashboard, web UI, event system, or central daemon for repository governance.
- Do not add extensive schema machinery until it validates actual state.
- Do not rewrite working repository tooling solely to make names uniform.
- Comments should explain invariants, security boundaries, or non-obvious behavior—not narrate straightforward code.

---

## 10. Durable state and resume protocol

Before `architecture` exists, keep temporary state beside this contract in:

```text
.architecture-bootstrap-state/
```

As soon as the repository exists, make this the canonical state location:

```text
architecture/initiatives/active/2026-08-13-managed-universe-bootstrap/
```

Maintain at least:

```text
contract.md
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
contract_path: "..."
contract_digest: "sha256:..."
current_phase: reconnaissance
current_gate: planning
last_completed_step: null
next_action: inventory-governed-repositories
orchestrator:
  runtime: codex-or-claude-code
  model: "..."
  session_id: "..."
  lease_started_at: "..."
  lease_heartbeat_at: "..."
repositories: {}
worktrees: {}
skills_commit: null
explicit_skill_invocations: []
completed_steps: []
open_prs: []
blockers: []
operator_action_required: null
```

### Single-orchestrator lease

Use a durable lease in state to prevent Codex and Claude Code from orchestrating the same initiative concurrently.

- Heartbeat the lease during work.
- A second orchestrator must stop if the lease is fresh.
- A stale lease may be taken over only after checking repository/worktree/process evidence and recording the takeover.
- Subagents do not acquire the global lease; their bounded assignments and worktrees are recorded by the orchestrator.

### Resume behavior

On `resume implementing architecture-bootstrap.md`:

1. Read the contract and canonical state before taking action.
2. Verify contract digest, lease, repo HEADs, worktrees, open PRs, CI state, and blockers.
3. Reconcile drift explicitly.
4. Continue from `next_action`.
5. Do not repeat completed audits or migrations unless evidence is stale or invalid.
6. Do not ask the operator to restate facts available in Git or state.

Commit durable state frequently enough that an interruption loses little coordination work, but do not commit raw transient logs.

---

## 11. Orchestration and model delegation

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
3. Establish temporary state and acquire the orchestrator lease.
4. Create isolated read-only discovery contexts or worktrees where needed.
5. Record remote, branch, commit, intended visibility, actual visibility, and accessibility.
6. Do not edit yet.

### Phase 1 — Discovery and synthesis

1. Audit all governed repository documentation and instructions.
2. Review ongoing shop work patterns without modifying active state.
3. Review current `myskills` capabilities.
4. Produce the content inventory and duplicate/conflict analysis.
5. Draft the repository catalogue, profiles, target standards, architecture layout, and migration map.
6. Identify missing repositories and ambiguous ownership.
7. Obtain focused Fable/Sol review of the proposed authority boundaries and public/private classifications.
8. Resolve findings and create `resolved-plan.md`.

### Gate 1 — Planning complete

This is a material governance change. Stop for operator approval when all of the following are ready:

- complete repository catalogue;
- target architecture layout;
- source-of-truth matrix;
- repository profile definitions;
- migration map with active-work protections;
- proposed reusable-skill changes;
- expected PR list;
- known exceptions and risks.

Ask for approval of the plan as a whole, not a series of routine implementation choices.

Do not begin mass documentation migration before this gate is approved.

### Phase 2 — Create and bootstrap `architecture`

After approval:

1. Create the private local `architecture` repository if absent.
2. Create the private GitHub repository when authenticated authority exists and the exact owner can be safely inferred; otherwise stop only at the repository-creation credential/approval gate.
3. Add the minimal useful structure, not empty ceremonial directories.
4. Commit the canonical contract and durable initiative state.
5. Add universe catalogue, standards, profiles, templates, initial ADRs, and conformance tooling.
6. Add CI for the architecture repository itself.
7. Push/open a PR according to the discovered repository workflow.

### Phase 3 — Prepare reusable skills

1. Create isolated `myskills` worktree/branch.
2. Implement only missing reusable capabilities from the approved plan.
3. Add behavior-based skill tests and misuse/failure tests.
4. Run the repository's own required checks.
5. Obtain review for any skill that can write several repositories.
6. Merge or otherwise approve the skill changes according to the normal workflow.
7. Pin the resulting commit in `skills.lock.yaml`.
8. Explicitly invoke the approved pinned skills for the remaining work.

### Phase 4 — Repository-by-repository conformance

For each repository:

1. Create an isolated worktree and branch from the current approved base.
2. Revalidate that the target paths have not changed since planning.
3. Apply only that repository's approved migration map entries.
4. Add/update the governance marker, local `AGENTS.md`, `CLAUDE.md`, README governance section, and profile-appropriate checks.
5. Keep local architecture, current-state docs, ADRs, operational procedures, and active working state in place.
6. Remove duplicated shared material only after the central authority exists and local usability is verified.
7. Run repository-native tests and conformance checks.
8. Review the diff for accidental private-data movement.
9. Open a focused PR with migration provenance and behavior evidence.
10. Do not merge unrelated repository changes into one branch or PR.

Parallelize independent repositories only after shared templates and standards are stable.

### Phase 5 — Integrated validation

Run an integrated managed-universe audit that verifies:

- every accessible governed repo is registered;
- each registered existing repo has the expected profile marker;
- managed agent baselines match the pinned source digest;
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

- creation of the private `architecture` remote when no safe authenticated path exists;
- protected-branch approval or merge requiring a human;
- repository ruleset changes requiring explicit authority;
- deletion of a disputed document;
- remediation of a real leaked credential or history rewrite;
- any repository visibility change;
- a material scope reduction or ownership decision not covered by Gate 1.

Group requested approvals so the operator can review coherent PRs rather than approving every file edit.

### Phase 6 — Completion and handoff

After all approved PRs are merged or the operator-approved equivalent is complete:

1. Re-run the integrated audit against final default branches.
2. Update repository commits, PRs, checks, and exceptions in durable state.
3. Mark the bootstrap initiative `COMPLETE`.
4. Move/archive it under `initiatives/completed/` only when doing so does not break the invocation/resume path; otherwise leave the canonical state in place with completed status and a completed index entry.
5. Produce a concise handoff covering:
   - repository purposes and relationships;
   - where standards live;
   - how local baselines are synchronized;
   - how conformance is checked;
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
- Add strong public-secret and manifest-validation guidance.
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

### `servitium`

- Keep application architecture, features, development commands, and tests local.
- Add only the minimum shared-governance integration.

### `nomadtty`

- Keep upstream relationship, local patches, build/test instructions, and fork decisions local.
- Add profile-specific requirements for tracking upstream and maintaining a readable delta.

### `mihkel`

- Keep agent behavior, OpenClaw integration, tests, and public-safe runtime architecture local.
- State clearly which credentials/configuration are external.
- Do not move provider- or Discord-specific implementation details into shared standards unless they genuinely apply across repositories.

### `ai-portal`

- Register as a planned public application repository and future cross-repository initiative.
- If it exists, bring only its current scaffold/docs into baseline conformance.
- If absent, do not invent implementation architecture or create empty complexity; record lifecycle and planned ownership.

### `entpass`

- Keep business-sensitive research and development local and private.
- Apply baseline agent/security/documentation rules without forcing deployable-application conventions before the project reaches that stage.

---

## 15. Behavior-based verification

Tests must verify durable behavior, not only file existence.

At minimum provide automated checks that demonstrate:

1. The universe registry parses and validates.
2. An existing governed repository maps to exactly one profile.
3. A planned/nonexistent repository can be represented without causing false failure.
4. The managed baseline updater changes only text inside its markers.
5. The updater refuses missing, nested, duplicated, or malformed markers.
6. Repository-specific content survives baseline synchronization byte-for-byte outside the managed section.
7. A stale baseline digest is detected.
8. Public repositories fail conformance when fixture secret/private patterns are introduced.
9. Private repositories are still secret-scanned.
10. Broken central/local documentation links are detected.
11. Active working-plan paths registered in the universe still exist.
12. A repository with a documented exception passes only when the exception is explicit and valid.
13. The work-routing standard correctly distinguishes local, primary-repo, and cross-repository initiatives through test fixtures or examples.
14. Running the conformance tool twice is idempotent and produces no second diff.
15. No production manifest/image changes are present in this initiative's `deploys` diff.

Use each repository's native tests for its own code. Do not add low-value tests that assert literal prose or incidental formatting.

---

## 16. Definition of done

The initiative is complete only when all of the following are true and evidenced:

1. The private `architecture` repository exists locally and remotely, unless the operator explicitly approved a temporary local-only state due to unavailable remote credentials.
2. `architecture` contains the approved universe catalogue, repository relationships, standards, profiles, templates, decisions, and durable initiative state.
3. Every accessible governed repository is represented with intended and actual visibility tracked separately.
4. Every existing governed repository has a profile-appropriate local contract and agent instructions.
5. Shared material has one authoritative central home; local duplicated material is either removed, intentionally generated, or explicitly excepted.
6. Repository-specific current truth, ADRs, operations, recovery, and active work remain in their owning repositories.
7. No active initiative's durable state or resume path was broken.
8. `myskills` remains separate and contains only reusable executable skills/plugins, with any new skill changes tested and pinned.
9. Conformance tooling runs across the managed universe and is idempotent.
10. Public/public-ready repositories pass secret and private-boundary checks.
11. No repository visibility, production deployment, application image, or live runtime behavior changed unintentionally.
12. AI Portal is registered as a planned separate initiative and has not been implemented here.
13. Final default-branch CI and repository-native tests pass, or every approved exception is documented.
14. Durable state records final commits, PRs, checks, decisions, exceptions, and handoff instructions.
15. A fresh Codex or Claude Code session opening any governed repository can identify:
    - what the repository owns;
    - what it must not own;
    - how to test it;
    - how to handle secrets/public content;
    - where local work plans belong;
    - when work must be escalated to `architecture`.

Do not claim completion based only on creating the `architecture` repository or generating standards without applying and validating them.

---

## 17. Final operator report

At completion, report concisely:

- repositories audited and their final profile;
- repositories absent or inaccessible;
- central standards created;
- significant material moved or reduced;
- active work deliberately left in place;
- reusable skills added or reused and pinned commit;
- PRs/commits merged or awaiting a human-only gate;
- conformance and security-test results;
- explicit exceptions and deferred cleanup;
- exact command/path for starting the separate AI Portal initiative.

Do not include secret values or dump raw logs.
