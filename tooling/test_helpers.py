"""Shared fixtures for the universe tests.

A throwaway universe on disk, plus the local AGENTS.md content every
synchronization test checks survives byte-for-byte.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import universe_catalogue as cat

ROOT = Path(__file__).resolve().parent.parent

LOCAL_CONTENT = """# example

Local rules that must survive synchronization unchanged.

- Run `bash scripts/validate` before handoff.
- Never commit a per-environment value.
"""


def _git(*args: str, cwd: Path) -> None:
    subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
    )


class Fixture:
    """A throwaway universe with one repository, on disk."""

    def __init__(
        self,
        languages=("shell",),
        npm_project=False,
        profile="application-public",
        direct_push=None,
        extra_standards=None,
        supports_rulesets=True,
    ):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "architecture"
        self.repo = self.tmp / "example"
        self.repo.mkdir(parents=True)

        for relative in (
            "templates/agent-baseline.md",
            "templates/claude-md-pointer.md",
            "universe/languages.yaml",
            "standards/index.yaml",
            "profiles.yaml",
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / relative, target)

        languages_yaml = "[" + ", ".join(languages) + "]"
        (self.root / "universe" / "repositories.yaml").write_text(
            "schema_version: 1\n"
            "repositories:\n"
            "  example:\n"
            "    description: A fixture.\n"
            f"    profile: {profile}\n"
            "    remote: https://example.invalid/example.git\n"
            f'    local_path: "{self.repo}"\n'
            "    default_branch: main\n"
            "    declared_visibility: public\n"
            "    current_remote_visibility: public\n"
            "    public_safe_required: true\n"
            "    publication_status: published\n"
            f"    languages: {languages_yaml}\n"
            f"    npm_project: {'true' if npm_project else 'false'}\n"
            f"    supports_rulesets: {'true' if supports_rulesets else 'false'}\n"
            + (f"    direct_push:\n{direct_push}" if direct_push else "")
            + (
                f"    extra_standards: [{', '.join(extra_standards)}]\n"
                if extra_standards
                else ""
            ),
            encoding="utf-8",
        )
        self.universe = cat.load(self.root)

    def reload(self):
        self.universe = cat.load(self.root)
        return self.universe

    def close(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
