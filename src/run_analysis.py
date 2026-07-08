"""CLI entrypoint for teleportation-aligned cycle analysis."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from basic_analysis import compute_cycle_metrics, load_records, summarize_validation_failures
from stability import classify_cycle, STABILITY_CLASSES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze room-temp teleportation-cycle measurement CSV files."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="data/samples/sample_measurements.csv",
        help="Path to a CSV file with teleportation-cycle metric columns.",
    )
    return parser


def _print_metric_block(name: str, summary: dict[str, float] | None) -> None:
    if not summary:
        print(f"- {name}: unavailable")
        return

    print(
        f"- {name}: mean={summary['mean']:.3f}, min={summary['min']:.3f}, max={summary['max']:.3f}"
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        raise SystemExit(f"CSV file not found: {csv_path}")

    records = load_records(csv_path)
    metrics = compute_cycle_metrics(records)
    failures = summarize_validation_failures(records)
    class_counts = Counter(classify_cycle(record) for record in records)

    print(f"Teleportation-aligned analysis for: {csv_path}")
    print(f"Loaded {metrics['record_count']} cycle records.")
    print()

    print("Cycle metrics:")
    _print_metric_block("t_active_ns", metrics["t_active_ns"])
    _print_metric_block("t_cycle_ns", metrics["t_cycle_ns"])
    _print_metric_block("cm_t", metrics["cm_t"])
    print(
        "- reset_confirmed:"
        f" {metrics['reset_confirmed_count']}/{metrics['record_count']} cycles"
    )
    print(
        "- continuity_ok:"
        f" {metrics['continuity_ok_count']}/{metrics['continuity_required_count']} transfer cycles"
    )
    print()

    print("Stability classes:")
    for stability_class in STABILITY_CLASSES:
        print(f"- {stability_class}: {class_counts.get(stability_class, 0)}")
    print()

    print("Per-cycle status:")
    for record in records:
        print(
            f"- cycle {record.cycle_index}: {classify_cycle(record)}"
            f" (CM_t={record.cm_t:.3f}, T_cycle={record.t_cycle_ns:.3f} ns)"
        )

    print()
    if failures:
        print("Validation failures:")
        for cycle_index, errors in failures.items():
            print(f"- cycle {cycle_index}:")
            for error in errors:
                print(f"  - {error}")
    else:
        print("Validation failures: none")


if __name__ == "__main__":
    main()
