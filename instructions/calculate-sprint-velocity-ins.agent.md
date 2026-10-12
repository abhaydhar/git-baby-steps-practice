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