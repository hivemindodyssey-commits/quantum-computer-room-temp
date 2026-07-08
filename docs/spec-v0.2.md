# Specification v0.2 — Teleportation-Aligned Room-Temperature Exciton Bus

## 1) Purpose

This specification defines a cycle-based control architecture where logical quantum state continuity is maintained via teleportation-style transfer across repeated, short-lived spin-exciton carriers at room temperature.

The core design principle is:

- The **logical state persists** across cycles.
- The **physical exciton carrier does not**; it is intentionally purged and re-instantiated each cycle.

---

## 2) Scope

This document covers:

- cycle timing model
- state-transfer interpretation
- coherence budget reformulation
- measurable acceptance criteria for early validation

Out of scope for v0.2:

- hardware-specific material stack guarantees
- full fault-tolerance threshold proofs
- fabrication and packaging constraints

---

## 3) Terms and Symbols

- \(T_{\pi}\): excitation pulse duration  
- \(T_{\mathrm{BSE}}\): estimation/inference window  
- \(T_{\mathrm{FF}}\): feed-forward correction packaging window  
- \(T_{\mathrm{UESA}}\): purge/reset window  
- \(T_{\mathrm{cycle}}\): total control-loop cycle duration  
- \(T_2^*\): effective dephasing/coherence time for active state handling  
- \(\mathrm{CM}_t\): teleportation-aligned coherence margin

Derived:

\[
T_{\mathrm{active}} = T_{\mathrm{BSE}} + T_{\mathrm{FF}}
\]

\[
\mathrm{CM}_t = \frac{T_2^*}{T_{\mathrm{active}}}
\]

---

## 4) Baseline Timing Budget (v0.2)

| Phase | Symbol | Duration (ns) | Role |
|---|---:|---:|---|
| π-pulse excitation | \(T_{\pi}\) | 1 | initialize exciton carrier |
| BSE estimation | \(T_{\mathrm{BSE}}\) | 100 | infer state/corrections |
| Feed-forward | \(T_{\mathrm{FF}}\) | 40 | package and route correction/state payload |
| UESA purge/reset | \(T_{\mathrm{UESA}}\) | 500 | intentional carrier destruction/reset |

\[
T_{\mathrm{cycle}} = 1 + 100 + 40 + 500 = 641\ \mathrm{ns}
\]

\[
T_{\mathrm{active}} = 100 + 40 = 140\ \mathrm{ns}
\]

---

## 5) Operational Cycle Semantics

Per cycle \(k\):

1. Instantiate carrier exciton via π-pulse.
2. Encode / bind logical-state representation onto carrier.
3. Perform BSE-based estimation over \(T_{\mathrm{BSE}}\).
4. Package feed-forward corrections over \(T_{\mathrm{FF}}\).
5. Purge carrier during \(T_{\mathrm{UESA}}\) (by design).
6. At cycle \(k+1\), instantiate a fresh carrier and reapply transferred logical-state payload.

Interpretation:

- Computation is a **state trajectory across cycles**.
- Excitons are **ephemeral transport primitives**.

---

## 6) Coherence Reformulation

### Legacy requirement (rejected for v0.2)
“Single exciton must remain coherent for full \(T_{\mathrm{cycle}} = 641\ \mathrm{ns}\).”

### Teleportation-aligned requirement (adopted for v0.2)
Logical state fidelity must be preserved across the active transfer window:

\[
T_{\mathrm{active}} = 140\ \mathrm{ns}
\]

\[
\mathrm{CM}_t = \frac{T_2^*}{140\ \mathrm{ns}}
\]

Engineering interpretation:

- \(\mathrm{CM}_t > 1\): operational timing margin exists
- \(\mathrm{CM}_t \approx 1\): threshold regime
- \(\mathrm{CM}_t < 1\): active window exceeds coherence budget

---

## 7) Acceptance Criteria (v0.2)

A run is considered v0.2-compliant if all are satisfied:

1. **Timing conformance**  
   Measured phase durations remain within ±5% of targets:
   - \(T_{\pi}=1\) ns
   - \(T_{\mathrm{BSE}}=100\) ns
   - \(T_{\mathrm{FF}}=40\) ns
   - \(T_{\mathrm{UESA}}=500\) ns

2. **Cycle closure**  
   \(T_{\mathrm{cycle}}\) measured at \(641\ \mathrm{ns}\) ±5%.

3. **Reset semantics**  
   Carrier purge is explicit and repeatable each cycle (no dependence on prior carrier survival).

4. **State handoff continuity**  
   Post-reset initialization at cycle \(k+1\) must use transferred state/correction payload from cycle \(k\).

5. **Coherence margin reporting**  
   Each experiment report includes \(T_2^*\), \(T_{\mathrm{active}}\), and \(\mathrm{CM}_t\).

6. **Minimum viability gate**  
   \(\mathrm{CM}_t \ge 1.0\) for baseline operating condition; otherwise flagged as non-viable at v0.2.

---

## 8) Data Requirements for Validation

Each recorded cycle should include:

- timestamp
- cycle index \(k\)
- measured phase durations (all four phases)
- environment metrics (temperature, humidity, vibration, EM noise)
- coherence proxy
- spin-exciton proxy
- handoff payload checksum or equivalent continuity marker
- anomaly/reset flags

---

## 9) Assumptions and Limitations

Assumptions:

- BSE inference and feed-forward packaging faithfully capture required state/correction information.
- Purge/reset does not erase externalized payload required for next-cycle reinstantiation.
- Room-temperature noise is stationary enough for repeated-cycle statistics.

Limitations:

- v0.2 does not prove fault-tolerant scaling.
- Proxy metrics may not fully represent logical fidelity without deeper tomography.
- Material/device nonlinearities may alter effective \(T_2^*\) under load.

---

## 10) Reproducibility Checklist

- Fixed hardware configuration per run
- Logged software/firmware version
- Constant sampling interval documented
- Explicit environment sensor calibration record
- Versioned analysis script/notebook references
- Archived raw data before processing

---

## 11) Change Log

- **v0.2**: Introduced teleportation-aligned state model, active-window coherence margin, and reset-positive cycle semantics.
