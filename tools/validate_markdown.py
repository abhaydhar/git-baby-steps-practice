import argparse
import os
import re
import sys
from pathlib import Path


EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "ENV",
    "build",
    "dist",
    "node_modules",
    "__pycache__",
}
MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdown"}
HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def check_markdown_text(text: str) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    if not text.endswith("\n"):
        findings.append((max(1, len(text.splitlines())), "final-newline", "Missing final newline."))

    lines = text.splitlines()
    previous_heading_level: int | None = None
    fence_marker: str | None = None
    fence_length = 0
    fence_start_line = 0

    def require_blank_neighbor(line_index: int, rule: str, message: str) -> None:
        if line_index > 0 and lines[line_index - 1].strip():
            findings.append((line_index + 1, rule, message))

    for index, line in enumerate(lines):
        line_number = index + 1
        fence_match = FENCE.match(line)
        if fence_marker is not None:
            is_closing = (
                fence_match is not None
                and fence_match.group(1)[0] == fence_marker
                and len(fence_match.group(1)) >= fence_length
                and not fence_match.group(2).strip()
            )
            if is_closing:
                if index + 1 < len(lines) and lines[index + 1].strip():
                    findings.append(
                        (line_number, "fence-spacing", "Expected a blank line after code fence.")
                    )
                fence_marker = None
                fence_length = 0
            continue

        if fence_match:
            marker = fence_match.group(1)
            fence_marker = marker[0]
            fence_length = len(marker)
            fence_start_line = line_number
            require_blank_neighbor(index, "fence-spacing", "Expected a blank line before code fence.")
            continue

        if line.rstrip(" \t") != line:
            findings.append((line_number, "trailing-whitespace", "Trailing spaces or tabs."))

        heading_match = HEADING.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            require_blank_neighbor(index, "heading-spacing", "Expected a blank line before heading.")
            if index + 1 < len(lines) and lines[index + 1].strip():
                findings.append(
                    (line_number, "heading-spacing", "Expected a blank line after heading.")
                )
            if previous_heading_level is not None and level > previous_heading_level + 1:
                findings.append(
                    (
                        line_number,
                        "heading-hierarchy",
                        f"Heading level {level} skips a level after level {previous_heading_level}.",
                    )
                )
            previous_heading_level = level

    if fence_marker is not None:
        findings.append((fence_start_line, "unbalanced-fence", "Code fence is not closed."))

    return findings


def discover_markdown_files(root: Path) -> list[Path]:
    markdown_files: list[Path] = []
    for directory, subdirectories, filenames in os.walk(root):
        subdirectories[:] = sorted(
            name for name in subdirectories if name not in EXCLUDED_DIRECTORIES
        )
        current = Path(directory)
        for filename in filenames:
            path = current / filename
            if path.suffix.lower() in MARKDOWN_SUFFIXES:
                markdown_files.append(path)
    return sorted(markdown_files, key=lambda path: path.relative_to(root).as_posix().lower())


def escape_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\r", " ").replace("\n", " ")


def validate_files(root: Path) -> tuple[list[tuple[str, int, str, str]], list[str], int]:
    findings: list[tuple[str, int, str, str]] = []
    errors: list[str] = []
    files = discover_markdown_files(root)

    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{relative}: {error}")
            continue
        findings.extend(
            (relative, line, rule, message)
            for line, rule, message in check_markdown_text(text)
        )

    return findings, errors, len(files)


def render_report(
    findings: list[tuple[str, int, str, str]], errors: list[str], file_count: int
) -> str:
    files_with_findings = len({finding[0] for finding in findings})
    lines = [
        "# Markdown Validation Report",
        "",
        f"- Files processed: {file_count}",
        f"- Files with formatting findings: {files_with_findings}",
        f"- Read errors: {len(errors)}",
        "",
        "## Checks Applied",
        "",
        "- UTF-8 decoding and final newline.",
        "- No trailing spaces or tabs.",
        "- Blank lines before and after ATX headings and fenced code blocks.",
        "- Heading levels do not skip a level.",
        "- Fenced code blocks have matching closing fences.",
        "",
        "## Findings",
        "",
    ]
    if findings:
        lines.extend(
            [
                "| File | Line | Rule | Finding |",
                "|---|---:|---|---|",
            ]
        )
        lines.extend(
            "| "
            + " | ".join(
                escape_cell(value)
                for value in (path, str(line), rule, message)
            )
            + " |"
            for path, line, rule, message in findings
        )
    else:
        lines.append("No formatting findings.")

    if errors:
        lines.extend(["", "## Read Errors", ""])
        lines.extend(f"- {escape_cell(error)}" for error in errors)

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate formatting in each Markdown file under the project root."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root directory (defaults to the repository root).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output report path (defaults to reports/markdown-validation.md under --root).",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve() if args.output else root / "reports" / "markdown-validation.md"
    if output == root or root not in output.parents:
        parser.error("output path must be inside --root and must not be the root directory")

    findings, errors, file_count = validate_files(root)
    report = render_report(findings, errors, file_count)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8", newline="\n")
    except OSError as error:
        print(f"Could not write {output}: {error}", file=sys.stderr)
        return 1

    print(f"Processed {file_count} Markdown files; found {len(findings)} formatting issues.")
    print(f"Report: {output}")
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if findings or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
