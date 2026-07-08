"""Generate a stability phase diagram from teleportation-cycle CSV data."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from basic_analysis import load_records
from stability import classify_cycle


def stability_color_map() -> dict[str, str]:
    return {
        "teleportation_stable": "tab:green",
        "timing_marginal": "tab:orange",
        "handoff_degraded": "tab:red",
        "reset_invalid": "tab:pink",
        "non_viable": "tab:gray",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a stability phase diagram for teleportation-cycle data."
    )
    parser.add_argument(
        "--csv",
        default="data/samples/sample_measurements.csv",
        help="Path to input CSV matching the MeasurementRecord schema.",
    )
    parser.add_argument(
        "--output",
        default="data/output/run05_15_phase_diagram.png",
        help="Output PNG path.",
    )
    parser.add_argument(
        "--title",
        default="Stability Phase Diagram — Run 05–15",
        help="Plot title.",
    )
    return parser


def plot_phase_diagram(csv_path: Path, output_path: Path, title: str) -> None:
    records = load_records(csv_path)
    if not records:
        raise SystemExit(f"No records loaded from CSV: {csv_path}")

    colors = stability_color_map()

    points_by_class: dict[str, list[tuple[int, float]]] = {}
    for record in records:
        classification = classify_cycle(record)
        points_by_class.setdefault(classification, []).append(
            (record.cycle_index, record.cm_t)
        )

    fig, ax = plt.subplots(figsize=(10, 6))
    for classification, points in points_by_class.items():
        xs = [x for x, _ in points]
        ys = [y for _, y in points]
        ax.scatter(
            xs,
            ys,
            s=35,
            alpha=0.85,
            color=colors.get(classification, "black"),
            edgecolors="none",
            label=classification,
        )

    ax.set_xlabel("Cycle index")
    ax.set_ylabel("CM_t = T2* / (T_BSE + T_FF)")
    ax.set_title(title)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.grid(True, alpha=0.3)
    ax.legend(title="Stability class", loc="best")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"CSV file not found: {csv_path}")

    output_path = Path(args.output)
    plot_phase_diagram(csv_path=csv_path, output_path=output_path, title=args.title)
    print(f"Wrote stability phase diagram to {output_path}")


if __name__ == "__main__":
    main()
