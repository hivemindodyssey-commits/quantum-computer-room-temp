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

## Included Starter Assets
- `docs/experiment-protocol.md`
- `docs/spec-v0.2.md`
- `data/README.md`
- `data/samples/sample_measurements.csv`
- `src/metrics_schema.py`
- `src/basic_analysis.py`
- `src/run_analysis.py`
- `notebooks/README.md`

## Reproducibility Checklist
- Keep hardware configuration fixed per run.
- Log software and firmware versions.
- Use consistent sampling intervals.
- Record calibration and manual interventions.
- Preserve raw data prior to transformation.
- Store processing notes alongside outputs.

## Disclaimer
This repository is a research scaffold and does not claim fault-tolerant quantum performance.
