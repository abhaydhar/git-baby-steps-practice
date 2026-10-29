# Module 12 Completion Report

## Instruction File
- Filename: calculate-sprint-velocity-ins.agent.md

```text
---
name: calculate-sprint-velocity-ins
description: Use the sprint-velocity CLI to total completed story points for a project and report the result.
---

# Calculate Sprint Velocity

Use `tools/sprint-velocity.py` when a user asks to calculate sprint velocity from story-point values.

## Inputs
- Collect the project code and one or more story-point values completed in the same sprint.
- If the project code or point values are missing, ask the user; do not invent values.
- Use only completed story points for the sprint being measured.
- Values may be fractional, but must be finite and non-negative.

## Run
- From the project root, invoke the script with the project code first, followed by each story-point value:
  `python tools/sprint-velocity.py <project_code> <story_points> [<story_points> ...]`
- Use the project's selected Python environment when invoking the script.
- If the CLI rejects an input, report the validation error and ask for corrected values.

## Present Results
- Report the CLI's project code and summed sprint velocity in story points.
- Preserve the total as printed by the CLI; do not calculate an average or add unprovided values.
```

## Script File
- Filename: sprint-velocity.py
- Language: Python

```python
import argparse
from decimal import Decimal, InvalidOperation


def project_code(value: str) -> str:
    code = value.strip()
    if not code:
        raise argparse.ArgumentTypeError("must not be empty")
    return code


def story_points(value: str) -> Decimal:
    try:
        points = Decimal(value)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("must be a number") from error

    if not points.is_finite() or points < 0:
        raise argparse.ArgumentTypeError("must be a finite, non-negative number")
    return points


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate sprint velocity from completed story-point values."
    )
    parser.add_argument("project_code", type=project_code)
    parser.add_argument("story_points", type=story_points, nargs="+")
    args = parser.parse_args()

    velocity = sum(args.story_points, start=Decimal("0"))
    print(f"Project {args.project_code} sprint velocity: {velocity.normalize():f} story points")


if __name__ == "__main__":
    main()
```

## Script Execution Output
```
usage: sprint-velocity.py [-h] project_code story_points [story_points ...]

Calculate sprint velocity from completed story-point values.

positional arguments:
  project_code
  story_points

options:
  -h, --help    show this help message and exit
```