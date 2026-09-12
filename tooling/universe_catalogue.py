"""Catalogue: loading, shared types, and validation.

`universe/repositories.yaml` is the authority on membership. This module reads
it, reads `profiles.yaml` and `universe/languages.yaml` alongside it, and checks
the three against each other.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

VISIBILITIES = {"public", "private"}
REMOTE_VISIBILITIES = {"public", "private", "unknown"}
PUBLICATION_STATUSES = {
    "published",
    "currently-private",
    "candidate",
    "not-applicable",
}

REQUIRED_FILES = ("README.md", "AGENTS.md", "CLAUDE.md")

# Every key a catalogue entry may carry. A key absent from this tuple is either
# a typo or a field nobody declared a reader for, and §5.9 wants neither. Adding
# a field means adding it here, which forces the question "what reads this?".
#
# default_branch_state was the case that prompted this: it recorded that a
# repository's main had no commits, nothing ever read it, and it stayed in the
# catalogue asserting something false after both repositories gained one.
KNOWN_REPO_FIELDS = frozenset(
    {
        # required
        "description",
        "profile",
        "remote",
        "local_path",
        "default_branch",
        "declared_visibility",
        "current_remote_visibility",
        "public_safe_required",
        "publication_status",
        "languages",
        "npm_project",
        "supports_rulesets",
        # read by the tooling
        "direct_push",
        "exceptions",
        "extra_standards",
        "governed",
        "lifecycle",
        "working_plans",
        # read by a person: they explain a decision the data cannot
        "governance_note",
        "is_fork",
        "languages_note",
        "local_checkout_note",
        "upstream",
        "visibility_reason",
        "what_still_applies",
    }
)

REQUIRED_REPO_FIELDS = (
    "description",
    "profile",
    "remote",
    "local_path",
    "default_branch",
    "declared_visibility",
    "current_remote_visibility",
    "public_safe_required",
    "publication_status",
    "languages",
    "npm_project",
    "supports_rulesets",
)


class UniverseError(Exception):
    """A condition the tool refuses to work around."""


@dataclass
class Problem:
    """One audit or validation finding.

    `advisory` marks a finding that is reported and does not fail. Use it where
    the standard states a preference rather than a rule, and where a repository's
    own usage can legitimately justify the difference. A repository may keep
    documents the central layout does not define; the audit says so, so the
    choice stays visible, and leaves the judgment to whoever owns the repository.
    """

    repo: str
    check: str
    detail: str
    fix: str = ""
    advisory: bool = False

    def __str__(self) -> str:
        mark = "note" if self.advisory else "fail"
        line = f"{mark}  {self.repo}: {self.check}: {self.detail}"
        if self.fix:
            line += f"\n      fix: {self.fix}"
        return line


@dataclass
class Universe:
    root: Path
    repositories: dict = field(default_factory=dict)
    profiles: dict = field(default_factory=dict)
    languages: dict = field(default_factory=dict)
    generic: dict = field(default_factory=dict)
    baseline: dict = field(default_factory=dict)
    standards: dict = field(default_factory=dict)
    notable_local_work: list = field(default_factory=list)


# --------------------------------------------------------------- loading ---


def find_root(start: Path | None = None) -> Path:
    """Return the architecture repository root.

    Walks up from `start` looking for universe/repositories.yaml.
    """
    here = (start or Path(__file__)).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "universe" / "repositories.yaml").is_file():
            return candidate
    raise UniverseError(
        "not inside the architecture repository: no universe/repositories.yaml found"
    )


def load(root: Path | None = None) -> Universe:
    root = root or find_root()
    repos_doc = _read_yaml(root / "universe" / "repositories.yaml")
    profiles_doc = _read_yaml(root / "profiles.yaml")
    languages_doc = _read_yaml(root / "universe" / "languages.yaml")
    standards_doc = _read_yaml(root / "standards" / "index.yaml")
    return Universe(
        root=root,
        repositories=repos_doc.get("repositories") or {},
        notable_local_work=repos_doc.get("notable_local_work") or [],
        profiles=profiles_doc.get("profiles") or {},
        baseline=profiles_doc.get("baseline") or {},
        languages=languages_doc.get("languages") or {},
        generic=languages_doc.get("generic") or {},
        standards=standards_doc.get("standards") or {},
    )


def _read_yaml(path: Path) -> dict:
    if not path.is_file():
        raise UniverseError(f"missing required file: {path}")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise UniverseError(f"{path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise UniverseError(f"{path}: expected a mapping at the top level")
    return loaded


def entry_for(universe: Universe, name: str) -> dict:
    """Return one catalogue entry, or refuse.

    A repository outside the catalogue is out of scope by construction.
    Refusing is not the same as failing it.
    """
    entry = universe.repositories.get(name)
    if entry is None:
        raise UniverseError(f"not in the catalogue: {name}")
    return entry


def exceptions_for(universe: Universe, name: str) -> dict:
    """The checks this repository has an explicit, recorded exception to.

    An exception is data, not a silence. It names the check, gives a reason, and
    links the decision that made it. `validate` refuses one that omits either,
    and reports one whose check no longer fires, so an exception cannot outlive
    the reason it was granted.
    """
    entry = universe.repositories.get(name) or {}
    return entry.get("exceptions") or {}


def is_governed(universe: Universe, name: str) -> bool:
    """Whether this universe's rules apply to a repository at all.

    A catalogued repository is normally governed. One whose profile declares
    `conformance: none` is recorded but left alone: a fork that follows its
    upstream's conventions, where every file this universe would add is a
    divergence a later upstream merge has to reconcile. See decisions/007.
    """
    entry = universe.repositories.get(name)
    if entry is None:
        return False
    if entry.get("governed") is False:
        return False
    profile = universe.profiles.get(entry.get("profile")) or {}
    return profile.get("conformance") != "none"


def checkout_path(entry: dict) -> Path:
    return Path(os.path.expanduser(entry["local_path"]))


# ------------------------------------------------------------ validation ---


def validate(universe: Universe) -> list[Problem]:
    """Check the catalogue against itself and against profiles.yaml."""
    problems: list[Problem] = []

    if not universe.repositories:
        problems.append(Problem("universe", "catalogue", "no repositories declared"))

    for name, entry in sorted(universe.repositories.items()):
        for required in REQUIRED_REPO_FIELDS:
            if required not in entry:
                problems.append(
                    Problem(name, "missing-field", f"`{required}` is not declared")
                )

        for key in sorted(set(entry) - KNOWN_REPO_FIELDS):
            problems.append(
                Problem(
                    name,
                    "unknown-field",
                    f"`{key}` is not a declared catalogue field",
                    "add it to KNOWN_REPO_FIELDS with a reader, or remove it",
                )
            )

        profile = entry.get("profile")
        if profile is not None and profile not in universe.profiles:
            problems.append(
                Problem(
                    name,
                    "unknown-profile",
                    f"`{profile}` is not defined in profiles.yaml",
                )
            )

        for language in entry.get("languages") or []:
            if language not in universe.languages:
                problems.append(
                    Problem(
                        name,
                        "unknown-language",
                        f"`{language}` is not defined in universe/languages.yaml",
                    )
                )

        declared = entry.get("declared_visibility")
        if declared is not None and declared not in VISIBILITIES:
            problems.append(
                Problem(name, "bad-visibility", f"declared_visibility `{declared}`")
            )
        remote = entry.get("current_remote_visibility")
        if remote is not None and remote not in REMOTE_VISIBILITIES:
            problems.append(
                Problem(name, "bad-visibility", f"current_remote_visibility `{remote}`")
            )
        status = entry.get("publication_status")
        if status is not None and status not in PUBLICATION_STATUSES:
            problems.append(Problem(name, "bad-status", f"publication_status `{status}`"))

        if declared == "public" and entry.get("public_safe_required") is False:
            problems.append(
                Problem(
                    name,
                    "unsafe-declaration",
                    "declared public but public_safe_required is false",
                )
            )

        # A profile that requires public safety must not be applied to a
        # repository that waives it.
        profile_spec = universe.profiles.get(profile) or {}
        if (
            profile_spec.get("public_safe_required") is True
            and entry.get("public_safe_required") is False
        ):
            problems.append(
                Problem(
                    name,
                    "profile-conflict",
                    f"profile `{profile}` requires public safety",
                )
            )

        profile_conformance = (universe.profiles.get(profile) or {}).get("conformance")
        if (entry.get("governed") is False) != (profile_conformance == "none"):
            problems.append(
                Problem(
                    name,
                    "governance-mismatch",
                    f"`governed: {entry.get('governed')}` disagrees with profile "
                    f"`{profile}`, whose conformance is `{profile_conformance}`",
                )
            )

        for check, spec in sorted((entry.get("exceptions") or {}).items()):
            if not isinstance(spec, dict):
                problems.append(
                    Problem(
                        name,
                        "malformed-exception",
                        f"exception `{check}` must be a mapping with a reason "
                        f"and a decision",
                    )
                )
                continue
            if not str(spec.get("matches") or "").strip():
                problems.append(
                    Problem(
                        name,
                        "unscoped-exception",
                        f"exception `{check}` has no `matches`, so it would "
                        f"silence every `{check}` finding, not the one granted",
                    )
                )
            for required in ("reason", "decision"):
                if not str(spec.get(required) or "").strip():
                    problems.append(
                        Problem(
                            name,
                            "malformed-exception",
                            f"exception `{check}` has no `{required}`; an "
                            f"exception without one is a silence",
                        )
                    )
            problems += _validate_substitute(name, check, spec)

        expected = _expected_publication_status(entry)
        if status is not None and expected is not None and status != expected:
            problems.append(
                Problem(
                    name,
                    "stale-publication-status",
                    f"declared {declared} and currently {remote} implies "
                    f"`{expected}`, not `{status}`",
                )
            )

        for document in entry.get("extra_standards") or []:
            if document not in universe.standards:
                problems.append(
                    Problem(
                        name,
                        "unknown-standard",
                        f"`{document}` is not in standards/index.yaml",
                    )
                )

    problems += _check_standards_are_read(universe)

    for item in universe.notable_local_work:
        repo = item.get("repository")
        if repo not in universe.repositories:
            problems.append(
                Problem(
                    repo or "?",
                    "unknown-repository",
                    "notable_local_work names a repository outside the catalogue",
                )
            )

    return problems


# A `missing-gate` exception waives a linter the standard makes unconditional.
# Saying why is not enough: prose cannot be run. `substitute` names the commands
# that stand in the waived gate's place, and the audit proves each one is still
# invoked, so removing the substitute breaks the audit rather than nothing.
SUBSTITUTED_CHECKS = ("missing-gate",)


def _validate_substitute(name: str, check: str, spec: dict) -> list[Problem]:
    """A waived gate names what runs instead, as commands rather than prose."""
    declared = spec.get("substitute")
    if declared is not None and (
        not isinstance(declared, list)
        or not all(isinstance(command, str) for command in declared)
    ):
        return [
            Problem(
                name,
                "malformed-exception",
                f"exception `{check}` has a `substitute` that is not a list of "
                f"commands",
            )
        ]

    commands = [command.strip() for command in declared or [] if command.strip()]
    if check in SUBSTITUTED_CHECKS and not commands:
        return [
            Problem(
                name,
                "unsubstituted-exception",
                f"exception `{check}` names no `substitute`, so nothing checks "
                f"that anything stands in for the gate it waives",
            )
        ]
    return []


def check_working_paths(universe: Universe) -> list[Problem]:
    """Check that every registered active working-plan path still exists."""
    problems: list[Problem] = []
    for item in universe.notable_local_work:
        name = item.get("repository")
        entry = universe.repositories.get(name)
        if entry is None:
            continue
        base = checkout_path(entry)
        if not base.exists():
            continue  # no checkout here; the audit reports that separately
        target = base / item["path"]
        if not target.exists():
            problems.append(
                Problem(
                    name,
                    "missing-working-path",
                    f"registered active work has disappeared: {item['path']}",
                    "remove the entry from notable_local_work, or restore the path",
                )
            )
    return problems


def _expected_publication_status(entry: dict) -> str | None:
    """What `declared` and `current_remote` together already imply.

    `candidate` is the one value they cannot imply: it records an intention to
    publish that nothing else in the catalogue carries.
    """
    if entry.get("publication_status") == "candidate":
        return "candidate"
    declared = entry.get("declared_visibility")
    remote = entry.get("current_remote_visibility")
    if declared == "private":
        return "not-applicable"
    if declared == "public":
        return "published" if remote == "public" else "currently-private"
    return None


def linked_standards(universe: Universe) -> set[str]:
    """Every standard some generated AGENTS.md section links."""
    linked = set(universe.baseline.get("standards") or [])
    for spec in universe.profiles.values():
        linked.update(spec.get("standards") or [])
    for entry in universe.repositories.values():
        linked.update(entry.get("extra_standards") or [])
    return linked


def _check_standards_are_read(universe: Universe) -> list[Problem]:
    """No standard exists unless a generated section links it.

    An owner-facing standard is exempt: it is linked from `architecture`'s own
    local section, which is where its reader already is.
    """
    problems = []
    linked = linked_standards(universe)
    for document in sorted(linked):
        if document not in universe.standards:
            problems.append(
                Problem(
                    "universe",
                    "unknown-standard",
                    f"`{document}` is linked but absent from standards/index.yaml",
                )
            )
        elif not (universe.root / "standards" / document).is_file():
            problems.append(
                Problem("universe", "missing-standard", f"standards/{document}")
            )
    for document, spec in sorted(universe.standards.items()):
        if spec.get("owner_facing") or document in linked:
            continue
        problems.append(
            Problem(
                "universe",
                "unlinked-standard",
                f"standards/{document} is linked from no generated section",
                "link it from profiles.yaml, or mark it owner_facing",
            )
        )
    return problems
