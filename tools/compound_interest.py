import argparse
import math


def non_negative_float(value: str) -> float:
    try:
        number = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a number") from error

    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be a finite, non-negative number")
    return number


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error

    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    compounds_per_year: int,
    total_years: float,
) -> tuple[float, float]:
    final_amount = principal * (
        1 + annual_rate / (100 * compounds_per_year)
    ) ** (compounds_per_year * total_years)
    interest_earned = final_amount - principal
    return final_amount, interest_earned


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate compound interest using an annual rate in percent."
    )
    parser.add_argument("principal", type=non_negative_float)
    parser.add_argument("annual_rate", type=non_negative_float)
    parser.add_argument("compounds_per_year", type=positive_int)
    parser.add_argument("total_years", type=non_negative_float)
    args = parser.parse_args()

    final_amount, interest_earned = calculate_compound_interest(
        args.principal,
        args.annual_rate,
        args.compounds_per_year,
        args.total_years,
    )
    print(f"Final amount: {final_amount:.2f}")
    print(f"Interest earned: {interest_earned:.2f}")


if __name__ == "__main__":
    main()