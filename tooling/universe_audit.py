"""Audit: what a repository looks like against what the catalogue says.

Reports only. Every fix these findings imply is ordinary work in the owning
repository, routed by standards/work-routing.md.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from universe_catalogue import (
    REQUIRED_FILES,
    Problem,
    Universe,
    checkout_path,
    entry_for,
    is_governed,
)
from universe_render import (
    HABIT_CONFIG_PATH,
    export_tree,
    extract_managed_section,
    local_line_count,
    render_baseline,
    render_habit_config,
)

# standards/documentation.md owns these numbers.
AGENTS_SOFT_TARGET = 60
AGENTS_HARD_CEILING = 150

# ----------------------------------------------------------------- audit ---


def audit_repository(
    universe: Universe, name: str, path: Path | None = None
) -> list[Problem]:
    """Audit one repository against the catalogue. Reports; never fixes.

    Without `path`, the files audited come from `origin/<default_branch>`, not
    from the working tree. A working tree lags the branch — after a merge it
    lags badly — and the audit skill fetches without pulling, by design. An
    audit that describes whatever a developer happens to have checked out
    answers a question nobody asked.

    `path` overrides that, for auditing a worktree before it is pushed.
    """
    entry = entry_for(universe, name)
    if not is_governed(universe, name):
        return []
    repo = path or checkout_path(entry)

    if not repo.is_dir():
        return [
            Problem(
                name,
                "no-checkout",
                f"no checkout at {entry['local_path']}",
                f"git clone {entry['remote']} {entry['local_path']}",
                advisory=True,
            )
        ]

    if path is not None:
        return _audit_tree(universe, name, entry, repo, repo)

    ref = _resolve_ref(repo, entry.get("default_branch") or "main")
    with tempfile.TemporaryDirectory() as workspace:
        exported = Path(workspace) / "tree"
        try:
            export_tree(repo, ref, exported)
        except (OSError, subprocess.CalledProcessError) as exc:
            return [
                Problem(
                    name,
                    "cannot-read-branch",
                    f"could not export {ref}: {exc}",
                    "fetch the repository, then run the audit again",
                )
            ]
        return _audit_tree(universe, name, entry, exported, repo)


def _audit_tree(
    universe: Universe, name: str, entry: dict, path: Path, repo: Path
) -> list[Problem]:
    """`path` holds the files to inspect; `repo` is where git history lives."""
    problems: list[Problem] = []

    problems += _audit_required_files(universe, name, entry, path)
    problems += _audit_managed_section(universe, name, path)
    problems += _audit_habit_config(universe, name, path)
    problems += _audit_agents_budget(name, path)
    problems += _audit_documentation(universe, name, entry, path)
    problems += _audit_languages(universe, name, entry, path, repo)
    problems += _audit_language_gates(universe, name, entry, path)
    problems += _audit_default_branch_commits(name, entry, repo)
    return problems


def gate_text(path: Path) -> str:
    """Everything a repository's CI could run, as one searchable string.

    Reads the workflows and any validation script they call. A linter invoked
    from either one counts as a gate.
    """
    chunks = []
    for candidate in sorted((path / ".github" / "workflows").glob("*.y*ml")):
        chunks.append(candidate.read_text(encoding="utf-8", errors="ignore"))
    for candidate in ("scripts/validate", "tests/run", "scripts/check"):
        target = path / candidate
        if target.is_file():
            chunks.append(target.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def _audit_language_gates(universe, name, entry, path) -> list[Problem]:
    """A declared language needs a gate; a gate needs a declared language."""
    problems = []
    text = gate_text(path)
    if not text:
        if entry.get("languages"):
            problems.append(
                Problem(
                    name,
                    "no-ci",
                    "declares a language but has no CI workflow to gate it",
                    "add a validate workflow; see standards/code-quality.md",
                )
            )
        return problems

    declared = set(entry.get("languages") or [])
    for language, spec in sorted(universe.languages.items()):
        linters = spec.get("linters") or []
        if not linters:
            continue
        present = any(linter in text for linter in linters)
        if language in declared and not present:
            problems.append(
                Problem(
                    name,
                    "missing-gate",
                    f"declares `{language}` but CI runs none of {linters}",
                    f"add the gate from standards/languages/{language}.md",
                )
            )
        elif language not in declared and present:
            problems.append(
                Problem(
                    name,
                    "undeclared-gate",
                    f"CI runs a `{language}` linter but the catalogue does not "
                    f"declare the language",
                    f"add `{language}` to universe/repositories.yaml, or remove the gate",
                )
            )
    return problems


def _audit_required_files(universe, name, entry, path) -> list[Problem]:
    problems = []
    required = list(universe.baseline.get("required_files") or REQUIRED_FILES)
    for filename in required:
        if not (path / filename).is_file():
            problems.append(
                Problem(
                    name,
                    "missing-file",
                    f"{filename} is required in every governed repository",
                    f"tooling/universe sync-baseline {name}",
                )
            )
    return problems


def _audit_managed_section(universe, name, path) -> list[Problem]:
    agents = path / "AGENTS.md"
    if not agents.is_file():
        return []
    text = agents.read_text(encoding="utf-8")
    present = extract_managed_section(text)
    if present is None:
        return [
            Problem(
                name,
                "bad-markers",
                "AGENTS.md has missing, duplicated, or out-of-order baseline markers",
                f"tooling/universe sync-baseline {name}",
            )
        ]
    expected = render_baseline(universe, name).rstrip("\n")
    if present.rstrip("\n") != expected:
        return [
            Problem(
                name,
                "stale-baseline",
                "the managed section differs from what architecture generates today",
                f"tooling/universe sync-baseline {name}",
            )
        ]
    return []


def _audit_habit_config(universe, name, path) -> list[Problem]:
    target = path / HABIT_CONFIG_PATH
    expected = render_habit_config(universe, name)
    if not target.is_file():
        return [
            Problem(
                name,
                "missing-habit-config",
                f"{HABIT_CONFIG_PATH} is generated and must be present",
                f"tooling/universe sync-baseline {name}",
            )
        ]
    if target.read_text(encoding="utf-8") != expected:
        return [
            Problem(
                name,
                "stale-habit-config",
                f"{HABIT_CONFIG_PATH} differs from what the catalogue generates",
                f"tooling/universe sync-baseline {name}",
            )
        ]
    return []


def _audit_agents_budget(name, path) -> list[Problem]:
    agents = path / "AGENTS.md"
    if not agents.is_file():
        return []
    count = local_line_count(agents.read_text(encoding="utf-8"))
    if count > AGENTS_HARD_CEILING:
        return [
            Problem(
                name,
                "agents-md-too-long",
                f"{count} lines of local content, over the {AGENTS_HARD_CEILING} ceiling",
                "move a command catalogue to docs/current/ and link central standards",
            )
        ]
    if count > AGENTS_SOFT_TARGET:
        return [
            Problem(
                name,
                "agents-md-over-target",
                f"{count} lines of local content, over the {AGENTS_SOFT_TARGET} target",
                "move a command catalogue to docs/current/ and link central standards",
                advisory=True,
            )
        ]
    return []


def _audit_documentation(universe, name, entry, path) -> list[Problem]:
    problems = []
    profile = universe.profiles.get(entry.get("profile")) or {}

    unimplemented = entry.get("lifecycle") == "registered-not-implemented"
    for expected in [] if unimplemented else (profile.get("expected_docs") or []):
        target = path / expected
        if not target.exists():
            problems.append(
                Problem(
                    name,
                    "missing-docs",
                    f"profile `{entry['profile']}` expects {expected}",
                    advisory=True,
                )
            )

    docs = path / "docs"
    if docs.is_dir():
        loose = sorted(f.name for f in docs.glob("*.md"))
        if loose:
            problems.append(
                Problem(
                    name,
                    "uncategorised-docs",
                    f"{len(loose)} Markdown file(s) directly under docs/ with no "
                    f"stated category: {', '.join(loose)}",
                    "move each into docs/current/, decisions/, evidence/, "
                    "issues/, or working/, unless this repository's usage needs "
                    "them where they are",
                    advisory=True,
                )
            )

    for candidate in (
        "docs/current",
        "docs/decisions",
        "docs/evidence",
        "docs/issues",
        "docs/working",
    ):
        target = path / candidate
        if target.is_dir() and not any(target.iterdir()):
            problems.append(
                Problem(
                    name,
                    "empty-docs-directory",
                    f"{candidate}/ exists and holds nothing",
                    f"delete {candidate}/ or give it content",
                )
            )

    decisions = path / "docs" / "decisions"
    if not decisions.is_dir():
        decisions = path / "decisions"
    if decisions.is_dir():
        for record in sorted(decisions.glob("*.md")):
            if not _has_decision_header(record.read_text(encoding="utf-8")):
                problems.append(
                    Problem(
                        name,
                        "bad-decision-record",
                        f"{record.relative_to(path)} declares no status, so it "
                        f"reads as current-state prose filed as a decision",
                        "use templates/decision.md",
                    )
                )
    return problems


# A status, in any of the forms this universe already uses: the central
# template's `- **Status:** accepted`, `**Status:** Accepted`, `Status: Accepted`,
# or a `## Status` section.
_DECISION_STATUS = re.compile(
    r"(?mi)^(?:-\s+)?(?:\*\*)?status(?:\*\*)?\s*:\s*\S|^#{1,3}\s+status\s*$"
)


def _has_decision_header(text: str) -> bool:
    """A decision record declares a status.

    The check is deliberately not the full template. Three older formats
    predate this standard, an accepted decision is append-only, and retrofitting
    26 records would be the bulk rewriting the framework forbids. What it does
    catch is the failure the standard names: current-state prose filed as a
    decision, which declares no status at all.
    """
    return bool(_DECISION_STATUS.search(text))


_SUFFIX_EVIDENCE = {
    "python": (".py",),
    "typescript": (".ts", ".tsx", ".js", ".mjs", ".cjs"),
    "shell": (".sh", ".bats"),
}

# Ansible does not have a file extension of its own. A YAML file is not Ansible;
# every repository here has YAML. Look for the layout instead.
_ANSIBLE_DIRS = ("roles/", "playbooks/", "group_vars/", "host_vars/")
_ANSIBLE_FILES = ("ansible.cfg", "hosts.yml", "site.yaml", "site.yml")

_IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    ".next",
    "dist",
    "build",
    ".worktrees",
}


def _tracked_files(path: Path) -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    files = []
    for line in out.splitlines():
        candidate = Path(line)
        if any(part in _IGNORED_DIRS for part in candidate.parts):
            continue
        files.append(candidate)
    return files


def _audit_languages(universe, name, entry, path, repo=None) -> list[Problem]:
    """Report a declared language the repository does not contain, and vice versa."""
    problems = []
    declared = set(entry.get("languages") or [])
    files = _tracked_files(repo or path)
    if not files:
        return problems

    observed = set()
    for language, suffixes in _SUFFIX_EVIDENCE.items():
        if any(candidate.suffix in suffixes for candidate in files):
            observed.add(language)

    for candidate in files:
        posix = candidate.as_posix()
        if posix in _ANSIBLE_FILES or candidate.name in _ANSIBLE_FILES:
            observed.add("ansible")
            break
        if any(posix.startswith(prefix) for prefix in _ANSIBLE_DIRS):
            observed.add("ansible")
            break

    # Shell hides behind a shebang rather than an extension.
    if "shell" not in observed:
        for candidate in files:
            if candidate.suffix:
                continue
            full = path / candidate
            try:
                first = full.read_bytes()[:64].decode("utf-8", "ignore")
            except OSError:
                continue
            if first.startswith("#!") and ("bash" in first or "/sh" in first):
                observed.add("shell")
                break

    for language in sorted(declared - observed):
        problems.append(
            Problem(
                name,
                "language-not-found",
                f"declares `{language}` but no matching file was found",
                "remove it from the catalogue, or check the evidence",
            )
        )
    for language in sorted(observed - declared):
        problems.append(
            Problem(
                name,
                "language-not-declared",
                f"contains `{language}` but does not declare it, so it has no gate",
                f"add `{language}` to universe/repositories.yaml",
            )
        )
    return problems


def _resolve_ref(path: Path, branch: str) -> str:
    """Prefer the remote ref.

    The audit skill fetches without pulling, and forbids pulling, so a local
    branch can be arbitrarily far behind what the audit is meant to describe.
    """
    remote = f"origin/{branch}"
    try:
        subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--verify", "--quiet", remote],
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return branch
    return remote


# GitHub's squash-merge default subject. A squash merge is a single-parent
# commit, so nothing structural distinguishes it from a direct push.
_SQUASH_MERGE = re.compile(r"\(#\d+\)\s*$")


def _audit_default_branch_commits(name, entry, path, limit: int = 50) -> list[Problem]:
    """Report commits that reached the default branch without a pull request.

    Five private repositories cannot enforce this through a ruleset, so the rule
    is the enforcement and this is the check. See standards/security.md.

    Two exception shapes are read from the catalogue, and nothing is hard-coded:
    `direct_push.allowed_paths` for a repository whose durable coordination
    state commits directly, and `direct_push.allowed_subject_pattern` for one
    that receives automated pushes.

    Known limit: a rebase merge leaves no metadata at all, so it reads as a
    direct push. The manual audit resolves that against the GitHub API.
    """
    branch = entry.get("default_branch")
    if not branch:
        return []
    ref = _resolve_ref(path, branch)

    exception = entry.get("direct_push") or {}
    allowed_paths = tuple(exception.get("allowed_paths") or ())
    pattern = exception.get("allowed_subject_pattern")
    allowed_subject = re.compile(pattern) if pattern else None
    baseline = _baseline_shas(path, exception.get("baseline_commit"))

    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                str(path),
                "log",
                "--first-parent",
                f"--max-count={limit}",
                "--format=%h%x1f%p%x1f%s",
                ref,
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []

    offenders = []
    baselined = 0
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) < 3:
            continue
        sha, parents, subject = parts[0], parts[1].split(), parts[2]
        if sha in baseline:
            baselined += 1
            continue
        if len(parents) > 1:
            continue  # a merge commit is a merged pull request
        if not parents:
            continue  # a root commit predates any branch
        if _SQUASH_MERGE.search(subject):
            continue  # squash-merged pull request
        if allowed_subject and allowed_subject.search(subject):
            continue
        if allowed_paths and _only_touches(path, sha, allowed_paths):
            continue
        offenders.append(f"{sha} {subject[:60]}")

    if not offenders:
        return []
    if entry.get("supports_rulesets"):
        fix = "enable the pull-request rule in this repository's ruleset"
    else:
        fix = (
            "this repository cannot carry a ruleset on the current plan, so the "
            "rule is the enforcement; see standards/agent-operation.md"
        )
    return [
        Problem(
            name,
            "direct-push",
            f"{len(offenders)} of the last {limit} commits reached `{ref}` "
            f"without a pull request, e.g. {offenders[0]}"
            + (f" ({baselined} older commits baselined)" if baselined else ""),
            fix,
        )
    ]


def _only_touches(path: Path, sha: str, prefixes: tuple[str, ...]) -> bool:
    """True when every path a commit changed sits under one of `prefixes`."""
    try:
        changed = subprocess.run(
            ["git", "-C", str(path), "show", "--name-only", "--format=", sha],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        return False
    paths = [line for line in changed if line.strip()]
    if not paths:
        return False
    return all(p.startswith(prefixes) for p in paths)


def _baseline_shas(path: Path, baseline_commit: str | None) -> set[str]:
    """Commits at or before the governance baseline, which are not this initiative's.

    The gate blocks on new work only, using a recorded baseline. That principle
    governs linters throughout this universe; history is no different. A
    repository that had 47 direct pushes before the rule existed does not need
    to be told 47 times, and a check nobody acts on is a check nobody reads.
    """
    if not baseline_commit:
        return set()
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "log", "--format=%h", baseline_commit],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    return set(out.split())
