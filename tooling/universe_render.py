"""Rendering: templates, managed markers, and generated artifacts.

Every file this writes is generated from the catalogue. Nothing here decides
policy; it materializes what the catalogue and the templates already say.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from universe_catalogue import (
    Problem,
    Universe,
    UniverseError,
    checkout_path,
    entry_for,
    load,
)

ARCHITECTURE_URL = "https://github.com/hannosirkel/architecture"
STANDARDS_URL = f"{ARCHITECTURE_URL}/blob/main/standards"

BEGIN_MARKER = "<!-- BEGIN MANAGED ARCHITECTURE BASELINE -->"
END_MARKER = "<!-- END MANAGED ARCHITECTURE BASELINE -->"

HABIT_CONFIG_PATH = Path(".habit-hooks/config.toml")

GENERATED_NOTICE = (
    "Generated from hannosirkel/architecture. Do not edit by hand.\n"
    "Regenerate with: tooling/universe sync-baseline {repo}"
)


class MarkerError(UniverseError):
    """The managed markers are missing, duplicated, nested, or out of order."""


# ------------------------------------------------------------- rendering ---


def habit_hooks_package(universe: Universe) -> str:
    """The one install command for the whole universe.

    `uv tool install` replaces extras rather than adding them, so every plugin
    the universe uses must be named in a single command. Verified against
    habit-hooks 1.3.1; see standards/code-quality.md.
    """
    plugins = set()
    for entry in universe.repositories.values():
        for language in entry.get("languages") or []:
            plugin = (universe.languages.get(language) or {}).get("habit_plugin")
            if plugin:
                plugins.add(plugin)
    if not plugins:
        return "habit-hooks"
    return f"habit-hooks[{','.join(sorted(plugins))}]"


def language_standards_line(universe: Universe, entry: dict) -> str:
    languages = entry.get("languages") or []
    if not languages:
        return ""
    links = []
    for language in languages:
        spec = universe.languages.get(language)
        if spec is None:
            raise UniverseError(f"undeclared language in languages.yaml: {language}")
        name = Path(spec["standard"]).name
        links.append(f"[{language}]({STANDARDS_URL}/languages/{name})")
    return "- Language standards: " + ", ".join(links) + "\n"


def render_baseline(universe: Universe, name: str) -> str:
    """Render the managed AGENTS.md section for one repository."""
    entry = entry_for(universe, name)
    template = (universe.root / "templates" / "agent-baseline.md").read_text(
        encoding="utf-8"
    )
    languages = entry.get("languages") or []
    if entry["public_safe_required"]:
        safety = "This repository must be safe to publish."
    else:
        safety = "This repository is private, which is not the same as secret."
    values = {
        "repo": name,
        "architecture_url": ARCHITECTURE_URL,
        "standards_url": STANDARDS_URL,
        "profile": entry["profile"],
        "declared_visibility": entry["declared_visibility"],
        "current_remote_visibility": entry["current_remote_visibility"],
        "public_safe_required": "yes" if entry["public_safe_required"] else "no",
        "languages_display": ", ".join(languages) if languages else "none",
        "language_standards_line": language_standards_line(universe, entry),
        "default_branch": entry["default_branch"],
        "public_safety_line": safety,
        "habit_hooks_package": habit_hooks_package(universe),
    }
    return _substitute(template, values)


def render_claude_pointer(universe: Universe, name: str) -> str:
    entry_for(universe, name)
    template = (universe.root / "templates" / "claude-md-pointer.md").read_text(
        encoding="utf-8"
    )
    return _substitute(template, {"repo": name})


def render_habit_config(universe: Universe, name: str) -> str:
    """Render .habit-hooks/config.toml for one repository.

    The `files` list is always explicit. A generic-only config that declares no
    files scans nothing and reports success; see decisions/006.
    """
    entry = entry_for(universe, name)
    languages = entry.get("languages") or []

    plugins: list[str] = []
    files: list[str] = []
    for language in languages:
        spec = universe.languages.get(language)
        if spec is None:
            raise UniverseError(f"undeclared language in languages.yaml: {language}")
        plugin = spec.get("habit_plugin")
        if plugin and plugin not in plugins:
            plugins.append(plugin)
        for pattern in spec.get("habit_files") or []:
            if pattern not in files:
                files.append(pattern)

    generic_plugin = universe.generic.get("habit_plugin", "generic")
    plugins.append(generic_plugin)

    if not any(
        (universe.languages.get(language) or {}).get("habit_plugin")
        for language in languages
    ):
        # No language plugin applies, so nothing has declared any files.
        for pattern in universe.generic.get("fallback_files") or []:
            if pattern not in files:
                files.append(pattern)

    lines = [f"# {line}" for line in GENERATED_NOTICE.format(repo=name).splitlines()]
    lines.append("")
    lines.append("plugins = [" + ", ".join(f'"{p}"' for p in plugins) + "]")
    lines.append("files = [")
    for pattern in files:
        lines.append(f'  "{pattern}",')
    lines.append("]")

    max_lines = universe.generic.get("max_file_lines")
    if max_lines:
        lines.append("")
        lines.append("# The plugin default is 200; the universe standard is this.")
        lines.append("[sensors.line-count]")
        lines.append(f'args = ["--max", "{max_lines}"]')

    if not entry["npm_project"]:
        for sensor in universe.generic.get("needs_npm_project") or []:
            lines.append("")
            lines.append(f"# No npm project here, so {sensor} cannot resolve from")
            lines.append("# node_modules/.bin. line-count is built in and still runs.")
            lines.append(f"[sensors.{sensor}]")
            lines.append("disabled = true")

    return "\n".join(lines) + "\n"


def _substitute(template: str, values: dict) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", str(value))
    leftover = re.findall(r"\{\{(\w+)\}\}", rendered)
    if leftover:
        raise UniverseError(f"template placeholder not substituted: {leftover[0]}")
    return rendered


# --------------------------------------------------------------- markers ---


def replace_managed_section(text: str, section: str) -> str:
    """Return `text` with its managed region replaced by `section`.

    Refuses missing-one-marker, duplicated, nested, and out-of-order markers.
    Inserts the section when the file carries no markers at all.
    """
    if not section.startswith(BEGIN_MARKER) or not section.rstrip().endswith(END_MARKER):
        raise MarkerError("the rendered section is not delimited by both markers")

    begins = _positions(text, BEGIN_MARKER)
    ends = _positions(text, END_MARKER)

    if not begins and not ends:
        return _insert_section(text, section)
    if len(begins) != 1 or len(ends) != 1:
        raise MarkerError(
            f"expected one begin marker and one end marker, "
            f"found {len(begins)} and {len(ends)}"
        )
    begin, end = begins[0], ends[0]
    if begin > end:
        raise MarkerError("the end marker comes before the begin marker")

    head = text[:begin]
    tail = text[end + len(END_MARKER) :]
    return head + section.rstrip("\n") + tail


def _positions(text: str, marker: str) -> list[int]:
    found, start = [], 0
    while True:
        index = text.find(marker, start)
        if index == -1:
            return found
        found.append(index)
        start = index + len(marker)


def _insert_section(text: str, section: str) -> str:
    """Insert the section after the file's title, or at the top."""
    if not text.strip():
        return section
    lines = text.splitlines(keepends=True)
    insert_at = 0
    if lines and lines[0].startswith("# "):
        insert_at = 1
        while insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1
    head = "".join(lines[:insert_at])
    tail = "".join(lines[insert_at:])
    if head and not head.endswith("\n"):
        head += "\n"
    if head and not head.endswith("\n\n"):
        head += "\n"
    if tail and not tail.startswith("\n"):
        tail = "\n" + tail
    return head + section.rstrip("\n") + "\n" + tail


