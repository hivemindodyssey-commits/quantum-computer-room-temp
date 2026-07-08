# Experiment Protocol (v0.1)

## Objective
Establish a repeatable baseline protocol for observing room-temperature environmental effects on quantum coherence proxies and spin-exciton response metrics.

## Controlled Variables
- Ambient temperature (°C)
- Relative humidity (%)
- Vibration index (arbitrary units)
- Electromagnetic (EM) noise estimate (arbitrary units)

## Session Setup
1. Calibrate measurement instruments.
2. Record baseline environment for 10 minutes.
3. Start observation window with fixed sampling interval.
4. Introduce one controlled perturbation at a time.
5. Return to baseline and continue capture.

## Sampling Guidance
- Recommended sampling interval: 1-10 seconds (depending on equipment).
- Minimum session duration: 30 minutes.
- Repeat each condition in at least 3 runs.

## Data Requirements
Each record should contain:
- timestamp
- ambient_temperature_c
- relative_humidity_pct
- vibration_index
- em_noise_estimate
- coherence_proxy
- spin_exciton_proxy
- anomaly_note

## Quality Checks
- Validate timestamp monotonicity.
- Reject out-of-range sensor values.
- Flag missing fields before analysis.

## Reproducibility Notes
- Keep hardware configuration constant per run.
- Record firmware/software versions.
- Document any manual interventions.
