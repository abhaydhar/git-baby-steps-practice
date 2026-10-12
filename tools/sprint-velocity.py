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