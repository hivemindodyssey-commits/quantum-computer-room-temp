"""Run 05–15 ingestion + bias-sweep atlas + stability mosaic workflow."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from math import ceil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from basic_analysis import load_records
from metrics_schema import MeasurementRecord
from plot_phase_diagram import _resolve_x_value, stability_color_map
from stability import STABILITY_CLASSES, classify_cycle

TEXT_COLOR_THRESHOLD = 0.45


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run an ingestion workflow for Run 05–15 datasets and generate a "
            "bias-sweep atlas plus a combined stability mosaic."
        )
    )
    parser.add_argument(
        "--input-dir",
        default="data",
        help="Directory containing runXX.csv files (default: data).",
    )
    parser.add_argument(
        "--run-start",
        type=int,
        default=5,
        help="First run number to include (default: 5).",
    )
    parser.add_argument(
        "--run-end",
        type=int,
        default=15,
        help="Last run number to include (default: 15).",
    )
    parser.add_argument(
        "--x-field",
        default="bias_khz",
        help=(
            "Field to plot on X-axis in atlas charts. Falls back to cycle_index "
            "for records without this field."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="data/output",
        help="Directory where workflow outputs are written.",
    )
    parser.add_argument(
        "--manifest",
        default="run05_15_ingestion_manifest.csv",
        help="Filename for ingestion summary CSV.",
    )
    parser.add_argument(
        "--atlas-output",
        default="run05_15_bias_sweep_atlas.png",
        help="Filename for the per-run bias-sweep atlas image.",
    )
    parser.add_argument(
        "--mosaic-output",
        default="run05_15_stability_mosaic.png",
        help="Filename for combined stability mosaic image.",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Skip missing run files instead of failing.",
    )
    return parser


def _run_filename(run_number: int) -> str:
    return f"run{run_number:02d}.csv"


def discover_runs(
    input_dir: Path, run_start: int, run_end: int, allow_missing: bool
) -> list[tuple[str, Path]]:
    if run_start > run_end:
        raise SystemExit(
            f"--run-start ({run_start}) must be <= --run-end ({run_end})."
        )

    discovered: list[tuple[str, Path]] = []
    missing: list[str] = []

    for run_number in range(run_start, run_end + 1):
        label = f"Run{run_number:02d}"
        csv_path = input_dir / _run_filename(run_number)
        if csv_path.exists():
            discovered.append((label, csv_path))
        else:
            missing.append(str(csv_path))

    if missing and not allow_missing:
        joined = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"Missing expected run CSV files:\n{joined}")
    if not discovered:
        raise SystemExit("No run CSV files discovered.")
    return discovered


def load_run_records(
    run_csvs: list[tuple[str, Path]],
) -> dict[str, list[MeasurementRecord]]:
    records_by_run: dict[str, list[MeasurementRecord]] = {}
    for label, csv_path in run_csvs:
        records = load_records(csv_path)
        if not records:
            raise SystemExit(f"No records found in {csv_path}")
        records_by_run[label] = records
    return records_by_run


def _effective_x_field(records: list[MeasurementRecord], requested_x_field: str) -> str:
    if requested_x_field == "cycle_index":
        return requested_x_field
    for record in records:
        if getattr(record, requested_x_field, None) is not None:
            return requested_x_field
    return "cycle_index"


def _run_span_label(run_labels: list[str]) -> str:
    run_numbers: list[int] = []
    for run_label in run_labels:
        match = re.search(r"(\d+)", run_label)
        if match:
            run_numbers.append(int(match.group(1)))
    if not run_numbers:
        return "Selected Runs"
    return f"Runs {min(run_numbers):02d}–{max(run_numbers):02d}"


def write_ingestion_manifest(
    records_by_run: dict[str, list[MeasurementRecord]],
    run_paths: dict[str, Path],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "run_label",
                "csv_path",
                "record_count",
                "mean_cm_t",
                "teleportation_stable_count",
                "viable_fraction",
            ],
        )
        writer.writeheader()
        for run_label in sorted(records_by_run):
            records = records_by_run[run_label]
            classifications = [classify_cycle(record) for record in records]
            class_counts = Counter(classifications)
            stable_count = class_counts.get("teleportation_stable", 0)
            writer.writerow(
                {
                    "run_label": run_label,
                    "csv_path": str(run_paths[run_label]),
                    "record_count": len(records),
                    "mean_cm_t": f"{np.mean([r.cm_t for r in records]):.6f}",
                    "teleportation_stable_count": stable_count,
                    "viable_fraction": f"{stable_count / len(records):.6f}",
                }
            )


def build_bias_sweep_atlas(
    records_by_run: dict[str, list[MeasurementRecord]],
    output_path: Path,
    x_field: str,
    title: str,
) -> None:
    colors = stability_color_map()
    run_labels = sorted(records_by_run)
    cols = 3
    rows = ceil(len(run_labels) / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5.5, rows * 4.0), squeeze=False)

    for index, run_label in enumerate(run_labels):
        row = index // cols
        col = index % cols
        ax = axes[row][col]
        records = records_by_run[run_label]
        effective_x_field = _effective_x_field(records, x_field)

        points_by_class: dict[str, list[tuple[float, float]]] = {}
        for record in records:
            points_by_class.setdefault(classify_cycle(record), []).append(
                (_resolve_x_value(record, x_field), record.cm_t)
            )

        for stability_class in STABILITY_CLASSES:
            points = points_by_class.get(stability_class, [])
            if not points:
                continue
            xs = [x for x, _ in points]
            ys = [y for _, y in points]
            ax.scatter(
                xs,
                ys,
                s=28,
                alpha=0.9,
                color=colors.get(stability_class, "black"),
                edgecolors="none",
                label=stability_class,
            )

        ax.set_title(run_label)
        ax.set_xlabel(effective_x_field.replace("_", " ").title())
        ax.set_ylabel("CM_t")
        ax.axhline(1.0, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
        ax.grid(alpha=0.25)

    total_axes = rows * cols
    for index in range(len(run_labels), total_axes):
        row = index // cols
        col = index % cols
        axes[row][col].axis("off")

    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            linestyle="",
            color=colors.get(stability_class, "black"),
            label=stability_class,
        )
        for stability_class in STABILITY_CLASSES
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3, title="Stability class")
    fig.suptitle(title)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def build_stability_mosaic(
    records_by_run: dict[str, list[MeasurementRecord]],
    output_path: Path,
    title: str,
) -> None:
    run_labels = sorted(records_by_run)
    class_labels = list(STABILITY_CLASSES)
    matrix = np.zeros((len(run_labels), len(class_labels)))

    for row_index, run_label in enumerate(run_labels):
        records = records_by_run[run_label]
        class_counts = Counter(classify_cycle(record) for record in records)
        total = len(records)
        for col_index, class_label in enumerate(class_labels):
            matrix[row_index, col_index] = class_counts.get(class_label, 0) / total

    fig, ax = plt.subplots(figsize=(10, max(4, len(run_labels) * 0.65)))
    image = ax.imshow(matrix, cmap="viridis", aspect="auto", vmin=0.0, vmax=1.0)
    fig.colorbar(image, ax=ax, label="Fraction of cycles")

    ax.set_xticks(range(len(class_labels)))
    ax.set_xticklabels([label.replace("_", "\n") for label in class_labels], fontsize=9)
    ax.set_yticks(range(len(run_labels)))
    ax.set_yticklabels(run_labels)
    ax.set_title(title)

    for row_index in range(len(run_labels)):
        for col_index in range(len(class_labels)):
            value = matrix[row_index, col_index]
            ax.text(
                col_index,
                row_index,
                f"{value:.2f}",
                ha="center",
                va="center",
                color="white" if value > TEXT_COLOR_THRESHOLD else "black",
                fontsize=8,
            )

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    discovered = discover_runs(
        input_dir=input_dir,
        run_start=args.run_start,
        run_end=args.run_end,
        allow_missing=args.allow_missing,
    )
    run_paths = {label: path for label, path in discovered}
    records_by_run = load_run_records(discovered)
    run_span = _run_span_label(sorted(records_by_run))

    manifest_path = output_dir / args.manifest
    atlas_path = output_dir / args.atlas_output
    mosaic_path = output_dir / args.mosaic_output

    write_ingestion_manifest(
        records_by_run=records_by_run, run_paths=run_paths, output_path=manifest_path
    )
    build_bias_sweep_atlas(
        records_by_run=records_by_run,
        output_path=atlas_path,
        x_field=args.x_field,
        title=f"Bias-Sweep Stability Atlas ({run_span})",
    )
    build_stability_mosaic(
        records_by_run=records_by_run,
        output_path=mosaic_path,
        title=f"Combined Stability Mosaic ({run_span})",
    )

    print(f"{run_span} workflow complete:")
    print(f"- Ingestion manifest: {manifest_path}")
    print(f"- Bias-sweep atlas: {atlas_path}")
    print(f"- Stability mosaic: {mosaic_path}")


if __name__ == "__main__":
    main()
