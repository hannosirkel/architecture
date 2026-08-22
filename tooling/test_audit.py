"""The audit reports what a repository looks like against the catalogue."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import universe_audit as audit
import universe_catalogue as cat
import universe_render as render
from test_helpers import LOCAL_CONTENT, ROOT, Fixture, _git


class StalenessTests(unittest.TestCase):
    """§15.6, §15.7 — staleness is a diff, and the finding names the fix."""

    def setUp(self):
        self.fixture = Fixture()
        self.addCleanup(self.fixture.close)
        (self.fixture.repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(self.fixture.universe, "example")

    def _checks(self):
        return {
            p.check: p
            for p in audit.audit_repository(
                self.fixture.universe, "example", path=self.fixture.repo
            )
        }

    def test_a_synchronized_repository_has_no_baseline_finding(self):
        found = self._checks()
        self.assertNotIn("stale-baseline", found)
        self.assertNotIn("stale-habit-config", found)

    def test_a_hand_edited_managed_section_fails_and_names_the_command(self):
        agents = self.fixture.repo / "AGENTS.md"
        text = agents.read_text(encoding="utf-8").replace("Profile", "Prof1le")
        agents.write_text(text, encoding="utf-8")
        found = self._checks()
        self.assertIn("stale-baseline", found)
        self.assertIn("sync-baseline example", found["stale-baseline"].fix)

    def test_a_policy_change_makes_every_repository_stale(self):
        template = self.fixture.root / "templates" / "agent-baseline.md"
        template.write_text(
            template.read_text(encoding="utf-8").replace(
                "Standards that apply here.", "Rules that apply here."
            ),
            encoding="utf-8",
        )
        self.fixture.reload()
        self.assertIn("stale-baseline", self._checks())

    def test_a_hand_edited_habit_config_fails(self):
        target = self.fixture.repo / render.HABIT_CONFIG_PATH
        target.write_text('plugins = ["generic"]\n', encoding="utf-8")
        self.assertIn("stale-habit-config", self._checks())


class DocumentationAuditTests(unittest.TestCase):
    """§15.19, §15.20 — empty directories and malformed decisions fail."""

    def setUp(self):
        self.fixture = Fixture()
        self.addCleanup(self.fixture.close)
        for name in ("README.md", "AGENTS.md"):
            (self.fixture.repo / name).write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(self.fixture.universe, "example")

    def _checks(self):
        return {
            p.check
            for p in audit.audit_repository(
                self.fixture.universe, "example", path=self.fixture.repo
            )
        }

    def test_an_empty_documentation_directory_fails(self):
        (self.fixture.repo / "docs" / "current").mkdir(parents=True)
        self.assertIn("empty-docs-directory", self._checks())

    def test_an_unimplemented_repository_is_not_asked_for_docs(self):
        """Requiring docs/current/ of a product that does not exist would force
        exactly the empty stub the documentation standard forbids."""
        universe = cat.load(ROOT)
        problems = audit.audit_repository(universe, "ai-portal")
        self.assertNotIn("missing-docs", [p.check for p in problems])

    def test_a_populated_documentation_directory_passes(self):
        target = self.fixture.repo / "docs" / "current"
        target.mkdir(parents=True)
        (target / "service.md").write_text("# service\n", encoding="utf-8")
        self.assertNotIn("empty-docs-directory", self._checks())

    def test_a_markdown_file_directly_under_docs_is_reported_not_failed(self):
        """A repository may keep a document where its own usage needs it."""
        docs = self.fixture.repo / "docs"
        docs.mkdir()
        (docs / "platform.md").write_text("# platform\n", encoding="utf-8")
        problems = audit.audit_repository(
            self.fixture.universe, "example", path=self.fixture.repo
        )
        found = [p for p in problems if p.check == "uncategorised-docs"]
        self.assertEqual(1, len(found))
        self.assertTrue(found[0].advisory, "a preference must not fail conformance")

    def test_an_empty_directory_still_fails(self):
        """Softening a preference must not soften a rule."""
        (self.fixture.repo / "docs" / "current").mkdir(parents=True)
        problems = audit.audit_repository(
            self.fixture.universe, "example", path=self.fixture.repo
        )
        found = [p for p in problems if p.check == "empty-docs-directory"]
        self.assertEqual(1, len(found))
        self.assertFalse(found[0].advisory)

    def test_the_same_file_inside_a_category_passes(self):
        target = self.fixture.repo / "docs" / "current"
        target.mkdir(parents=True)
        (target / "platform.md").write_text("# platform\n", encoding="utf-8")
        self.assertNotIn("uncategorised-docs", self._checks())

    def test_an_empty_evidence_directory_fails_like_any_other(self):
        (self.fixture.repo / "docs" / "evidence").mkdir(parents=True)
        self.assertIn("empty-docs-directory", self._checks())

    def test_a_decision_without_the_template_header_fails(self):
        target = self.fixture.repo / "docs" / "decisions"
        target.mkdir(parents=True)
        (target / "001-x.md").write_text(
            "# How the service works today\n\nIt does this.\n", encoding="utf-8"
        )
        self.assertIn("bad-decision-record", self._checks())

    def test_a_well_formed_decision_passes(self):
        target = self.fixture.repo / "docs" / "decisions"
        target.mkdir(parents=True)
        (target / "001-x.md").write_text(
            "# 001. Do the thing\n\n"
            "- **Date:** 2026-08-21\n"
            "- **Status:** accepted\n\n## Decision\n\nDid it.\n",
            encoding="utf-8",
        )
        self.assertNotIn("bad-decision-record", self._checks())

    def test_the_real_decision_records_are_well_formed(self):
        for record in sorted((ROOT / "decisions").glob("*.md")):
            with self.subTest(record=record.name):
                self.assertTrue(
                    audit._has_decision_header(record.read_text(encoding="utf-8"))
                )

    def test_a_missing_required_file_names_the_fix(self):
        (self.fixture.repo / "README.md").unlink()
        problems = audit.audit_repository(
            self.fixture.universe, "example", path=self.fixture.repo
        )
        missing = [p for p in problems if p.check == "missing-file"]
        self.assertTrue(missing)
        self.assertIn("sync-baseline", missing[0].fix)


class BudgetAuditTests(unittest.TestCase):
    """§15.18 — the ceiling fails; the target is reported and passes."""

    def setUp(self):
        self.fixture = Fixture()
        self.addCleanup(self.fixture.close)
        (self.fixture.repo / "README.md").write_text("# example\n", encoding="utf-8")

    def _checks(self, local_lines: int):
        (self.fixture.repo / "AGENTS.md").write_text(
            "# example\n\n" + "local rule\n" * local_lines, encoding="utf-8"
        )
        render.sync_baseline(self.fixture.universe, "example")
        return {
            p.check
            for p in audit.audit_repository(
                self.fixture.universe, "example", path=self.fixture.repo
            )
        }

    def test_over_the_ceiling_fails(self):
        found = self._checks(audit.AGENTS_HARD_CEILING + 20)
        self.assertIn("agents-md-too-long", found)

    def test_over_the_target_is_reported_but_not_a_failure(self):
        found = self._checks(audit.AGENTS_SOFT_TARGET + 10)
        self.assertIn("agents-md-over-target", found)
        self.assertNotIn("agents-md-too-long", found)

    def test_within_the_target_is_clean(self):
        found = self._checks(10)
        self.assertNotIn("agents-md-over-target", found)
        self.assertNotIn("agents-md-too-long", found)


class LanguageGateTests(unittest.TestCase):
    """§15.13 — a declared language needs a gate, and a gate needs a language."""

    def setUp(self):
        self.fixture = Fixture(languages=("shell",))
        self.addCleanup(self.fixture.close)
        (self.fixture.repo / "README.md").write_text("# example\n", encoding="utf-8")
        (self.fixture.repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(self.fixture.universe, "example")
        self.workflows = self.fixture.repo / ".github" / "workflows"
        self.workflows.mkdir(parents=True)

    def _write_workflow(self, body: str):
        (self.workflows / "validate.yml").write_text(body, encoding="utf-8")

    def _checks(self):
        return {
            p.check
            for p in audit.audit_repository(
                self.fixture.universe, "example", path=self.fixture.repo
            )
        }

    def test_a_declared_language_with_no_gate_fails(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n      - run: true\n"
        )
        self.assertIn("missing-gate", self._checks())

    def test_a_declared_language_with_its_gate_passes(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n      - run: shellcheck scripts/*\n"
        )
        self.assertNotIn("missing-gate", self._checks())

    def test_a_gate_for_an_undeclared_language_fails(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n"
            "      - run: shellcheck scripts/*\n      - run: ruff check .\n"
        )
        self.assertIn("undeclared-gate", self._checks())

    def test_a_gate_inside_a_validation_script_counts(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n"
            "      - run: bash scripts/validate\n"
        )
        scripts = self.fixture.repo / "scripts"
        scripts.mkdir()
        (scripts / "validate").write_text(
            "#!/usr/bin/env bash\nshellcheck ./*.sh\n", encoding="utf-8"
        )
        self.assertNotIn("missing-gate", self._checks())

    def test_a_suppression_directive_is_not_a_gate(self):
        """orange passed with shellcheck running nowhere: its validate script
        contained `# shellcheck disable=SC1091`, and the detector matched the
        bare word. A false pass is worse than a false failure — nobody goes
        looking for it."""
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n"
            "      - run: bash scripts/validate\n"
        )
        scripts = self.fixture.repo / "scripts"
        scripts.mkdir()
        (scripts / "validate").write_text(
            "#!/usr/bin/env bash\n# shellcheck disable=SC1091\nsource ./lib.sh\n",
            encoding="utf-8",
        )
        self.assertIn("missing-gate", self._checks())

    def test_a_step_named_after_a_tool_is_not_a_gate(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n"
            "      - name: Shellcheck\n        run: true\n"
        )
        self.assertIn("missing-gate", self._checks())

    def test_a_real_invocation_still_counts(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n"
            "      - run: shellcheck scripts/*.sh\n"
        )
        self.assertNotIn("missing-gate", self._checks())

    def test_an_invocation_behind_sudo_or_a_pipe_still_counts(self):
        for command in ("sudo shellcheck x.sh", "git ls-files | xargs shellcheck"):
            with self.subTest(command=command):
                self._write_workflow(
                    f"name: Validate\njobs:\n  x:\n    steps:\n      - run: {command}\n"
                )
                self.assertNotIn("missing-gate", self._checks())

    def test_a_gate_reached_through_npm_run_counts(self):
        """plepic runs eslint as `npm run lint`; the literal token is absent."""
        fixture = Fixture(languages=("typescript",), npm_project=True)
        self.addCleanup(fixture.close)
        (fixture.repo / "README.md").write_text("# example\n", encoding="utf-8")
        (fixture.repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(fixture.universe, "example", path=fixture.repo)
        workflows = fixture.repo / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "validate.yml").write_text(
            "name: Validate\njobs:\n  x:\n    steps:\n"
            "      - run: bash scripts/validate\n",
            encoding="utf-8",
        )
        scripts = fixture.repo / "scripts"
        scripts.mkdir()
        (scripts / "validate").write_text(
            "#!/usr/bin/env bash\nnpm run lint\n", encoding="utf-8"
        )
        (fixture.repo / "package.json").write_text(
            json.dumps({"name": "example", "scripts": {"lint": "eslint ."}}),
            encoding="utf-8",
        )
        checks = {
            p.check
            for p in audit.audit_repository(
                fixture.universe, "example", path=fixture.repo
            )
        }
        self.assertNotIn("missing-gate", checks)

    def test_a_declared_but_unrun_npm_script_is_not_a_gate(self):
        """A linter nothing invokes gates nothing."""
        fixture = Fixture(languages=("typescript",), npm_project=True)
        self.addCleanup(fixture.close)
        (fixture.repo / "README.md").write_text("# example\n", encoding="utf-8")
        (fixture.repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(fixture.universe, "example", path=fixture.repo)
        workflows = fixture.repo / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "validate.yml").write_text(
            "name: Validate\njobs:\n  x:\n    steps:\n      - run: npm test\n",
            encoding="utf-8",
        )
        (fixture.repo / "package.json").write_text(
            json.dumps({"name": "example", "scripts": {"lint": "eslint ."}}),
            encoding="utf-8",
        )
        checks = {
            p.check
            for p in audit.audit_repository(
                fixture.universe, "example", path=fixture.repo
            )
        }
        self.assertIn("missing-gate", checks)

    def test_a_repository_without_renovate_config_is_reported(self):
        """portfolio-bot shipped without one and nothing noticed until Renovate
        opened an onboarding pull request saying so."""
        self.assertIn("no-dependency-automation", self._checks())

    def test_a_renovate_config_not_extending_the_preset_is_reported(self):
        (self.fixture.repo / "renovate.json").write_text(
            '{"extends": ["config:recommended"]}\n', encoding="utf-8"
        )
        self.assertIn("unshared-dependency-config", self._checks())

    def test_extending_the_shared_preset_is_clean(self):
        (self.fixture.repo / "renovate.json").write_text(
            '{"extends": ["local>hannosirkel/architecture//templates/default"]}\n',
            encoding="utf-8",
        )
        checks = self._checks()
        self.assertNotIn("no-dependency-automation", checks)
        self.assertNotIn("unshared-dependency-config", checks)

    def test_a_repository_with_no_ci_has_no_secret_scan(self):
        self.assertIn("no-secret-scan", self._checks())

    def test_ci_without_gitleaks_is_reported(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n      - run: shellcheck scripts/*\n"
        )
        self.assertIn("no-secret-scan", self._checks())

    def test_ci_with_gitleaks_is_clean(self):
        self._write_workflow(
            "name: Validate\njobs:\n  x:\n    steps:\n"
            "      - run: shellcheck scripts/*\n"
            "      - run: ./gitleaks git --redact --verbose\n"
        )
        self.assertNotIn("no-secret-scan", self._checks())

    def test_a_languageless_repository_is_still_checked(self):
        """The gap this check exists to close.

        Language gates fire only for a declared language, so a repository
        declaring none had no secret scanning and no finding saying so.
        portfolio-bot was exactly that, and nothing noticed.
        """
        fixture = Fixture(languages=(), profile="research-private")
        self.addCleanup(fixture.close)
        (fixture.repo / "README.md").write_text("# example\n", encoding="utf-8")
        (fixture.repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(fixture.universe, "example", path=fixture.repo)
        checks = {
            p.check
            for p in audit.audit_repository(
                fixture.universe, "example", path=fixture.repo
            )
        }
        self.assertIn("no-secret-scan", checks)
        self.assertNotIn("no-ci", checks, "no-ci needs a declared language")

    def test_no_ci_at_all_is_reported_distinctly(self):
        self.assertIn("no-ci", self._checks())


class ExceptionTests(unittest.TestCase):
    """A deliberate recorded choice is not a defect.

    Built on a fixture rather than a real repository: a test that depends on
    a checkout existing passes here and fails on a runner, which is how the
    first draft of these tests behaved.
    """

    GRANTED = (
        "      missing-gate:\n"
        '        matches: "declares `typescript`"\n'
        "        reason: no npm project; see the decision\n"
        "        decision: docs/decisions/0005-no-npm-project.md\n"
    )

    def _fixture(self, exceptions=None, languages=("typescript", "shell")):
        fixture = Fixture(languages=languages, exceptions=exceptions)
        self.addCleanup(fixture.close)
        (fixture.repo / "README.md").write_text("# example\n", encoding="utf-8")
        (fixture.repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(fixture.universe, "example", path=fixture.repo)
        workflows = fixture.repo / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "validate.yml").write_text(
            "name: Validate\njobs:\n  x:\n    steps:\n      - run: true\n",
            encoding="utf-8",
        )
        return fixture

    def _audit(self, fixture):
        return audit.audit_repository(fixture.universe, "example", path=fixture.repo)

    def test_the_excepted_finding_is_advisory_and_still_printed(self):
        fixture = self._fixture(self.GRANTED)
        found = [
            p
            for p in self._audit(fixture)
            if p.check == "missing-gate" and "typescript" in p.detail
        ]
        self.assertEqual(1, len(found))
        self.assertTrue(found[0].advisory)
        self.assertIn("excepted:", found[0].detail)
        self.assertIn("decisions/", found[0].fix)

    def test_an_exception_does_not_silence_a_neighbouring_finding(self):
        """One check fires for several reasons; an exception covers one."""
        fixture = self._fixture(self.GRANTED)
        others = [
            p
            for p in self._audit(fixture)
            if p.check == "missing-gate" and "typescript" not in p.detail
        ]
        self.assertTrue(others, "the shell gate should still be reported")
        for problem in others:
            self.assertFalse(problem.advisory, f"{problem.detail} must still fail")

    def test_without_matches_the_exception_would_silence_both(self):
        """The first draft did exactly this. Keep the evidence in the suite."""
        unscoped = "      missing-gate:\n        reason: r\n        decision: d\n"
        fixture = self._fixture(unscoped)
        gates = [p for p in self._audit(fixture) if p.check == "missing-gate"]
        self.assertEqual(2, len(gates))
        self.assertTrue(all(p.advisory for p in gates))
        checks = [p.check for p in cat.validate(fixture.universe)]
        self.assertIn("unscoped-exception", checks, "validate must refuse it")

    def test_an_exception_that_matches_nothing_is_stale(self):
        never = (
            "      direct-push:\n"
            '        matches: "never appears"\n'
            "        reason: r\n"
            "        decision: d\n"
        )
        fixture = self._fixture(never)
        self.assertIn("stale-exception", [p.check for p in self._audit(fixture)])

    def test_validate_refuses_an_exception_without_a_reason(self):
        fixture = self._fixture(
            '      missing-gate:\n        matches: "x"\n        decision: d\n'
        )
        checks = [p.check for p in cat.validate(fixture.universe)]
        self.assertIn("malformed-exception", checks)

    def test_validate_refuses_an_exception_without_a_decision(self):
        fixture = self._fixture(
            '      missing-gate:\n        matches: "x"\n        reason: r\n'
        )
        checks = [p.check for p in cat.validate(fixture.universe)]
        self.assertIn("malformed-exception", checks)

    def test_the_real_catalogue_exceptions_are_well_formed(self):
        universe = cat.load(ROOT)
        self.assertEqual([], [str(p) for p in cat.validate(universe)])
        granted = {
            name: cat.exceptions_for(universe, name)
            for name in universe.repositories
            if cat.exceptions_for(universe, name)
        }
        self.assertEqual({"mihkel", "servitium"}, set(granted))


class BranchNotWorkingTreeTests(unittest.TestCase):
    """The audit describes the branch, not whatever is checked out.

    A working tree lags its branch, badly right after a merge, and the audit
    skill fetches without pulling by design. Reading the checkout answers a
    question nobody asked.
    """

    def setUp(self):
        self.fixture = Fixture()
        self.addCleanup(self.fixture.close)
        repo = self.fixture.repo
        _git("init", "--initial-branch=main", cwd=repo)
        _git("config", "user.email", "t@example.invalid", cwd=repo)
        _git("config", "user.name", "t", cwd=repo)
        (repo / "README.md").write_text("# example\n", encoding="utf-8")
        (repo / "AGENTS.md").write_text(LOCAL_CONTENT, encoding="utf-8")
        render.sync_baseline(self.fixture.universe, "example")
        _git("add", "-A", cwd=repo)
        _git("commit", "-m", "initial commit", cwd=repo)

    def test_an_uncommitted_working_tree_change_is_not_reported(self):
        """Committed state is clean, so a dirty checkout must not fail the audit."""
        (self.fixture.repo / "AGENTS.md").write_text("# broken\n", encoding="utf-8")
        checks = {
            p.check for p in audit.audit_repository(self.fixture.universe, "example")
        }
        self.assertNotIn("bad-markers", checks)

    def test_the_same_change_is_reported_when_the_worktree_is_audited_directly(self):
        (self.fixture.repo / "AGENTS.md").write_text("# broken\n", encoding="utf-8")
        checks = {
            p.check
            for p in audit.audit_repository(
                self.fixture.universe, "example", path=self.fixture.repo
            )
        }
        self.assertIn("bad-markers", checks)

    def test_an_unreadable_branch_is_a_finding_not_a_pass(self):
        broken = Fixture()
        self.addCleanup(broken.close)
        problems = audit.audit_repository(broken.universe, "example")
        self.assertEqual(["cannot-read-branch"], [p.check for p in problems])


class DirectPushTests(unittest.TestCase):
    """§7.5 — the rule is the enforcement where a ruleset is unavailable."""

    def setUp(self):
        self.fixture = Fixture()
        self.addCleanup(self.fixture.close)
        self._init_git(self.fixture.repo)

    @staticmethod
    def _init_git(repo):
        _git("init", "--initial-branch=main", cwd=repo)
        _git("config", "user.email", "t@example.invalid", cwd=repo)
        _git("config", "user.name", "t", cwd=repo)
        (repo / "README.md").write_text("# example\n", encoding="utf-8")
        _git("add", "-A", cwd=repo)
        _git("commit", "-m", "initial commit", cwd=repo)

    def _entry(self):
        return self.fixture.universe.repositories["example"]

    def test_a_root_commit_is_whitelisted(self):
        problems = audit._audit_default_branch_commits(
            "example", self._entry(), self.fixture.repo
        )
        self.assertEqual([], problems)

    def test_a_direct_push_is_reported(self):
        (self.fixture.repo / "src.sh").write_text("echo hi\n", encoding="utf-8")
        _git("add", "-A", cwd=self.fixture.repo)
        _git("commit", "-m", "feat: straight to main", cwd=self.fixture.repo)
        problems = audit._audit_default_branch_commits(
            "example", self._entry(), self.fixture.repo
        )
        self.assertEqual(1, len(problems))
        self.assertEqual("direct-push", problems[0].check)

    def _commit_initiative_state(self):
        target = self.fixture.repo / "initiatives" / "active" / "x"
        target.mkdir(parents=True, exist_ok=True)
        (target / "state.yaml").write_text("status: IMPLEMENTING\n", encoding="utf-8")
        _git("add", "-A", cwd=self.fixture.repo)
        _git("commit", "-m", "state: record progress", cwd=self.fixture.repo)

    def test_initiative_state_is_exempt_only_where_the_catalogue_says_so(self):
        """The exception is architecture's, not every repository's."""
        self._commit_initiative_state()
        problems = audit._audit_default_branch_commits(
            "example", self._entry(), self.fixture.repo
        )
        self.assertEqual(["direct-push"], [p.check for p in problems])

    def test_initiative_state_is_exempt_where_the_catalogue_grants_it(self):
        fixture = Fixture(direct_push='      allowed_paths: ["initiatives/"]\n')
        self.addCleanup(fixture.close)
        self._init_git(fixture.repo)
        target = fixture.repo / "initiatives" / "active" / "x"
        target.mkdir(parents=True)
        (target / "state.yaml").write_text("status: IMPLEMENTING\n", encoding="utf-8")
        _git("add", "-A", cwd=fixture.repo)
        _git("commit", "-m", "state: record progress", cwd=fixture.repo)
        problems = audit._audit_default_branch_commits(
            "example", fixture.universe.repositories["example"], fixture.repo
        )
        self.assertEqual([], problems)

    def test_a_mixed_commit_is_not_exempt(self):
        """An exempt prefix must not launder an unrelated change alongside it."""
        fixture = Fixture(direct_push='      allowed_paths: ["initiatives/"]\n')
        self.addCleanup(fixture.close)
        self._init_git(fixture.repo)
        target = fixture.repo / "initiatives" / "active" / "x"
        target.mkdir(parents=True)
        (target / "state.yaml").write_text("status: IMPLEMENTING\n", encoding="utf-8")
        (fixture.repo / "src.sh").write_text("echo hi\n", encoding="utf-8")
        _git("add", "-A", cwd=fixture.repo)
        _git("commit", "-m", "state: record progress", cwd=fixture.repo)
        problems = audit._audit_default_branch_commits(
            "example", fixture.universe.repositories["example"], fixture.repo
        )
        self.assertEqual(["direct-push"], [p.check for p in problems])

    def test_an_automated_push_is_exempt_by_subject_pattern(self):
        """deploys receives digest pushes that a pull-request rule would break."""
        fixture = Fixture(
            direct_push="      allowed_subject_pattern: '^deploy\\(live\\): '\n"
        )
        self.addCleanup(fixture.close)
        self._init_git(fixture.repo)
        (fixture.repo / "digest.yaml").write_text("sha256: abc\n", encoding="utf-8")
        _git("add", "-A", cwd=fixture.repo)
        _git("commit", "-m", "deploy(live): PR #35 sha256:abc", cwd=fixture.repo)
        problems = audit._audit_default_branch_commits(
            "example", fixture.universe.repositories["example"], fixture.repo
        )
        self.assertEqual([], problems)

    def test_a_squash_merged_pull_request_is_not_a_direct_push(self):
        """A squash merge is single-parent; only its subject distinguishes it."""
        (self.fixture.repo / "src.sh").write_text("echo hi\n", encoding="utf-8")
        _git("add", "-A", cwd=self.fixture.repo)
        _git(
            "commit", "-m", "feat: add interactive dice hall (#2)", cwd=self.fixture.repo
        )
        problems = audit._audit_default_branch_commits(
            "example", self._entry(), self.fixture.repo
        )
        self.assertEqual([], problems)

    def test_history_before_the_baseline_is_not_reported(self):
        """New-work-first applies to history exactly as it does to a linter."""
        repo = self.fixture.repo
        (repo / "old.sh").write_text("echo old\n", encoding="utf-8")
        _git("add", "-A", cwd=repo)
        _git("commit", "-m", "feat: an old direct push", cwd=repo)
        baseline = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        fixture = Fixture(direct_push=f'      baseline_commit: "{baseline}"\n')
        self.addCleanup(fixture.close)
        entry = dict(fixture.universe.repositories["example"])
        entry["local_path"] = str(repo)

        self.assertEqual([], audit._audit_default_branch_commits("example", entry, repo))

        (repo / "new.sh").write_text("echo new\n", encoding="utf-8")
        _git("add", "-A", cwd=repo)
        _git("commit", "-m", "feat: a new direct push", cwd=repo)
        problems = audit._audit_default_branch_commits("example", entry, repo)
        self.assertEqual(["direct-push"], [p.check for p in problems])
        self.assertIn("baselined", problems[0].detail)

    def test_the_fix_names_the_ruleset_where_one_is_possible(self):
        (self.fixture.repo / "src.sh").write_text("echo hi\n", encoding="utf-8")
        _git("add", "-A", cwd=self.fixture.repo)
        _git("commit", "-m", "feat: straight to main", cwd=self.fixture.repo)
        problems = audit._audit_default_branch_commits(
            "example", self._entry(), self.fixture.repo
        )
        self.assertIn("ruleset", problems[0].fix)

    def test_the_fix_names_the_rule_where_a_ruleset_is_impossible(self):
        fixture = Fixture(supports_rulesets=False)
        self.addCleanup(fixture.close)
        self._init_git(fixture.repo)
        (fixture.repo / "src.sh").write_text("echo hi\n", encoding="utf-8")
        _git("add", "-A", cwd=fixture.repo)
        _git("commit", "-m", "feat: straight to main", cwd=fixture.repo)
        problems = audit._audit_default_branch_commits(
            "example", fixture.universe.repositories["example"], fixture.repo
        )
        self.assertIn("cannot carry a ruleset", problems[0].fix)

    def test_a_merged_pull_request_is_not_a_direct_push(self):
        repo = self.fixture.repo
        _git("checkout", "-q", "-b", "feature", cwd=repo)
        (repo / "src.sh").write_text("echo hi\n", encoding="utf-8")
        _git("add", "-A", cwd=repo)
        _git("commit", "-m", "feat: on a branch", cwd=repo)
        _git("checkout", "-q", "main", cwd=repo)
        _git("merge", "--no-ff", "-m", "Merge pull request #1", "feature", cwd=repo)
        problems = audit._audit_default_branch_commits("example", self._entry(), repo)
        self.assertEqual([], problems)


if __name__ == "__main__":
    unittest.main()
