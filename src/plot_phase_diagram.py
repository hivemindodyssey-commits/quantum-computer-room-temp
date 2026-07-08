"""Generate a stability phase diagram from teleportation-cycle CSV data."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt

from basic_analysis import load_records
from metrics_schema import MeasurementRecord
from stability import classify_cycle


def stability_color_map() -> dict[str, str]:
    return {
        "teleportation_stable": "tab:green",
        "timing_marginal": "tab:orange",
        "handoff_degraded": "tab:red",
        "reset_invalid": "tab:pink",
        "non_viable": "tab:gray",
    }


def run_marker_map(run_labels: Iterable[str]) -> dict[str, str]:
    """Assign deterministic marker symbols per run label, cycling as needed."""
    markers = ["o", "s", "D", "^", "v", "P", "X", "*", "<", ">"]
    labels = sorted(set(run_labels))
    return {label: markers[index % len(markers)] for index, label in enumerate(labels)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a stability phase diagram for teleportation-cycle data."
    )
    parser.add_argument(
        "--csvs",
        nargs="+",
        help="List of input CSV paths for multi-run plotting.",
    )
    parser.add_argument(
        "--run-labels",
        nargs="+",
        help="List of run labels matching --csvs order.",
    )
    parser.add_argument(
        "--csv",
        default="data/samples/sample_measurements.csv",
        help="Path to a single input CSV matching the MeasurementRecord schema.",
    )
    parser.add_argument(
        "--output",
        default="data/output/multi_run_phase_diagram.png",
        help="Output PNG path.",
    )
    parser.add_argument(
        "--title",
        default="Stability Phase Diagram — Multi-Run",
        help="Plot title.",
    )
    parser.add_argument(
        "--x-field",
        default="cycle_index",
        help=(
            "Record field to use as the X-axis (e.g. bias_khz, delta_t_ns). "
            "Falls back to cycle_index if the field is absent or None."
        ),
    )
    return parser


def _resolve_inputs(
    csv: str, csvs: list[str] | None, run_labels: list[str] | None
) -> tuple[list[Path], list[str]]:
    if csvs:
        csv_paths = [Path(path) for path in csvs]
        for csv_path in csv_paths:
            if not csv_path.exists():
                raise SystemExit(f"CSV file not found: {csv_path}")
        labels = run_labels if run_labels is not None else [p.stem for p in csv_paths]
        if len(labels) != len(csv_paths):
            raise SystemExit("Error: --csvs and --run-labels must have the same length.")
        return csv_paths, labels

    csv_path = Path(csv)
    if not csv_path.exists():
        raise SystemExit(f"CSV file not found: {csv_path}")
    label = run_labels[0] if run_labels else csv_path.stem
    return [csv_path], [label]


def _collect_records_with_labels(
    csv_paths: list[Path], run_labels: list[str]
) -> list[tuple[MeasurementRecord, str]]:
    records_with_labels: list[tuple[MeasurementRecord, str]] = []
    for csv_path, run_label in zip(csv_paths, run_labels):
        records = load_records(csv_path)
        records_with_labels.extend((record, run_label) for record in records)
    return records_with_labels


def _resolve_x_value(record: MeasurementRecord, x_field: str) -> float:
    """Return the value of *x_field* from *record*, falling back to cycle_index."""
    if x_field != "cycle_index":
        value = getattr(record, x_field, None)
        if value is not None:
            return float(value)
    return float(record.cycle_index)


def plot_phase_diagram(
    records_with_labels: list[tuple[MeasurementRecord, str]],
    output_path: Path,
    title: str,
    x_field: str = "cycle_index",
) -> None:
    if not records_with_labels:
        raise SystemExit("No records loaded from provided CSV inputs.")

    run_markers = run_marker_map(run_label for _, run_label in records_with_labels)
    colors = stability_color_map()

    # Determine the effective X label: use the requested field name unless we
    # fell back to cycle_index for every record (field absent on the dataclass).
    first_record = records_with_labels[0][0]
    effective_x_field = (
        x_field
        if x_field == "cycle_index" or getattr(first_record, x_field, None) is not None
        else "cycle_index"
    )
    x_label = effective_x_field.replace("_", " ").title()

    points_by_class_and_run: dict[str, dict[str, list[tuple[float, float]]]] = {}
    for record, run_label in records_with_labels:
        classification = classify_cycle(record)
        x_val = _resolve_x_value(record, x_field)
        points_by_class_and_run.setdefault(classification, {}).setdefault(
            run_label, []
        ).append((x_val, record.cm_t))

    fig, ax = plt.subplots(figsize=(11, 7))
    for classification, grouped_by_run in points_by_class_and_run.items():
        for run_label, points in grouped_by_run.items():
            xs = [x for x, _ in points]
            ys = [y for _, y in points]
            ax.scatter(
                xs,
                ys,
                s=40,
                alpha=0.85,
                color=colors.get(classification, "black"),
                marker=run_markers[run_label],
                edgecolors="none",
                label=f"{run_label} — {classification}",
            )

    ax.set_xlabel(x_label)
    ax.set_ylabel("CM_t = T2* / (T_BSE + T_FF)")
    ax.set_title(title)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.grid(True, alpha=0.3)
    ax.legend(title="Run × Stability Class", loc="best", fontsize="small")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    csv_paths, run_labels = _resolve_inputs(
        csv=args.csv, csvs=args.csvs, run_labels=args.run_labels
    )
    records_with_labels = _collect_records_with_labels(csv_paths, run_labels)
    if not records_with_labels:
        raise SystemExit("No records loaded; check CSV paths and schema.")

    output_path = Path(args.output)
    plot_phase_diagram(
        records_with_labels=records_with_labels,
        output_path=output_path,
        title=args.title,
        x_field=args.x_field,
    )
    print(f"Wrote stability phase diagram to {output_path}")


if __name__ == "__main__":
    main()
