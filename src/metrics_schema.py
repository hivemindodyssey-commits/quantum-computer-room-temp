"""Schema helpers for teleportation-aligned room-temperature cycle metrics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MeasurementRecord:
    timestamp: datetime
    cycle_index: int
    ambient_temperature_c: float
    relative_humidity_pct: float
    vibration_index: float
    em_noise_estimate: float
    coherence_proxy: float
    spin_exciton_proxy: float
    t_pi_ns: float
    t_bse_ns: float
    t_ff_ns: float
    t_uesa_ns: float
    t2_star_ns: float
    reset_confirmed: bool
    handoff_checksum: Optional[str] = None
    prior_handoff_checksum: Optional[str] = None
    state_continuity_flag: Optional[bool] = None
    anomaly_note: Optional[str] = None

    @property
    def t_active_ns(self) -> float:
        return self.t_bse_ns + self.t_ff_ns

    @property
    def t_cycle_ns(self) -> float:
        return self.t_pi_ns + self.t_bse_ns + self.t_ff_ns + self.t_uesa_ns

    @property
    def cm_t(self) -> float:
        if self.t_active_ns <= 0:
            return 0.0
        return self.t2_star_ns / self.t_active_ns


def validate_record(record: MeasurementRecord) -> list[str]:
    """Backward-compatible proxy for the focused v0.2 validation module."""
    from validation import validate_record as validate_cycle_record

    return validate_cycle_record(record)
