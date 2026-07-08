"""Basic analysis utilities for exploratory metric inspection."""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


NUMERIC_FIELDS = [
    "ambient_temperature_c",
    "relative_humidity_pct",
    "vibration_index",
    "em_noise_estimate",
    "coherence_proxy",
    "spin_exciton_proxy",
]


def load_rows(csv_path: str | Path) -> list[dict[str, str]]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def summarize_numeric_fields(rows: list[dict[str, str]]) -> dict[str, float]:
    summary: dict[str, float] = {}
    if not rows:
        return summary

    for field in NUMERIC_FIELDS:
        values: list[float] = []
        for row in rows:
            raw = row.get(field, "").strip()
            if not raw:
                continue
            try:
                values.append(float(raw))
            except ValueError:
                continue

        if values:
            summary[field] = mean(values)

    return summary


def print_summary(summary: dict[str, float]) -> None:
    if not summary:
        print("No numeric summary available.")
        return

    print("Mean values by metric:")
    for key, value in summary.items():
        print(f"- {key}: {value:.6f}")


if __name__ == "__main__":
    sample_path = Path("data/samples/sample_measurements.csv")
    if sample_path.exists():
        rows = load_rows(sample_path)
        print_summary(summarize_numeric_fields(rows))
    else:
        print("Sample file not found at data/samples/sample_measurements.csv")
