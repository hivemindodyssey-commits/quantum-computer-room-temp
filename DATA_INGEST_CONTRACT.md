# Data Ingest Contract (Run05–Run15)

## Required files
Place these files in `data/`:

- `run05.csv`
- `run06.csv`
- `run07.csv`
- `run08.csv`
- `run09.csv`
- `run10.csv`
- `run11.csv`
- `run12.csv`
- `run13.csv`
- `run14.csv`
- `run15.csv`

Filenames are case-sensitive in CI expectations (`run05.csv`, not `Run05.csv`).

## Required columns
Each CSV must include:

- `timestamp`
- `cycle_index`
- `ambient_temperature_c`
- `relative_humidity_pct`
- `vibration_index`
- `em_noise_estimate`
- `coherence_proxy`
- `spin_exciton_proxy`
- `t_pi_ns`
- `t_bse_ns`
- `t_ff_ns`
- `t_uesa_ns`
- `t2_star_ns`
- `handoff_checksum`
- `prior_handoff_checksum`
- `reset_confirmed`
- `state_continuity_flag`
- `anomaly_note`
- `bias_khz` (or supply a different field via `--x-field`)

## Data type expectations
- Numeric: `t_bse_ns`, `t_ff_ns`, `t2_star_ns`, `bias_khz` (and other timing/environment numeric fields)
- Boolean string: `reset_confirmed`, `state_continuity_flag` as `true|false`
- Non-empty: each file must have header + at least 1 data row

## Derived metrics
- `t_active_ns = t_bse_ns + t_ff_ns`
- `t_cycle_ns = t_pi_ns + t_bse_ns + t_ff_ns + t_uesa_ns`
- `CM_t = t2_star_ns / t_active_ns`

## Pre-push validation
Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\validate-runs.ps1
```

Push only if output ends with:

```text
GREEN LIGHT: run05–run15 ready to push.
```

## Commit/push (PowerShell-safe)
```powershell
git add data/run05.csv data/run06.csv data/run07.csv data/run08.csv data/run09.csv data/run10.csv data/run11.csv data/run12.csv data/run13.csv data/run14.csv data/run15.csv
git commit -m "Add Run05–Run15 physics-bearing CSVs"
git push
```

## Workflow execution
```powershell
python src/run_bias_sweep_workflow.py `
  --input-dir data `
  --run-start 5 `
  --run-end 15 `
  --x-field bias_khz `
  --output-dir data/output
```

## Expected outputs (`data/output/`)
- `run05_15_ingestion_manifest.csv`
- `run05_15_bias_sweep_atlas.png`
- `run05_15_stability_mosaic.png`
