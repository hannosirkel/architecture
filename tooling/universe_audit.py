"""Audit: what a repository looks like against what the catalogue says.

Reports only. Every fix these findings imply is ordinary work in the owning
repository, routed by standards/work-routing.md.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from universe_catalogue import (
    REQUIRED_FILES,
    Problem,
    Universe,
    checkout_path,
    entry_for,
)
from universe_render import (
    HABIT_CONFIG_PATH,
    extract_managed_section,
    local_line_count,
    render_baseline,
    render_habit_config,
)

# standards/documentation.md owns these numbers.
AGENTS_SOFT_TARGET = 60
AGENTS_HARD_CEILING = 150

# The two cases standards/agent-operation.md whitelists, and nothing else.
DIRECT_PUSH_WHITELIST_PATHS = ("initiatives/",)


# ----------------------------------------------------------------- audit ---


def audit_repository(
    universe: Universe, name: str, path: Path | None = None
) -> list[Problem]:
    """Audit one repository against the catalogue. Reports; never fixes.

    `path` overrides the catalogue's `local_path`, for auditing a worktree.
    """
    entry = entry_for(universe, name)
    path = path or checkout_path(entry)
    problems: list[Problem] = []

    if not path.is_dir():
        return [
            Problem(
                name,
                "no-checkout",
                f"no checkout at {entry['local_path']}",
                f"git clone {entry['remote']} {entry['local_path']}",
            )
        ]

    problems += _audit_required_files(universe, name, entry, path)
    problems += _audit_managed_section(universe, name, path)
    problems += _audit_habit_config(universe, name, path)
    problems += _audit_agents_budget(name, path)
    problems += _audit_documentation(universe, name, entry, path)
    problems += _audit_languages(universe, name, entry, path)
    problems += _audit_language_gates(universe, name, entry, path)
    problems += _audit_default_branch_commits(name, entry, path)
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
                f"{count} lines of local content, over the {AGENTS_SOFT_TARGET} target "
                f"(reported, not a failure)",
            )
        ]
    return []


def _audit_documentation(universe, name, entry, path) -> list[Problem]:
    problems = []
    profile = universe.profiles.get(entry.get("profile")) or {}

    for expected in profile.get("expected_docs") or []:
        target = path / expected
        if not target.exists():
            problems.append(
                Problem(
                    name,
                    "missing-docs",
                    f"profile `{entry['profile']}` expects {expected}",
                )
            )

    for candidate in ("docs/current", "docs/decisions", "docs/issues", "docs/working"):
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
                        f"{record.relative_to(path)} has no number, date, "
                        f"and status header",
                        "use templates/decision.md",
                    )
                )
    return problems


_DECISION_TITLE = re.compile(r"^#\s*\d+\.\s+\S")
_DECISION_DATE = re.compile(r"(?mi)^-\s+\*\*date:\*\*\s+\d{4}-\d{2}-\d{2}\s*$")
_DECISION_STATUS = re.compile(r"(?mi)^-\s+\*\*status:\*\*\s+\S")


def _has_decision_header(text: str) -> bool:
    head = text.lstrip()
    first = head.splitlines()[0] if head.splitlines() else ""
    return bool(
        _DECISION_TITLE.match(first)
        and _DECISION_DATE.search(text)
        and _DECISION_STATUS.search(text)
    )


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


def _audit_languages(universe, name, entry, path) -> list[Problem]:
    """Report a declared language the repository does not contain, and vice versa."""
    problems = []
    declared = set(entry.get("languages") or [])
    files = _tracked_files(path)
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


def _audit_default_branch_commits(name, entry, path, limit: int = 50) -> list[Problem]:
    """Report commits that reached the default branch without a pull request.

    Five private repositories cannot enforce this through a ruleset, so the rule
    is the enforcement and this is the check. See standards/security.md.
    """
    branch = entry.get("default_branch")
    if not branch:
        return []
    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                str(path),
                "log",
                "--first-parent",
                f"--max-count={limit}",
                "--format=%h%x1f%p%x1f%s%x1f%D",
                branch,
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []

    offenders = []
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) < 3:
            continue
        sha, parents, subject = parts[0], parts[1].split(), parts[2]
        if len(parents) > 1:
            continue  # a merge commit is a merged pull request
        if subject.startswith("Merge pull request"):
            continue
        if _is_whitelisted_direct_push(path, sha):
            continue
        offenders.append(f"{sha} {subject[:60]}")

    if not offenders:
        return []
    return [
        Problem(
            name,
            "direct-push",
            f"{len(offenders)} of the last {limit} commits reached `{branch}` "
            f"without a pull request, e.g. {offenders[0]}",
            "branch and open a pull request; see standards/agent-operation.md",
        )
    ]


def _is_whitelisted_direct_push(path: Path, sha: str) -> bool:
    """Durable initiative state, and an empty repository's first commit."""
    try:
        changed = subprocess.run(
            ["git", "-C", str(path), "show", "--name-only", "--format=%P", sha],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        return False
    if not changed:
        return False
    if not changed[0].strip():
        return True  # a root commit has no parent
    paths = [line for line in changed[1:] if line.strip()]
    if not paths:
        return False
    return all(
        any(p.startswith(prefix) for prefix in DIRECT_PUSH_WHITELIST_PATHS) for p in paths
    )
