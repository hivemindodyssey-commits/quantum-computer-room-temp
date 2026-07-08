"""Schema helpers for room-temperature quantum environment metrics."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MeasurementRecord:
    timestamp: datetime
    ambient_temperature_c: float
    relative_humidity_pct: float
    vibration_index: float
    em_noise_estimate: float
    coherence_proxy: float
    spin_exciton_proxy: float
    anomaly_note: Optional[str] = None


def validate_record(record: MeasurementRecord) -> list[str]:
    """Return a list of validation errors; empty list means valid."""
    errors: list[str] = []

    if not (-20.0 <= record.ambient_temperature_c <= 80.0):
        errors.append("ambient_temperature_c out of expected range (-20 to 80)")

    if not (0.0 <= record.relative_humidity_pct <= 100.0):
        errors.append("relative_humidity_pct must be between 0 and 100")

    for field_name in [
        "vibration_index",
        "em_noise_estimate",
        "coherence_proxy",
        "spin_exciton_proxy",
    ]:
        value = getattr(record, field_name)
        if value != value:  # NaN check
            errors.append(f"{field_name} must not be NaN")

    return errors