def strip_managed_section(text: str) -> str:
    begins = _positions(text, BEGIN_MARKER)
    ends = _positions(text, END_MARKER)
    if len(begins) != 1 or len(ends) != 1 or begins[0] > ends[0]:
        return text
    return text[: begins[0]] + text[ends[0] + len(END_MARKER) :]


def local_line_count(text: str) -> int:
    """Count the non-blank lines of an AGENTS.md outside the managed section.

    The managed section is central policy. A repository cannot shorten it, so it
    is not charged for it. Blank lines are not counted either: removing the
    managed section leaves one behind, and a count that moved with the marker
    position would measure an artifact rather than content.

    See standards/documentation.md.
    """
    local = strip_managed_section(text)
    return sum(1 for line in local.splitlines() if line.strip())


def extract_managed_section(text: str) -> str | None:
    begins = _positions(text, BEGIN_MARKER)
    ends = _positions(text, END_MARKER)
    if len(begins) != 1 or len(ends) != 1 or begins[0] > ends[0]:
        return None
    return text[begins[0] : ends[0] + len(END_MARKER)]


# ----------------------------------------------------------------- drift ---


def _export(repo: Path, ref: str, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", ref],
        capture_output=True,
        check=True,
    ).stdout
    subprocess.run(["tar", "-x", "-C", str(destination)], input=archive, check=True)


