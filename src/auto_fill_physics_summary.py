import os
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "timestamp",
    "cycle_index",
    "ambient_temperature_c",
    "relative_humidity_pct",
    "vibration_index",
    "em_noise_estimate",
    "coherence_proxy",
    "spin_exciton_proxy",
    "t_pi_ns",
    "t_bse_ns",
    "t_ff_ns",
    "t_uesa_ns",
    "t2_star_ns",
    "handoff_checksum",
    "prior_handoff_checksum",
    "reset_confirmed",
    "state_continuity_flag",
    "anomaly_note",
    "bias_khz"
]

def load_run_csv(path):
    """Load a single run CSV and validate schema."""
    df = pd.read_csv(path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")

    # Derived metrics
    df["t_active_ns"] = df["t_bse_ns"] + df["t_ff_ns"]
    df["t_cycle_ns"] = df["t_pi_ns"] + df["t_bse_ns"] + df["t_ff_ns"] + df["t_uesa_ns"]
    df["CM_t"] = df["t2_star_ns"] / df["t_active_ns"]

    return df


def load_all_runs(data_dir="data", run_start=5, run_end=15):
    """Load run05.csv … run15.csv into a dict of DataFrames."""
    runs = {}
    for run_id in range(run_start, run_end + 1):
        filename = f"run{run_id:02d}.csv"
        path = os.path.join(data_dir, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Expected file missing: {path}")

        runs[run_id] = load_run_csv(path)

    return runs


def compute_plateau(df):
    """Return bias range where CM_t stays above 1.0."""
    stable = df[df["CM_t"] >= 1.0]
    if stable.empty:
        return None
    return stable["bias_khz"].min(), stable["bias_khz"].max()


def compute_collapse_boundary(df):
    """Return the first bias where CM_t < 1.0."""
    collapsed = df[df["CM_t"] < 1.0]
    if collapsed.empty:
        return None
    return collapsed["bias_khz"].min()


def compute_drift_corridors(df):
    """
    Identify drift corridors: regions where CM_t is unstable
    (oscillatory, sloping, or dipping before collapse).
    This is a heuristic placeholder — refine later.
    """
    cm = df["CM_t"].values
    bias = df["bias_khz"].values

    # Simple heuristic: look for high variance in sliding windows
    corridors = []
    window = 5
    for i in range(len(cm) - window):
        segment = cm[i:i+window]
        if np.std(segment) > 0.15:  # tunable threshold
            corridors.append((bias[i], bias[i+window-1]))

    return corridors


def summarize_run(df):
    """Compute plateau, collapse, and drift corridor summary for one run."""
    plateau = compute_plateau(df)
    collapse = compute_collapse_boundary(df)
    corridors = compute_drift_corridors(df)

    return {
        "plateau": plateau,
        "collapse_boundary": collapse,
        "drift_corridors": corridors
    }


def summarize_all_runs(runs):
    """Return a dict keyed by run_id with physics summaries."""
    summary = {}
    for run_id, df in runs.items():
        summary[run_id] = summarize_run(df)
    return summary


if __name__ == "__main__":
    runs = load_all_runs()
    summary = summarize_all_runs(runs)

    print("Physics summary (Run05–Run15):")
    for run_id, info in summary.items():
        print(f"\nRun {run_id:02d}")
        print(f"  Plateau: {info['plateau']}")
        print(f"  Collapse boundary: {info['collapse_boundary']}")
        print(f"  Drift corridors: {info['drift_corridors']}")
