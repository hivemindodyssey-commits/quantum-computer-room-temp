"""Validation helpers for teleportation-aligned measurement records."""

from __future__ import annotations

from metrics_schema import MeasurementRecord


TIMING_TARGETS_NS = {
    "t_pi_ns": 1.0,
    "t_bse_ns": 100.0,
    "t_ff_ns": 40.0,
    "t_uesa_ns": 500.0,
}
TIMING_TOLERANCE_RATIO = 0.05
CYCLE_TARGET_NS = 641.0


def _is_nan(value: float) -> bool:
    return value != value


def _within_target(value: float, target: float) -> bool:
    tolerance = target * TIMING_TOLERANCE_RATIO
    return abs(value - target) <= tolerance


def validate_environmental_ranges(record: MeasurementRecord) -> list[str]:
    errors: list[str] = []

    if record.cycle_index < 0:
        errors.append("cycle_index must be non-negative")

    if not (-20.0 <= record.ambient_temperature_c <= 80.0):
        errors.append("ambient_temperature_c out of expected range (-20 to 80)")

    if not (0.0 <= record.relative_humidity_pct <= 100.0):
        errors.append("relative_humidity_pct must be between 0 and 100")

    for field_name in [
        "vibration_index",
        "em_noise_estimate",
        "coherence_proxy",
        "spin_exciton_proxy",
        "t2_star_ns",
    ]:
        value = getattr(record, field_name)
        if _is_nan(value):
            errors.append(f"{field_name} must not be NaN")

    return errors


def validate_timing_budget(record: MeasurementRecord) -> list[str]:
    errors: list[str] = []

    for field_name, target in TIMING_TARGETS_NS.items():
        value = getattr(record, field_name)
        if value <= 0:
            errors.append(f"{field_name} must be positive")
            continue
        if not _within_target(value, target):
            errors.append(
                f"{field_name} must stay within ±5% of {target:.0f} ns target"
            )

    if record.t2_star_ns <= 0:
        errors.append("t2_star_ns must be positive")

    if record.t_active_ns <= 0:
        errors.append("t_active_ns must be positive")

    if not _within_target(record.t_cycle_ns, CYCLE_TARGET_NS):
        errors.append("t_cycle_ns must stay within ±5% of 641 ns target")

    return errors


def validate_teleportation_semantics(record: MeasurementRecord) -> list[str]:
    errors: list[str] = []

    if record.cm_t < 1.0:
        errors.append("cm_t must be at least 1.0 for baseline viability")

    if not record.reset_confirmed:
        errors.append("reset_confirmed must be true for compliant cycles")

    if record.cycle_index > 0:
        if not record.prior_handoff_checksum:
            errors.append(
                "prior_handoff_checksum is required for nonzero cycle indices"
            )
        if not record.handoff_checksum:
            errors.append("handoff_checksum is required for nonzero cycle indices")
        if record.state_continuity_flag is not True:
            errors.append(
                "state_continuity_flag must be true for nonzero cycle indices"
            )

    return errors


def validate_record(record: MeasurementRecord) -> list[str]:
    """Return v0.2 scaffold validation errors for a single cycle."""
    return (
        validate_environmental_ranges(record)
        + validate_timing_budget(record)
        + validate_teleportation_semantics(record)
    )
