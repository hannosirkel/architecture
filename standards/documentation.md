# Documentation standard

Write the shortest document that keeps the meaning. State the answer first.
Give every fact one home. Use the layout below.

This standard governs every document in the managed universe, including itself.

## Layout

Use these directories. Create one when it has content.

```text
docs/
  current/     implemented behaviour — how it works today
  decisions/   numbered records for durable choices
  evidence/    append-only dated records of something that happened
  issues/      open correctness and operability problems
  working/     active plans, one file or directory per initiative
```

| Directory | Holds | Does not hold |
| --- | --- | --- |
| `current/` | present state, present tense | history, plans, rationale |
| `decisions/` | why a non-obvious choice was made | present state |
| `evidence/` | a dated record of a drill, a deployment, or a verification | present state, or a claim about it |
| `issues/` | a real problem with no active plan | a plan |
| `working/` | intent for work not yet shipped | source of truth |

No repository needs every directory. An empty directory fails conformance.

**Prefer to put every document in one of these directories.** A Markdown file
directly under `docs/` has no stated category, so a reader cannot tell whether
it is current truth, a plan, or a record of something that once happened.

**A repository may keep a document outside these categories when its own usage
needs it there.** The audit reports such a file so the choice stays visible, and
does not fail on it. This layout is the default that saves an agent from
guessing, not a rule that outranks how a repository is actually worked on. If a
path is load-bearing — named by a check, a script, or an active plan — that is a
reason to keep it, not a violation to fix.

Root documents stay few: `README.md`, `AGENTS.md`, `CLAUDE.md`. Repository
boundaries and ownership belong in `README.md`.

### `current/`

Describe what is true now. Do not narrate how it became true; Git holds that.

When behaviour changes, update the matching `current/` file in the same commit.
A current-state document that contradicts the code is worse than no document.

### `decisions/`

Record why, once, numbered and dated. Use the MADR format, from
[`templates/decision.md`](../templates/decision.md). Every file carries the
template header: number, date, status.

Write a decision when a maintainer could reasonably ask why the obvious
alternative was rejected. Do not write one for a self-evident detail.

Accepted decisions are append-only. Supersede a decision with a new one. Do not
rewrite its rationale.

Do not restate a decision in `current/`. Link it.

### `evidence/`

Record what happened, with a date. A recovery drill, a deployment, a
verification run.

Evidence is append-only. Do not rewrite a past entry; add a new one.

Evidence is not current state. `current/` says how the system works now;
`evidence/` says that on a given date somebody proved it. A claim without a
dated record behind it is not evidence.

Never record a credential, a raw hostvar, a kubeconfig, a rendered Secret, or
secret-bearing command output.

### `working/`

Hold active plans here. Archive the file when the work completes.

Fold durable facts into `current/` and rationale into `decisions/` first.

An active working record is protected. Do not relocate, rename, reformat, or
split one while its owner is still working. Doing so breaks another agent's
resume path.

## Structure: Minto

State the answer in the first paragraph. Then the supporting points, grouped.
Then the detail.

A reader who stops after the first paragraph still has the answer. Do not build
up to a conclusion.

## Grouping: MECE

Groups do not overlap, and together they cover the subject.

Two documents that claim the same fact break the one-authoritative-home rule. A
gap between sections is a missing document, not an implicit rule.

## Wording: ASD-STE100

Write Simplified Technical English.

- Use one word for one meaning. Use the same term for the same thing everywhere.
- Use the active voice. Use the imperative mood for instructions.
- Give one instruction per sentence.
- Keep a procedural sentence to 20 words, and a descriptive sentence to 25.
- Keep a paragraph to 6 sentences.
- Use the present tense for present truth.
- Do not use a synonym for variety.
- Do not use jargon a new agent cannot resolve.
- Keep articles and normal grammar. Do not write telegraphic notes.

When the three sources conflict, meaning wins over structure, and structure wins
over wording.

## Prose budget

Prefer a table, a list, or a command to a paragraph.

Do not pad with restatement, motivation, or history. Do not compress into
ambiguity: an agent that has to guess costs more than the words saved.

## `AGENTS.md` budget

An agent reads `AGENTS.md` at the start of every task, so length there is a
recurring cost.

| Measure | Limit | Result |
| --- | --- | --- |
| Local content | 60 lines | soft target; the audit reports it and passes |
| Local content | 150 lines | hard ceiling; conformance fails |
| Managed section | 45 lines | central budget; exceeding it is a standards defect |

Local content is every non-blank line outside the managed markers. The managed
section is central policy, so a repository cannot shorten it and is not charged
for it.

Blank lines do not count either. Removing the managed section leaves a blank
line behind. A count that moved with the marker position would measure that
artifact, not the content.

The ceiling gates the outrage; the target coaches the ideal. A hard failure at
the ideal length would be met by compressing into ambiguity, which costs more.

The managed budget was 40 and is 45. It was raised once, on evidence: two cold
tests opened a repository with no other context and could not say where a
working plan belongs, so the section gained the answer and the link to the
standard that owns it. Raising a self-set number because a test proved content
was missing is not the same as raising it to fit content that was not needed.
Cut something before raising it again.

Keep an `AGENTS.md` short by moving material, not by deleting meaning:

- Move a command catalogue to `docs/current/` or to a script that lists the
  commands. Name the few commands an agent needs first, then link the rest.
- Link a central standard. Do not restate it.
- Keep every line that states a rule an agent breaks without it, or a fact it
  cannot discover quickly.

Local instructions must stay operationally sufficient on their own. Do not
reduce an `AGENTS.md` to "read the architecture repository".

## Automated checks

Two tools check the mechanical part. Nothing else is automated.

| Tool | Checks |
| --- | --- |
| `markdownlint-cli2` | structure and layout |
| `lychee` | links, internal and external |

`tooling/universe audit` reports layout separately, and distinguishes the two
kinds of finding it can make:

| Marked | Meaning |
| --- | --- |
| `fail` | a rule is broken; conformance fails |
| `note` | a preference differs; reported, and it passes |

A check that fails on a preference gets ignored, and then the checks that matter
get ignored with it.

Full ASD-STE100 conformance cannot be automated. The controlled vocabulary is a
licensed specification and no certified open checker exists. A prose linter with
a hand-maintained word list would be abandoned within months, which is worse
than having none. Wording is a review concern.

Do not write a documentation checker. Use these two.
