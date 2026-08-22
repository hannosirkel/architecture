# Repository relationships

`architecture` governs. `myskills` supplies reusable behaviour. `orange` and
`orange-inventory` are one platform split along the public/private line.
Application repositories build artifacts, `deploys` holds the desired state, and
Argo CD reconciles it.

## The map

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
├── mihkel
├── robobook
├── ai-portal
└── entpass, where and when deployable
    │
    └── CI builds and verifies immutable artifacts and images
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

## Pairs that need care

### `orange` and `orange-inventory`

`orange-inventory` is checked out at `orange/inventory`. It is a separate Git
repository with its own branches, hooks, and remote. It is not a submodule, a
subtree, or a symlink.

Public CI runs against `inventory-example/` only. It must keep working without
access to the private repository.

A change touching both is pushed private-first. See
[`standards/agent-operation.md`](../standards/agent-operation.md).

### `plepic`, `servitium`, and `deploys`

Both applications build images and promote digests into their own top-level
directory in `deploys`. Neither owns the other's directory. The repository root
of `deploys` is not deployable.

### `orange` and `deploys`

`orange` owns the Argo CD `Application` objects and the namespaces. `deploys`
owns what those Applications point at. Changing an Application is an `orange`
change; changing a workload is a `deploys` change.

### `mihkel` and `orange`

`orange` manages the Mihkel VM's host baseline: OpenClaw configuration, pinned
software, users, SSH, networking, credentials, and checkout provisioning.
`mihkel` owns the agent's own behaviour inside that baseline.

`mihkel` does not modify managed host state. It requests a change to `orange`.

### `nomadtty` and upstream

`nomadtty` is a maintained fork of
[shifulegend/nomadtty](https://github.com/shifulegend/nomadtty). It is
**catalogued but not governed**: it keeps its own instruction files,
conventions, and checks, and the conformance tooling skips it.

The universe holds as few divergences from upstream as it can, because each one
is a merge conflict waiting for whoever pulls the next upstream fix. See
[decision 007](../decisions/007-nomadtty-is-governed-by-upstream.md).

What still binds is the boundary in the catalogue: it is public, and it must not
hold Orange credentials or private host details. That is an ownership fact, not
a governance mechanic.

## Lifecycle exceptions

Two repositories do not fit the flow above, and that is recorded rather than
hidden.

| Repository | Why it differs |
| --- | --- |
| `ai-portal` | The repository exists and is public. The product is unimplemented and `main` has no commits. Registered, not built. |
| `entpass` | Early research. It has no deployable artifact and does not yet need application conventions. |
