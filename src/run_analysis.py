"""CLI entrypoint for quick CSV metric summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from basic_analysis import load_rows, print_summary, summarize_numeric_fields


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize room-temp exciton metric CSV files."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="data/samples/sample_measurements.csv",
        help="Path to a CSV file with metric columns.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        raise SystemExit(f"CSV file not found: {csv_path}")

    rows = load_rows(csv_path)
    summary = summarize_numeric_fields(rows)
    print_summary(summary)


if __name__ == "__main__":
    main()
