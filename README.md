# quantum-computer-room-temp

Room-temperature quantum-computing research scaffold focused on spin-exciton proxy metrics, repeatable protocol design, and lightweight analysis utilities.

## Repository Layout
- `docs/` — protocol and specification docs
- `data/` — raw/processed/sample datasets
- `src/` — schema + analysis utilities
- `notebooks/` — exploratory analysis workspace

## Quickstart
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the analysis entrypoint on the sample dataset:
   ```bash
   python src/run_analysis.py
   ```
4. Optionally run against another CSV:
   ```bash
   python src/run_analysis.py path/to/your_measurements.csv
   ```
5. Generate a stability phase diagram:
   ```bash
   python src/plot_phase_diagram.py \
     --csv data/samples/sample_measurements.csv \
     --output data/output/run05_15_phase_diagram.png
   ```

The CLI now parses teleportation-cycle records and computes derived cycle metrics such as `t_active_ns`, `t_cycle_ns`, and `CM_t`.
It validates each cycle against the v0.2 timing/reset/handoff scaffold and prints per-cycle stability classes.

## Included Starter Assets
- `docs/experiment-protocol.md`
- `docs/spec-v0.2.md`
- `data/README.md`
- `data/samples/sample_measurements.csv`
- `src/metrics_schema.py`
- `src/basic_analysis.py`
- `src/validation.py`
- `src/stability.py`
- `src/run_analysis.py`
- `notebooks/README.md`

## Teleportation-Aligned CSV Fields
Each cycle row records the existing environmental/proxy metrics plus the v0.2 timing and state-transfer fields:

- `cycle_index`
- `t_pi_ns`, `t_bse_ns`, `t_ff_ns`, `t_uesa_ns`
- `t2_star_ns`
- `handoff_checksum`, `prior_handoff_checksum`
- `reset_confirmed`
- `state_continuity_flag`

The sample CSV includes representative stable, non-viable, timing-marginal, reset-invalid, and handoff-degraded cycles so the analysis report exercises the new classification flow.

## Reproducibility Checklist
- Keep hardware configuration fixed per run.
- Log software and firmware versions.
- Use consistent sampling intervals.
- Record calibration and manual interventions.
- Preserve raw data prior to transformation.
- Store processing notes alongside outputs.

## Disclaimer
This repository is a research scaffold and does not claim fault-tolerant quantum performance.
