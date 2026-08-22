# Cold test

§16 item 20 requires it: three repositories of deliberately dissimilar
profiles, a fresh session with no prior context, opening only that repository
and answering seven questions from it alone.

Run 2026-08-22 against `deploys` (`gitops-public`), `orange`
(`platform-public-ready`), and `mihkel` (`application-public`). `nomadtty`, the
contract's third suggestion, is no longer governed.

Each agent was told to read only that repository, reach no network, and report a
gap rather than fill it with a plausible guess.

## Result

**Six of seven, three times. All three failed the same question, and all three
named the same root cause first.**

| Question | deploys | orange | mihkel |
| --- | --- | --- | --- |
| What it owns | yes | yes | yes |
| What it must not own | yes | yes | yes |
| How to test it | yes | yes | yes |
| Which language standards apply | named, unreadable | named, unreadable | named, unreadable |
| Secrets and public content | yes | yes | yes |
| **Where working plans belong** | **no** | yes | **no** |
| When to escalate | partial | yes | yes |

## Finding 1: the checkouts were stale, and nothing said so

Every one of the three was behind its remote, with a clean `git status`.
`deploys` by nine commits, `mihkel` by four, `orange` by four. In each case the
missing commits were the governance work itself.

> An agent that opens this directory and starts reading finds no agent
> instructions at all. — deploys
>
> You get the pre-governance repository and you will answer half these
> questions wrong. — mihkel
>
> I would have written a plan-location note into `docs/AGENTS.md`, a file
> deleted upstream, and branched from a `main` four commits stale. — orange

This is the highest-impact finding in the whole initiative, and no mechanical
check would have caught it: every audit reads `origin/<default_branch>`, by
design, so the audit was right while the workstation was wrong.

**Fixed.** Nine checkouts fast-forwarded. `ai-portal` and `portfolio-bot` had an
unborn `HEAD`, so an agent opening them found an empty directory; both are now
on `main`. `orange/inventory` was left alone: it carries another session's
uncommitted work.

## Finding 2: nobody could say where a working plan goes

Two of three could not answer it at all, and the cause was a design error.

`work-routing.md` was marked `owner_facing`, so no generated section linked it,
and the answer lived only in a private repository the test could not open. In
`mihkel`'s case the governance merge had also **deleted** `docs/AGENTS.md`, the
only local file that had ever carried the answer.

> Unanswerable from `origin/main`. The only file that ever defined this was
> deleted in the governance merge. — mihkel

**Fixed.** Every generated section now links the standard and states the answer
outright. `orange` gets a different generated answer, because its plans go to
the private inventory rather than the public repository.

## Finding 3: the standards are behind a private door

All three named it independently. A public repository's `AGENTS.md` links six
standards in a private repository. For the owner's agents that is fine. For
anyone else it is a rule set they cannot open, and `lychee.toml` documents the
fact by excluding exactly those URLs.

> I reconstructed the enforceable subset from `scripts/validate`, the CI
> workflow, and ADR 0005. That worked, but it is reverse-engineering, not
> reading. — mihkel

Partly mitigated by finding 2's fix: the section now states the rules an agent
breaks without them, rather than only linking. The structural question — whether
`architecture` should be public — is an operator decision and out of scope here.

## Finding 4: `deploys` contains 3,376 lines of undeclared Ruby

`plepic/tests/manifests.sh` is 3,246 lines, of which **3,227 are Ruby** inside a
`<<'RUBY'` heredoc. `servitium/tests/manifests.sh` adds 149 more. `deploys`
declares `shell` only.

`shellcheck` gates the file and cannot see inside a heredoc, so it lints 19
lines of 3,246. The manifest contract assertions — the environment boundaries,
the non-root container contract, the default-deny policy — are in the 3,227.

This is the same file whose two `! grep` assertions were already found unable to
fail. Both defects live in the part no gate can see.

The language detector missed it because it reads file extensions and shebangs.
A language embedded in a heredoc is invisible to it.

## Other findings, routed rather than fixed

- **`orange` never mentions Plepic.** Zero occurrences in `README.md`,
  `AGENTS.md`, or `CONTRIBUTING.md`, despite it being the dominant recent work.
- **`scripts/validate` passing no longer means a green pull request.** Wave 2
  added `markdownlint`, `lychee`, and `zizmor` as CI jobs the local script does
  not run.
- **`mihkel`'s `WORKFLOWS.md` contradicts its own baseline**: the managed
  section says never commit to a default branch; `WORKFLOWS.md` step 5 says push
  reviewable history to `main`. The governance merge did not update it.
- **`orange`'s `.operator/` and `.bin/` are undocumented**, and `.gitleaks.toml`
  allowlists a test file that does not exist.
- **A public-safety question nobody recorded**: `mihkel` is public and carries
  RFC1918 addresses, an internal hostname, and a live n8n workflow ID. None is a
  secret value and gitleaks passes it. Nothing records that the exposure was
  considered and accepted.

## Time to orient

15 minutes for `deploys`, 25 for `mihkel`, 25 for `orange` — and in every case a
third of it was spent discovering and working around the stale checkout.

All three said they would not change *code* safely at that point. Two named the
same reason, and it was not documentation: the local gate could not run.
`mihkel` has no `bats` on this workstation; `orange`'s `scripts/bootstrap` needs
the network.

> For prose I would have been comfortable at about 15 minutes; for anything
> under `skills/`, `scripts/`, or `workflows/`, I am still not, and the blocker
> is the environment, not the documentation. — mihkel
