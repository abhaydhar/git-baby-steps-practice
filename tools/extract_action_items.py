import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_SOURCES = (
    "BACKLOG.md",
    "project_spec.md",
    "work/jira-dashboard-requirements.md",
)
UNCHECKED_TASK = re.compile(r"^\s*[-*+]\s+\[\s\]\s+(.*\S)\s*$")
CHECKED_TASK = re.compile(r"^\s*[-*+]\s+\[[xX]\]\s+")
BULLET = re.compile(r"^\s*[-*+]\s+(.*\S)\s*$")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
OWNER = re.compile(r"\b(?:owner|assignee)\s*:\s*([^;|]+)", re.IGNORECASE)
DUE = re.compile(r"\b(?:due(?: date)?|deadline)\s*:\s*([^;|]+)", re.IGNORECASE)


@dataclass
class ActionItem:
    text: str
    category: str
    owner: str = "Not stated"
    due_date: str = "Not stated"
    sources: list[str] = field(default_factory=list)


@dataclass
class OpenRequirement:
    text: str
    sources: list[str] = field(default_factory=list)
    backlog_items: list[int] = field(default_factory=list)


REQUIREMENT_TARGETS = {
    "actual jira server url": ("confirm the jira server url",),
    "jira server version and supported api version": (
        "confirm the jira server url",
        "record the jira server version",
    ),
    "jira project and sprint field names": (
        "confirm the jira project key project identifier and sprint fields",
    ),
    "issue type status assignee due date priority and story point mappings": (
        "confirm the field mappings for status assignee due date priority issue type",
    ),
    "whether story points are required for progress reporting": (
        "confirm the field mappings for status assignee due date priority issue type",
        "add optional story point calculations",
    ),
    "authorized jira integration identity and authentication method": (
        "define the authorized jira integration identity and authentication method",
    ),
    "exact external stakeholder distribution and access policy": (
        "define internal and external stakeholder groups",
        "obtain approval for external stakeholder access",
    ),
    "team lead responsible for dashboard maintenance": (
        "identify the team lead responsible for dashboard maintenance",
    ),
    "deployment target and hosting environment for the separate web application": (
        "confirm the approved hosting environment and deployment target",
    ),
    "whether the dashboard should expose only summary data to external stakeholders or full jira issue data": (
        "confirm whether the dashboard must retrieve only summary data or full issue details",
    ),
}


