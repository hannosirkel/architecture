"""The catalogue parses, validates, and resolves against profiles."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import universe_audit as audit
import universe_catalogue as cat
import universe_render as render
from test_helpers import ROOT


class CatalogueTests(unittest.TestCase):
    """§15.1, §15.2 — the real catalogue parses, validates, and resolves."""

    def setUp(self):
        self.universe = cat.load(ROOT)

    def test_real_catalogue_validates(self):
        self.assertEqual([], [str(p) for p in cat.validate(self.universe)])

    def test_every_repository_maps_to_exactly_one_known_profile(self):
        for name, entry in self.universe.repositories.items():
            with self.subTest(repo=name):
                self.assertIn(entry["profile"], self.universe.profiles)

    def test_every_declared_language_has_a_standard_document(self):
        for name, entry in self.universe.repositories.items():
            for language in entry["languages"]:
                with self.subTest(repo=name, language=language):
                    spec = self.universe.languages[language]
                    self.assertTrue((ROOT / spec["standard"]).is_file())

    def test_meeme_declares_node_javascript_without_becoming_an_npm_project(self):
        entry = self.universe.repositories["meeme"]

        self.assertEqual(["typescript", "shell"], entry["languages"])
        self.assertFalse(entry["npm_project"])
        # The set, not one key. Reading `exceptions["missing-gate"]` passed
        # unchanged with a second exception beside it waiving the
        # unconditional Renovate control, which is the scope this claims to
        # pin down.
        self.assertEqual({"missing-gate"}, set(entry["exceptions"]))
        exception = entry["exceptions"]["missing-gate"]
        self.assertEqual("declares `typescript`", exception["matches"])
        self.assertEqual(
            "meeme docs/decisions/0001-no-npm-project-for-javascript-gate.md",
            exception["decision"],
        )
        self.assertEqual(
            ["node --check", "node --test", "cmp"], exception["substitute"]
        )

    def test_an_ungoverned_repository_is_recognised(self):
        """A fork follows upstream's conventions; see decisions/007."""
        self.assertFalse(cat.is_governed(self.universe, "nomadtty"))
        self.assertTrue(cat.is_governed(self.universe, "plepic"))

    def test_an_ungoverned_repository_is_audited_as_nothing(self):
        self.assertEqual([], audit.audit_repository(self.universe, "nomadtty"))

    def test_sync_refuses_to_write_into_an_ungoverned_repository(self):
        """Generated files there are divergences a later upstream merge inherits."""
        with self.assertRaises(cat.UniverseError) as caught:
            render.sync_baseline(self.universe, "nomadtty")
        self.assertIn("not governed", str(caught.exception))

    def test_the_two_governance_declarations_must_agree(self):
        self.universe.repositories["nomadtty"]["governed"] = True
        checks = [p.check for p in cat.validate(self.universe)]
        self.assertIn("governance-mismatch", checks)

    def test_an_undeclared_catalogue_field_is_a_finding(self):
        """default_branch_state was the case: read by nothing, and left in the
        catalogue asserting something false after it stopped being true."""
        self.universe.repositories["orange"]["invented_field"] = "x"
        problems = [p for p in cat.validate(self.universe) if p.check == "unknown-field"]
        self.assertEqual(1, len(problems))
        self.assertIn("invented_field", problems[0].detail)
        self.assertIn("reader", problems[0].fix)

    def test_every_field_in_the_real_catalogue_is_declared(self):
        universe = cat.load(ROOT)
        used = set()
        for entry in universe.repositories.values():
            used.update(entry)
        self.assertEqual(set(), used - cat.KNOWN_REPO_FIELDS)

    def test_unknown_profile_is_a_finding(self):
        self.universe.repositories["orange"]["profile"] = "made-up"
        checks = [p.check for p in cat.validate(self.universe)]
        self.assertIn("unknown-profile", checks)

    def test_public_repository_cannot_waive_public_safety(self):
        self.universe.repositories["plepic"]["public_safe_required"] = False
        checks = [p.check for p in cat.validate(self.universe)]
        self.assertIn("unsafe-declaration", checks)

    def test_registered_working_paths_still_exist(self):
        """§15.10 — a disappeared active plan is a finding, not a silent pass."""
        for problem in cat.check_working_paths(self.universe):
            self.fail(str(problem))


class MembershipTests(unittest.TestCase):
    """§15.12 — a repository outside the catalogue is out of scope."""

    def test_an_uncatalogued_repository_is_refused_not_audited(self):
        universe = cat.load(ROOT)
        with self.assertRaises(cat.UniverseError):
            audit.audit_repository(universe, "some-personal-repo")

    def test_the_cli_refuses_an_uncatalogued_repository_distinctly(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tooling" / "universe"), "audit", "not-governed"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(2, result.returncode, "a tool that cannot run exits 2, not 1")
        self.assertIn("not in the catalogue", result.stderr)


class ToolFailureTests(unittest.TestCase):
    """§15.17 — a tool that cannot run is never reported as a pass."""

    def _run(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(ROOT / "tooling" / "universe"), *args],
            capture_output=True,
            text=True,
            cwd=cwd,
        )

    def test_a_missing_catalogue_exits_two_not_zero(self):
        empty = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, empty, True)
        result = self._run("--root", empty, "validate")
        self.assertEqual(2, result.returncode)
        self.assertIn("cannot run", result.stderr)

    def test_a_malformed_catalogue_exits_two(self):
        broken = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, broken, True)
        (broken / "universe").mkdir()
        (broken / "universe" / "repositories.yaml").write_text(
            "repositories: [unclosed\n", encoding="utf-8"
        )
        result = self._run("--root", str(broken), "validate")
        self.assertEqual(2, result.returncode)
        self.assertIn("cannot run", result.stderr)

    def test_the_cli_names_a_skip_rather_than_reporting_it_clean(self):
        """A pass for a repository nobody audited is the placebo to avoid."""
        result = self._run("audit", "nomadtty")
        self.assertIn("not governed", result.stdout)
        self.assertNotIn("clean: 1 repositories", result.stdout)

    def test_every_subcommand_runs_from_the_cli(self):
        """The module tests never invoked main(), so a shadowed name got through.

        render-baseline crashed with an AttributeError and a traceback, which is
        neither a pass nor the promised loud exit 2.
        """
        for args in (
            ["validate"],
            ["audit", "architecture"],
            ["render-baseline", "deploys"],
            ["sync-baseline", "architecture", "--dry-run"],
            ["drift", "--before", "HEAD", "--after", "HEAD"],
        ):
            with self.subTest(command=args[0]):
                result = self._run(*args)
                self.assertNotIn("Traceback", result.stderr)
                self.assertIn(
                    result.returncode,
                    (0, 1),
                    f"{args[0]} exited {result.returncode}: {result.stderr}",
                )

    def test_the_real_catalogue_validates_from_the_cli(self):
        result = self._run("validate")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("clean", result.stdout)


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
