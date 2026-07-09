# Quantum Computer Room Temp

![Version](https://img.shields.io/badge/version-v2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/hivemindodyssey-commits/quantum-computer-room-temp/actions/workflows/ci.yml/badge.svg)
![Repo Size](https://img.shields.io/github/repo-size/hivemindodyssey-commits/quantum-computer-room-temp)
![Last Commit](https://img.shields.io/github/last-commit/hivemindodyssey-commits/quantum-computer-room-temp)

A research scaffold for deterministic temporal analysis of exciton–polariton racetrack behavior in a vdW-hosted stack, with explicit contracts for schema, summary, and template rendering.

## What this repository provides

- **Deterministic data ingestion** for Run05–Run15 style datasets
- **Physics summary extraction**:
  - plateau region
  - collapse boundary
  - drift corridors
- **Versioned documentation contracts**:
  - `docs/schema_v2.md`
  - `docs/summary_contract_v2.md`
  - `docs/template_interface_v2.md`
  - `docs/renderer_validation_v2.md`

## Current computation model (implemented)

From `src/auto_fill_physics_summary.py`:

- `t_active_ns = t_bse_ns + t_ff_ns`
- `t_cycle_ns = t_pi_ns + t_bse_ns + t_ff_ns + t_uesa_ns`
- `CM_t = t2_star_ns / t_active_ns`

Heuristic summaries:

- plateau: bias interval where `CM_t >= 1.0`
- collapse boundary: first bias where `CM_t < 1.0`
- drift corridors: sliding-window variance regions over `CM_t`

## Repository structure

- `src/` — ingestion + summary logic
- `data/` — run CSV inputs
- `docs/` — contracts, interfaces, validation specs

## Documentation split

Long-form architecture/theory and experiment workflows are maintained in docs:

- `docs/theory/time_crystal_architecture.md`
- `docs/experiments/subharmonic_validation_protocol.md`

## Scientific status note

This repo contains both:
- **implemented deterministic extraction logic** (code-backed), and
- **forward-looking theoretical architecture text** (research hypothesis).

Do not treat theoretical sections as experimentally validated claims unless independently verified.

## Quick start

```bash
python src/auto_fill_physics_summary.py
```

Expected output: per-run plateau, collapse boundary, drift corridor summaries.

## Contract-first workflow (recommended)

1. Validate input against `docs/schema_v2.md`
2. Produce summary payload per `docs/summary_contract_v2.md`
3. Render templates via `docs/template_interface_v2.md`
4. Enforce CI checks from `docs/renderer_validation_v2.md`