def normalize_item(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*`_~]", "", text)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def metadata(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return match.group(1).strip() if match else "Not stated"


def extract_file(path: Path, source_label: str) -> tuple[list[ActionItem], str | None]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return [], f"{source_label}: {error}"

    extracted: list[ActionItem] = []
    in_open_requirements = False

    for line_number, line in enumerate(lines, start=1):
        heading = HEADING.match(line)
        if heading:
            title = heading.group(1).lower()
            in_open_requirements = "open requirements" in title
            continue

        task = UNCHECKED_TASK.match(line)
        if task:
            item_text = task.group(1).strip()
            extracted.append(
                ActionItem(
                    text=item_text,
                    category="Unchecked backlog task",
                    owner=metadata(OWNER, item_text),
                    due_date=metadata(DUE, item_text),
                    sources=[f"{source_label}:{line_number}"],
                )
            )
            continue

        if in_open_requirements and not CHECKED_TASK.match(line):
            bullet = BULLET.match(line)
            if bullet:
                item_text = bullet.group(1).strip()
                extracted.append(
                    ActionItem(
                        text=item_text,
                        category="Open requirement",
                        owner=metadata(OWNER, item_text),
                        due_date=metadata(DUE, item_text),
                        sources=[f"{source_label}:{line_number}"],
                    )
                )

    return extracted, None


def collect_actions(
    root: Path, sources: tuple[str, ...] = DEFAULT_SOURCES
) -> tuple[list[ActionItem], list[OpenRequirement], list[str]]:
    actions: list[ActionItem] = []
    by_normalized_text: dict[str, ActionItem] = {}
    requirements: list[OpenRequirement] = []
    by_normalized_requirement: dict[str, OpenRequirement] = {}
    errors: list[str] = []

    for source in sources:
        source_path = root / source
        items, error = extract_file(source_path, source)
        if error:
            errors.append(error)
            continue

        for item in items:
            key = normalize_item(item.text)
            if item.category == "Open requirement":
                existing_requirement = by_normalized_requirement.get(key)
                if existing_requirement is None:
                    requirement = OpenRequirement(item.text, list(item.sources))
                    by_normalized_requirement[key] = requirement
                    requirements.append(requirement)
                else:
                    existing_requirement.sources.extend(item.sources)
                continue

            existing = by_normalized_text.get(key)
            if existing is None:
                by_normalized_text[key] = item
                actions.append(item)
                continue
            existing.sources.extend(item.sources)
            if existing.owner == "Not stated":
                existing.owner = item.owner
            if existing.due_date == "Not stated":
                existing.due_date = item.due_date

    for requirement in requirements:
        targets = REQUIREMENT_TARGETS.get(normalize_item(requirement.text), ())
        for index, action in enumerate(actions, start=1):
            normalized_action = normalize_item(action.text)
            if any(target in normalized_action for target in targets):
                requirement.backlog_items.append(index)

    return actions, requirements, errors


def escape_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\r", " ").replace("\n", " ")


def render_report(
    actions: list[ActionItem],
    requirements: list[OpenRequirement],
    errors: list[str],
) -> str:
    lines = [
        "# Action Items",
        "",
        f"- Unchecked backlog tasks: {len(actions)}",
        f"- Open requirements: {len(requirements)}",
        f"- Source files with errors: {len(errors)}",
        "- Task references below refer to row numbers in this report, not GitHub issue numbers.",
        "",
        "| # | Type | Action item | Owner | Due date | Source |",
        "|---:|---|---|---|---|---|",
    ]

    for index, item in enumerate(actions, start=1):
        values = (
            str(index),
            item.category,
            item.text,
            item.owner,
            item.due_date,
            ", ".join(item.sources),
        )
        lines.append("| " + " | ".join(escape_cell(value) for value in values) + " |")

    if not actions:
        lines.append("| — | — | No explicit open action items found. | — | — | — |")

    lines.extend(
        [
            "",
            "## Open Requirements",
            "",
            "| Requirement | Source | Related backlog task(s) |",
            "|---|---|---|",
        ]
    )
    if requirements:
        for requirement in requirements:
            related_items = (
                ", ".join(f"#{number}" for number in requirement.backlog_items)
                if requirement.backlog_items
                else "No matching backlog task found"
            )
            related_items = related_items.replace("#", "Task ")
            values = (
                requirement.text,
                ", ".join(requirement.sources),
                related_items,
            )
            lines.append("| " + " | ".join(escape_cell(value) for value in values) + " |")
    else:
        lines.append("| No explicit open requirements found. | — | — |")

    if errors:
        lines.extend(["", "## Input Errors", ""])
        lines.extend(f"- {escape_cell(error)}" for error in errors)

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract explicit open actions from the project's Markdown sources."
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
        help="Output report path (defaults to reports/action-items.md under --root).",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve() if args.output else root / "reports" / "action-items.md"

    source_paths = {(root / source).resolve() for source in DEFAULT_SOURCES}
    if output in source_paths:
        parser.error("output path must not overwrite an input source")

    actions, requirements, errors = collect_actions(root)
    report = render_report(actions, requirements, errors)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8", newline="\n")
    except OSError as error:
        print(f"Could not write {output}: {error}", file=sys.stderr)
        return 1

    print(
        f"Processed {len(DEFAULT_SOURCES)} source files; "
        f"found {len(actions)} unchecked tasks and {len(requirements)} open requirements."
    )
    print(f"Report: {output}")
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