def baselines_at(repo: Path, ref: str, workspace: Path) -> dict[str, str]:
    """Render every repository's managed section as `architecture` was at `ref`.

    Exports the tree rather than switching branches, so it never disturbs a
    working checkout.
    """
    destination = workspace / ref.replace("/", "_")
    _export(repo, ref, destination)
    try:
        universe = load(destination)
    except UniverseError:
        # The catalogue did not exist yet at this ref. Every repository is new
        # rather than changed; that is a report, not a reason to refuse.
        return {}
    return {name: render_baseline(universe, name) for name in universe.repositories}


def drift(repo: Path, before: str, after: str, workspace: Path) -> list[Problem]:
    """Report which repositories a change to `architecture` just invalidated.

    Compares two generated outputs, so it needs no clones and no token.
    """
    old = baselines_at(repo, before, workspace)
    new = baselines_at(repo, after, workspace)

    problems = []
    for name in sorted(set(old) | set(new)):
        if name not in old:
            problems.append(
                Problem(name, "new-repository", "joined the catalogue in this change")
            )
        elif name not in new:
            problems.append(
                Problem(name, "removed-repository", "left the catalogue in this change")
            )
        elif old[name] != new[name]:
            problems.append(
                Problem(
                    name,
                    "baseline-invalidated",
                    "this change alters its generated AGENTS.md section",
                    f"tooling/universe sync-baseline {name}, then open a pull request",
                )
            )
    return problems


# ----------------------------------------------------------------- write ---


def sync_baseline(
    universe: Universe,
    name: str,
    dry_run: bool = False,
    path: Path | None = None,
) -> list[str]:
    """Materialise every generated artifact for one repository.

    Returns the paths that changed. Running it twice produces no second diff.

    `path` overrides the catalogue's `local_path`. Agents work in isolated
    worktrees, so the generated files usually have to land somewhere other than
    the primary checkout.
    """
    entry = entry_for(universe, name)
    path = path or checkout_path(entry)
    if not path.is_dir():
        raise UniverseError(f"no checkout at {path}")

    changed: list[str] = []

    agents = path / "AGENTS.md"
    section = render_baseline(universe, name)
    current = agents.read_text(encoding="utf-8") if agents.is_file() else f"# {name}\n"
    updated = replace_managed_section(current, section)
    if not updated.endswith("\n"):
        updated += "\n"
    if updated != current or not agents.is_file():
        changed.append("AGENTS.md")
        if not dry_run:
            agents.write_text(updated, encoding="utf-8")

    pointer = path / "CLAUDE.md"
    pointer_text = render_claude_pointer(universe, name)
    if not pointer.is_file() or pointer.read_text(encoding="utf-8") != pointer_text:
        changed.append("CLAUDE.md")
        if not dry_run:
            if pointer.is_symlink():
                pointer.unlink()
            pointer.write_text(pointer_text, encoding="utf-8")

    habit = path / HABIT_CONFIG_PATH
    habit_text = render_habit_config(universe, name)
    if not habit.is_file() or habit.read_text(encoding="utf-8") != habit_text:
        changed.append(str(HABIT_CONFIG_PATH))
        if not dry_run:
            habit.parent.mkdir(parents=True, exist_ok=True)
            habit.write_text(habit_text, encoding="utf-8")

    return changed
