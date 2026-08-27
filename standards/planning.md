# Planning standard

Size every row of a working plan so that one reviewable pull request closes it.
A row that one pull request cannot close is not a row. It is a task, and it is
decomposed before the plan is approved.

[`work-routing.md`](./work-routing.md) decides where a plan lives. This standard
decides how the plan is written.

## The unit of work

A row is one `- [ ]` checkbox. Size it by how it closes, not by how it reads.

| Rule | The row is wrong when |
| --- | --- |
| One row closes with one pull request | closing it needs two pull requests |
| A row names the files it changes | nobody can tell what the row touches |
| That file list stays inside one repository | it names files in two repositories |
| A row states how it is verified | no command or artifact proves it done |

**Cross-repository work is two rows with a stated order**, one per repository,
not one row that spans both. The order is part of the plan, not a runtime
discovery.

Where a plan format declares files per task rather than per row, the file rules
above apply to the pull-request unit the task splits into. One row, one pull
request, one repository is the shape either way.

**A row that needs its own design document to become implementable was approved
too coarse.** Write the design, then rewrite the row. Do not carry a design
document as a substitute for a row that was never sized.

Decomposition happens before approval. A plan is approved once, and running it
is not the time to find out that a row is a project.

## Pull-request size

Size is a gate, not a signal.

| Bound | Trips the gate at |
| --- | --- |
| Changed lines | more than 800 |
| Files | more than 10 |

Aim at 400–800 lines. Generated lockfiles are excluded from both counts, and
their paths and line count are named in the pull-request body.

**Over either bound, the pull request carries a named override.** It states who
approved it and why the work could not be split. A reviewer refuses a pull
request that is over a bound and carries no override, and an author does not
approve their own. No check counts lines: this one is a review concern.

One build merged 30 of 44 pull requests over the bound, the largest at 8,047
hand-written lines across 70 files.

## Documentation stands up first

Where the repository's profile expects a docs tree, it stands up with content
before the first implementation row runs. Make that the plan's first row.

| Directory | What the plan puts there first | Create it when |
| --- | --- | --- |
| `docs/current/` | the behaviour the plan starts from | the profile expects it |
| `docs/decisions/` | the decisions the plan already made | the plan made one |
| `docs/issues/` | the known problems the plan does not close | there is one |

**Create a directory only once it has content.** An empty one fails
conformance, so this section never requires an empty directory. A profile that
says a docs tree does not belong governs over this section; `gitops-public`
says exactly that.

[`documentation.md`](./documentation.md) owns the layout and
[`profiles.yaml`](../profiles.yaml) owns which tree a repository keeps. This
standard fixes only when it stands up.

Durable knowledge lands somewhere whether or not there is a home for it. One
application `README.md` grew from 1,824 to 135,084 bytes in 13 days, because no
other directory existed to receive it.
