import tempfile
import unittest
from pathlib import Path

from tools.extract_action_items import ActionItem, collect_actions, render_report
from tools.validate_markdown import check_markdown_text, discover_markdown_files


class ExtractActionItemsTests(unittest.TestCase):
    def test_extracts_open_tasks_and_open_requirements_by_source_line(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "backlog.md").write_text(
                "# Backlog\n\n- [ ] Ship feature\n- [x] Completed task\n",
                encoding="utf-8",
            )
            (root / "requirements.md").write_text(
                "# Requirements\n\n"
                "## Open Requirements and Dependencies\n\n"
                "- Confirm API version\n",
                encoding="utf-8",
            )

            actions, requirements, errors = collect_actions(
                root, ("backlog.md", "requirements.md")
            )

        self.assertEqual(errors, [])
        self.assertEqual([item.text for item in actions], ["Ship feature"])
        self.assertEqual(actions[0].sources, ["backlog.md:3"])
        self.assertEqual(len(requirements), 1)
        self.assertEqual(requirements[0].text, "Confirm API version")
        self.assertEqual(requirements[0].backlog_items, [])

    def test_deduplicates_identical_items_and_keeps_all_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "first.md").write_text("- [ ] Confirm API version\n", encoding="utf-8")
            (root / "second.md").write_text("- [ ] Confirm API version\n", encoding="utf-8")

            actions, requirements, errors = collect_actions(
                root, ("first.md", "second.md")
            )

        self.assertEqual(errors, [])
        self.assertEqual(requirements, [])
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].sources, ["first.md:1", "second.md:1"])

    def test_links_open_requirements_to_matching_backlog_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "backlog.md").write_text(
                "- [ ] Confirm the Jira Server URL and supported API version\n",
                encoding="utf-8",
            )
            (root / "requirements.md").write_text(
                "## Open Requirements and Dependencies\n\n- Actual Jira Server URL\n",
                encoding="utf-8",
            )

            actions, requirements, errors = collect_actions(
                root, ("backlog.md", "requirements.md")
            )

        self.assertEqual(errors, [])
        self.assertEqual(len(actions), 1)
        self.assertEqual(len(requirements), 1)
        self.assertEqual(requirements[0].backlog_items, [1])

    def test_reports_missing_sources_instead_of_silently_dropping_them(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            actions, requirements, errors = collect_actions(
                Path(temporary_directory), ("missing.md",)
            )

        self.assertEqual(actions, [])
        self.assertEqual(requirements, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("missing.md", errors[0])

    def test_report_escapes_table_delimiters(self) -> None:
        report = render_report(
            [ActionItem("Check A | B", "Unchecked backlog task", sources=["sample.md:1"])],
            [],
            [],
        )

        self.assertIn("Check A \\| B", report)


class ValidateMarkdownTests(unittest.TestCase):
    def test_accepts_valid_markdown(self) -> None:
        text = "# Title\n\n## Details\n\nText.\n\n```text\ncontent\n```\n"

        self.assertEqual(check_markdown_text(text), [])

    def test_ignores_heading_syntax_inside_fenced_code(self) -> None:
        text = "# Title\n\n```markdown\n### Example\n```\n"

        self.assertEqual(check_markdown_text(text), [])

    def test_reports_whitespace_heading_hierarchy_and_unbalanced_fence(self) -> None:
        text = "# Title  \n### Skipped\n```python\nprint('x')\n"
        findings = check_markdown_text(text)
        rules = {rule for _, rule, _ in findings}

        self.assertIn("trailing-whitespace", rules)
        self.assertIn("heading-hierarchy", rules)
        self.assertIn("unbalanced-fence", rules)

    def test_reports_missing_final_newline_and_heading_spacing(self) -> None:
        text = "Paragraph\n# Heading\nText"
        findings = check_markdown_text(text)
        rules = {rule for _, rule, _ in findings}

        self.assertIn("final-newline", rules)
        self.assertIn("heading-spacing", rules)

    def test_discovery_skips_dependency_and_build_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "README.md").write_text("# Root\n", encoding="utf-8")
            (root / ".venv").mkdir()
            (root / ".venv" / "ignored.md").write_text("# Ignore\n", encoding="utf-8")
            (root / "build").mkdir()
            (root / "build" / "ignored.md").write_text("# Ignore\n", encoding="utf-8")

            files = discover_markdown_files(root)

        self.assertEqual([path.name for path in files], ["README.md"])


if __name__ == "__main__":
    unittest.main()
