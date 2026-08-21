"""Rendering: markers, budgets, generated artifacts, and drift."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import universe_catalogue as cat
import universe_render as render
from test_helpers import LOCAL_CONTENT, ROOT, Fixture, _git


class MarkerTests(unittest.TestCase):
    """§15.3, §15.4, §15.5 — the updater only ever touches its own region."""

    def setUp(self):
        self.section = f"{render.BEGIN_MARKER}\nmanaged\n{render.END_MARKER}\n"

    def test_replaces_only_between_markers(self):
        original = (
            "# title\n\nbefore\n\n"
            f"{render.BEGIN_MARKER}\nold\n{render.END_MARKER}\n"
            "\nafter\n"
        )
        updated = render.replace_managed_section(original, self.section)
        self.assertIn("before", updated)
        self.assertIn("after", updated)
        self.assertIn("managed", updated)
        self.assertNotIn("old", updated)

    def test_local_content_survives_byte_for_byte(self):
        original = (
            "before\n"
            f"{render.BEGIN_MARKER}\nold\n{render.END_MARKER}"
            "\ntrailing   spaces   here\n\tand a tab\n"
        )
        updated = render.replace_managed_section(original, self.section)
        head = updated.split(render.BEGIN_MARKER)[0]
        tail = updated.split(render.END_MARKER)[-1]
        self.assertEqual("before\n", head)
        self.assertEqual("\ntrailing   spaces   here\n\tand a tab\n", tail)

    def test_refuses_a_missing_end_marker(self):
        with self.assertRaises(render.MarkerError):
            render.replace_managed_section(f"x\n{render.BEGIN_MARKER}\ny\n", self.section)

    def test_refuses_a_missing_begin_marker(self):
        with self.assertRaises(render.MarkerError):
            render.replace_managed_section(f"x\n{render.END_MARKER}\n", self.section)

    def test_refuses_duplicated_markers(self):
        text = (
            f"{render.BEGIN_MARKER}\na\n{render.END_MARKER}\n"
            f"{render.BEGIN_MARKER}\nb\n{render.END_MARKER}\n"
        )
        with self.assertRaises(render.MarkerError):
            render.replace_managed_section(text, self.section)

    def test_refuses_nested_markers(self):
        text = (
            f"{render.BEGIN_MARKER}\n{render.BEGIN_MARKER}\nx\n"
            f"{render.END_MARKER}\n{render.END_MARKER}\n"
        )
        with self.assertRaises(render.MarkerError):
            render.replace_managed_section(text, self.section)

    def test_refuses_out_of_order_markers(self):
        text = f"{render.END_MARKER}\nx\n{render.BEGIN_MARKER}\n"
        with self.assertRaises(render.MarkerError):
            render.replace_managed_section(text, self.section)

    def test_inserts_when_the_file_has_no_markers(self):
        updated = render.replace_managed_section("# title\n\nlocal rule\n", self.section)
        self.assertIn("managed", updated)
        self.assertIn("local rule", updated)
        self.assertTrue(updated.startswith("# title\n"))

    def test_refuses_a_section_that_is_not_delimited(self):
        with self.assertRaises(render.MarkerError):
            render.replace_managed_section("x\n", "not a managed section\n")


class LineBudgetTests(unittest.TestCase):
    """§15.18 — the managed section is not charged to the repository."""

    def test_managed_section_is_not_counted(self):
        text = (
            "one\ntwo\n"
            f"{render.BEGIN_MARKER}\n" + "filler\n" * 200 + f"{render.END_MARKER}\n"
            "three\n"
        )
        self.assertEqual(3, render.local_line_count(text))

    def test_counts_a_file_with_no_managed_section(self):
        self.assertEqual(2, render.local_line_count("one\ntwo\n"))

    def test_the_count_does_not_move_with_the_marker_position(self):
        managed = f"{render.BEGIN_MARKER}\nmanaged\n{render.END_MARKER}\n"
        top = managed + "\none\n\ntwo\n"
        bottom = "one\n\ntwo\n\n" + managed
        self.assertEqual(render.local_line_count(top), render.local_line_count(bottom))
        self.assertEqual(2, render.local_line_count(top))


class SyncTests(unittest.TestCase):
    """§15.3, §15.5, §15.11 — synchronization is faithful and idempotent."""

    def setUp(self):
        self.fixture = Fixture()
        self.addCleanup(self.fixture.close)
        (self.fixture.repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")

    def test_first_sync_writes_every_generated_artifact(self):
        changed = render.sync_baseline(self.fixture.universe, "example")
        self.assertEqual(
            {"AGENTS.md", "CLAUDE.md", ".habit-hooks/config.toml"}, set(changed)
        )

    def test_running_twice_produces_no_second_diff(self):
        render.sync_baseline(self.fixture.universe, "example")
        self.assertEqual([], render.sync_baseline(self.fixture.universe, "example"))

    def test_local_content_survives_synchronization(self):
        render.sync_baseline(self.fixture.universe, "example")
        text = (self.fixture.repo / "AGENTS.md").read_text(encoding="utf-8")
        for line in LOCAL_CONTENT.strip().splitlines():
            self.assertIn(line, text)

    def test_a_symlinked_claude_md_is_replaced_by_the_pointer(self):
        pointer = self.fixture.repo / "CLAUDE.md"
        pointer.symlink_to("AGENTS.md")
        render.sync_baseline(self.fixture.universe, "example")
        self.assertFalse(pointer.is_symlink())
        self.assertIn("AGENTS.md", pointer.read_text(encoding="utf-8"))

    def test_dry_run_writes_nothing(self):
        render.sync_baseline(self.fixture.universe, "example", dry_run=True)
        self.assertFalse((self.fixture.repo / "CLAUDE.md").exists())


class StandardsLinkTests(unittest.TestCase):
    """A standard an agent needs is linked where that agent reads."""

    def setUp(self):
        self.universe = cat.load(ROOT)

    def test_the_baseline_standards_appear_in_every_section(self):
        for name in self.universe.repositories:
            section = render.render_baseline(self.universe, name)
            for document in self.universe.baseline["standards"]:
                with self.subTest(repo=name, standard=document):
                    self.assertIn(document, section)

    def test_the_gitops_repository_links_the_gitops_standard(self):
        """Leaving it owner-facing meant the deploys agent never met it."""
        self.assertIn(
            "gitops-and-deployment.md", render.render_baseline(self.universe, "deploys")
        )

    def test_a_publisher_links_the_gitops_standard_despite_its_profile(self):
        """plepic and robobook share a profile; only one promotes digests."""
        self.assertIn(
            "gitops-and-deployment.md", render.render_baseline(self.universe, "plepic")
        )
        self.assertNotIn(
            "gitops-and-deployment.md", render.render_baseline(self.universe, "robobook")
        )

    def test_every_linked_standard_exists_and_every_standard_is_linked(self):
        self.assertEqual([], [str(p) for p in cat.validate(self.universe)])

    def test_an_unknown_standard_is_refused(self):
        self.universe.baseline["standards"] = ["made-up.md"]
        with self.assertRaises(cat.UniverseError):
            render.render_baseline(self.universe, "deploys")


class HabitConfigTests(unittest.TestCase):
    """§15.16 and decisions/006 — the coach never scans nothing."""

    def test_a_languageless_repository_still_gets_an_explicit_files_list(self):
        fixture = Fixture(languages=(), profile="research-private")
        self.addCleanup(fixture.close)
        config = render.render_habit_config(fixture.universe, "example")
        self.assertIn('plugins = ["generic"]', config)
        self.assertIn("files = [", config)
        self.assertIn('"**/*.md"', config)

    def test_generic_coverage_survives_a_language_plugin(self):
        """A repository that is mostly Markdown was scanning only its code."""
        fixture = Fixture(languages=("python",))
        self.addCleanup(fixture.close)
        config = render.render_habit_config(fixture.universe, "example")
        self.assertIn('"**/*.py"', config)
        self.assertIn('"**/*.md"', config)

    def test_a_language_sensor_is_scoped_to_its_own_language(self):
        """Widening the root files handed Markdown to ruff: 2592 parse errors."""
        fixture = Fixture(languages=("python",))
        self.addCleanup(fixture.close)
        config = render.render_habit_config(fixture.universe, "example")
        ruff_block = config.split("[sensors.ruff]")[1].split("[sensors.")[0]
        self.assertIn('"**/*.py"', ruff_block)
        self.assertNotIn('"**/*.md"', ruff_block)
        self.assertIn('"**/*.md"', config.split("[sensors.")[0])

    def test_a_languageless_repository_needs_no_sensor_scoping(self):
        fixture = Fixture(languages=(), profile="research-private")
        self.addCleanup(fixture.close)
        config = render.render_habit_config(fixture.universe, "example")
        self.assertNotIn("[sensors.ruff]", config)
        self.assertNotIn("[sensors.eslint]", config)

    def test_jscpd_is_disabled_without_an_npm_project(self):
        fixture = Fixture(languages=("shell",), npm_project=False)
        self.addCleanup(fixture.close)
        self.assertIn(
            "[sensors.jscpd]", render.render_habit_config(fixture.universe, "example")
        )

    def test_jscpd_stays_enabled_with_an_npm_project(self):
        fixture = Fixture(languages=("typescript",), npm_project=True)
        self.addCleanup(fixture.close)
        self.assertNotIn(
            "[sensors.jscpd]", render.render_habit_config(fixture.universe, "example")
        )

    def test_typescript_files_cover_javascript(self):
        fixture = Fixture(languages=("typescript",), npm_project=True)
        self.addCleanup(fixture.close)
        config = render.render_habit_config(fixture.universe, "example")
        self.assertIn('"**/*.js"', config)
        self.assertIn('"**/*.mjs"', config)

    def test_changing_languages_changes_the_config_and_the_instruction(self):
        before = Fixture(languages=("shell",))
        self.addCleanup(before.close)
        after = Fixture(languages=("python",))
        self.addCleanup(after.close)
        self.assertNotEqual(
            render.render_habit_config(before.universe, "example"),
            render.render_habit_config(after.universe, "example"),
        )
        self.assertNotEqual(
            render.render_baseline(before.universe, "example"),
            render.render_baseline(after.universe, "example"),
        )

    def test_the_install_command_names_every_plugin_the_universe_uses(self):
        universe = cat.load(ROOT)
        package = render.habit_hooks_package(universe)
        self.assertEqual("habit-hooks[python,typescript]", package)
        self.assertIn(package, render.render_baseline(universe, "deploys"))


class BaselineRenderTests(unittest.TestCase):
    """The generated section is complete and language-aware."""

    def setUp(self):
        self.universe = cat.load(ROOT)

    def test_no_placeholder_survives_rendering(self):
        for name in self.universe.repositories:
            with self.subTest(repo=name):
                self.assertNotIn("{{", render.render_baseline(self.universe, name))

    def test_a_languageless_repository_gets_no_language_line(self):
        self.assertNotIn(
            "Language standards", render.render_baseline(self.universe, "entpass")
        )

    def test_a_language_repository_links_its_standards(self):
        section = render.render_baseline(self.universe, "plepic")
        self.assertIn("languages/typescript.md", section)
        self.assertIn("languages/shell.md", section)

    def test_every_generated_section_is_within_its_budget(self):
        for name in self.universe.repositories:
            with self.subTest(repo=name):
                count = len(
                    render.render_baseline(self.universe, name).strip().splitlines()
                )
                self.assertLessEqual(count, 40, "the managed section budget is 40 lines")

    def test_every_standard_the_section_links_exists(self):
        section = render.render_baseline(self.universe, "mihkel")
        for fragment in (
            "agent-operation",
            "security",
            "code-quality",
            "repository-contract",
        ):
            self.assertTrue((ROOT / "standards" / f"{fragment}.md").is_file())
            self.assertIn(fragment, section)


class DriftTests(unittest.TestCase):
    """decisions/005 — a policy change reports what it just invalidated."""

    def setUp(self):
        self.fixture = Fixture()
        self.addCleanup(self.fixture.close)
        root = self.fixture.root
        _git("init", "--initial-branch=main", cwd=root)
        _git("config", "user.email", "t@example.invalid", cwd=root)
        _git("config", "user.name", "t", cwd=root)
        _git("add", "-A", cwd=root)
        _git("commit", "-m", "baseline", cwd=root)
        self.workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.workspace, True)

    def _commit(self, message: str):
        _git("add", "-A", cwd=self.fixture.root)
        _git("commit", "-m", message, cwd=self.fixture.root)

    def test_an_unrelated_change_invalidates_nothing(self):
        (self.fixture.root / "notes.md").write_text("# notes\n", encoding="utf-8")
        self._commit("docs: add notes")
        problems = render.drift(self.fixture.root, "HEAD~1", "HEAD", self.workspace)
        self.assertEqual([], problems)

    def test_a_template_change_invalidates_the_repository(self):
        template = self.fixture.root / "templates" / "agent-baseline.md"
        template.write_text(
            template.read_text(encoding="utf-8").replace(
                "Standards that apply here.", "Rules that apply here."
            ),
            encoding="utf-8",
        )
        self._commit("standards: reword the baseline")
        problems = render.drift(self.fixture.root, "HEAD~1", "HEAD", self.workspace)
        self.assertEqual(1, len(problems))
        self.assertEqual("baseline-invalidated", problems[0].check)
        self.assertIn("sync-baseline example", problems[0].fix)

    def test_a_catalogue_language_change_invalidates_the_repository(self):
        catalogue = self.fixture.root / "universe" / "repositories.yaml"
        catalogue.write_text(
            catalogue.read_text(encoding="utf-8").replace(
                "languages: [shell]", "languages: [shell, python]"
            ),
            encoding="utf-8",
        )
        self._commit("universe: declare python")
        problems = render.drift(self.fixture.root, "HEAD~1", "HEAD", self.workspace)
        self.assertEqual(["baseline-invalidated"], [p.check for p in problems])

    def test_a_parent_without_a_catalogue_reports_new_rather_than_refusing(self):
        """The first push after the catalogue lands must not crash the job."""
        (self.fixture.root / "universe" / "repositories.yaml").unlink()
        _git("add", "-A", cwd=self.fixture.root)
        _git("commit", "-m", "remove the catalogue", cwd=self.fixture.root)
        problems = render.drift(self.fixture.root, "HEAD", "HEAD~1", self.workspace)
        self.assertEqual(["new-repository"], [p.check for p in problems])

    def test_a_new_repository_is_reported_as_new(self):
        catalogue = self.fixture.root / "universe" / "repositories.yaml"
        entry = catalogue.read_text(encoding="utf-8").replace(
            "  example:", "  second:", 1
        )
        body = entry.split("repositories:\n", 1)[1]
        catalogue.write_text(
            catalogue.read_text(encoding="utf-8") + body, encoding="utf-8"
        )
        self._commit("universe: add a repository")
        problems = render.drift(self.fixture.root, "HEAD~1", "HEAD", self.workspace)
        self.assertIn("new-repository", [p.check for p in problems])


if __name__ == "__main__":
    unittest.main()
