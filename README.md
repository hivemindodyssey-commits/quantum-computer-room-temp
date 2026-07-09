# quantum-computer-room-temp

![Dataset Validation](https://github.com/hivemindodyssey-commits/quantum-computer-room-temp/actions/workflows/validate-dataset.yml/badge.svg)

Room-temperature quantum-computing research scaffold focused on spin-exciton proxy metrics, repeatable protocol design, and lightweight analysis utilities.

## Table of Contents
- [Quickstart](#quickstart)
- [Data Ingest Contract](#data-ingest-contract-run05run15)
- [Workflow Execution](#workflow-execution)
- [Outputs](#outputs)
- [Data Provenance](#data-provenance)
- [Developer Notes](#developer-notes)
- [Reproducibility Checklist](#reproducibility-checklist)
- [Disclaimer](#disclaimer)

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

## Data Ingest Contract (Run05–Run15)

The Run05–Run15 bias-sweep analysis pipeline requires a set of physics-bearing CSV
files that conform to the v0.2 `MeasurementRecord` schema. These files define the
input domain for ingestion, validation, stability classification, and atlas/mosaic
generation.

A full specification of required files, schema, data types, derived metrics, and
pre-push validation steps is provided here:

➡️ **[DATA_INGEST_CONTRACT.md](./DATA_INGEST_CONTRACT.md)**

Before running the multi-run workflow, ensure that:

- All required CSVs (`run05.csv` … `run15.csv`) are present in `data/`
- Each file passes the validation script (`validate-runs.ps1`)
- Filenames match CI expectations (case-sensitive)
- Sweep parameter (`bias_khz` or alternative `--x-field`) is included

## Workflow Execution
Once the data ingest contract is satisfied, execute:

```bash
python src/run_bias_sweep_workflow.py \
  --input-dir data \
  --run-start 5 \
  --run-end 15 \
  --x-field bias_khz \
  --output-dir data/output
```

## Outputs
This produces:

- `run05_15_ingestion_manifest.csv`
- `run05_15_bias_sweep_atlas.png`
- `run05_15_stability_mosaic.png`

These artifacts form the basis for coherence-window analysis, collapse-boundary
mapping, drift-corridor identification, and run-to-run stability interpretation.

## Data Provenance
The Run05–Run15 dataset provenance is tracked with both human-readable and machine-readable manifests:

- Text manifest: **[`data/manifest_run05_15.txt`](./data/manifest_run05_15.txt)**
- JSON manifest: **[`data/manifest_run05_15.json`](./data/manifest_run05_15.json)**

Use these manifests to verify run presence, schema versioning, validation status, and derived metric definitions before executing multi-run analysis.

## Developer Notes
### Workflow trigger logic
- Dataset validation CI is designed to trigger on dataset and validation script changes.
- Expected trigger paths include `data/run*.csv`, `data/manifest_run05_15.txt`, `data/manifest_run05_15.json`, and `validate-runs.ps1`.

### Data and manifest assumptions
- The multi-run pipeline assumes contiguous Run05–Run15 CSV availability in `data/`.
- Filenames are case-sensitive and must match contract expectations exactly.
- Provenance is dual-layered: text manifest for human inspection and JSON manifest for machine validation and CI workflows.

### Validation contract
- `validate-runs.ps1` is the gatekeeper for schema and field-level integrity.
- Validation is expected to fail fast on missing files, required-column mismatches, or invalid numeric/boolean field encodings.
- CI status should be treated as authoritative for merge readiness of dataset updates.

### Timing and sequence architecture
- Canonical execution order:
  1. **Ingest readiness check** (file presence and naming)
  2. **Schema validation** (`validate-runs.ps1`)
  3. **Bias sweep execution** (`src/run_bias_sweep_workflow.py`)
  4. **Artifact generation** (ingestion manifest, atlas, stability mosaic)
  5. **Interpretation and reporting** (physics summary and stability review)
- Any failed precondition in steps 1–2 should block downstream analysis to preserve reproducibility.

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
