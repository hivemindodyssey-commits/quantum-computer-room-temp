"""Basic analysis utilities for teleportation-aligned cycle inspection."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from statistics import mean

from metrics_schema import MeasurementRecord
from validation import validate_record


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


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def _parse_optional_bool(value: str) -> bool | None:
    if not value.strip():
        return None
    return parse_bool(value)


def _parse_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def parse_record(row: dict[str, str]) -> MeasurementRecord:
    return MeasurementRecord(
        timestamp=_parse_timestamp(row["timestamp"]),
        cycle_index=int(row["cycle_index"]),
        ambient_temperature_c=float(row["ambient_temperature_c"]),
        relative_humidity_pct=float(row["relative_humidity_pct"]),
        vibration_index=float(row["vibration_index"]),
        em_noise_estimate=float(row["em_noise_estimate"]),
        coherence_proxy=float(row["coherence_proxy"]),
        spin_exciton_proxy=float(row["spin_exciton_proxy"]),
        t_pi_ns=float(row["t_pi_ns"]),
        t_bse_ns=float(row["t_bse_ns"]),
        t_ff_ns=float(row["t_ff_ns"]),
        t_uesa_ns=float(row["t_uesa_ns"]),
        t2_star_ns=float(row["t2_star_ns"]),
        handoff_checksum=_parse_optional_text(row.get("handoff_checksum")),
        prior_handoff_checksum=_parse_optional_text(row.get("prior_handoff_checksum")),
        reset_confirmed=parse_bool(row["reset_confirmed"]),
        state_continuity_flag=_parse_optional_bool(
            row.get("state_continuity_flag", "")
        ),
        anomaly_note=_parse_optional_text(row.get("anomaly_note")),
    )


def load_records(csv_path: str | Path) -> list[MeasurementRecord]:
    return [parse_record(row) for row in load_rows(csv_path)]


def _metric_summary(values: list[float]) -> dict[str, float]:
    return {
        "mean": mean(values),
        "min": min(values),
        "max": max(values),
    }


def compute_cycle_metrics(records: list[MeasurementRecord]) -> dict[str, object]:
    if not records:
        return {
            "record_count": 0,
            "t_active_ns": None,
            "t_cycle_ns": None,
            "cm_t": None,
            "reset_confirmed_count": 0,
            "continuity_ok_count": 0,
            "continuity_required_count": 0,
        }

    continuity_required = [record for record in records if record.cycle_index > 0]
    continuity_ok_count = sum(
        record.state_continuity_flag is True for record in continuity_required
    )

    return {
        "record_count": len(records),
        "t_active_ns": _metric_summary([record.t_active_ns for record in records]),
        "t_cycle_ns": _metric_summary([record.t_cycle_ns for record in records]),
        "cm_t": _metric_summary([record.cm_t for record in records]),
        "reset_confirmed_count": sum(record.reset_confirmed for record in records),
        "continuity_ok_count": continuity_ok_count,
        "continuity_required_count": len(continuity_required),
    }


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


def summarize_validation_failures(
    records: list[MeasurementRecord],
) -> dict[int, list[str]]:
    failures: dict[int, list[str]] = {}
    for record in records:
        errors = validate_record(record)
        if errors:
            failures[record.cycle_index] = errors
    return failures


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
        records = load_records(sample_path)
        metrics = compute_cycle_metrics(records)
        print(f"Loaded {metrics['record_count']} teleportation cycles.")
        if metrics["cm_t"]:
            print(f"Mean cm_t: {metrics['cm_t']['mean']:.6f}")
    else:
        print("Sample file not found at data/samples/sample_measurements.csv")
