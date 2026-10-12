---
name: calculate-compound-interest
description: Calculate compound interest with the project CLI and present the final amount and interest earned.
---

# Calculate Compound Interest

Use the `tools/compound_interest.py` CLI when a user requests a compound-interest calculation.

## Inputs
- Collect the principal, annual rate, compounding frequency, and total duration in years.
- If any input is missing, ask the user for it instead of guessing.
- Pass the annual rate as a percentage, such as `7.34` for 7.34% (not `0.0734`).
- Principal and annual rate must be finite, non-negative numbers.
- Compounds per year must be a positive integer.
- Total years must be a finite, non-negative number; fractional years are allowed.

## Run
- Invoke from the project root with four positional arguments in this order:
  `python tools/compound_interest.py <principal> <annual_rate_percent> <compounds_per_year> <total_years>`
- Use the project's selected Python environment when invoking the script.
- If the CLI rejects an input, report the validation error and request corrected values; do not substitute values.

## Present Results
- Report both values printed by the CLI: final amount and interest earned.
- Preserve the CLI's two-decimal-place formatting and clearly label each value.
- Do not imply the result includes taxes, fees, or other adjustments not modeled by the calculation.