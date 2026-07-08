"""Stability classification helpers for teleportation-aligned cycles."""

from __future__ import annotations

from metrics_schema import MeasurementRecord
from validation import validate_timing_budget


STABILITY_CLASSES = (
    "teleportation_stable",
    "timing_marginal",
    "handoff_degraded",
    "reset_invalid",
    "non_viable",
)


def classify_cycle(record: MeasurementRecord) -> str:
    if record.cm_t < 1.0:
        return "non_viable"

    if not record.reset_confirmed:
        return "reset_invalid"

    if record.cycle_index > 0 and (
        not record.handoff_checksum
        or not record.prior_handoff_checksum
        or record.state_continuity_flag is False
        or record.state_continuity_flag is None
    ):
        return "handoff_degraded"

    if validate_timing_budget(record):
        return "timing_marginal"

    return "teleportation_stable"
