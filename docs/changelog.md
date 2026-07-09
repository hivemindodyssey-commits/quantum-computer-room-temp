# Changelog

All notable changes to this repository should be documented in this file.

This project tracks two parallel change streams:

1. **Code/Contract changes** (deterministic pipeline and interfaces)
2. **Experiment/Protocol changes** (Floquet subharmonic workflow, thresholds, safety rules)

---

## Status Legend

- ✅ **Implemented**
- 🧪 **Experimental**
- 🚧 **In Progress**
- 📋 **Planned**

---

## Change Types

Use these tags in entries:

- `CODE` — source code behavior changes
- `DOCS` — documentation-only updates
- `CONTRACT` — schema/interface/validation contract changes
- `PROTOCOL` — experiment workflow changes
- `THRESHOLD` — pass/fail/abort threshold changes
- `SAFETY` — abort handling, shutdown, recovery changes
- `CI` — workflow/check/pipeline behavior changes

---

## Versioning Guidance

Recommended version semantics:

- **MAJOR** (`vX.0.0`): breaking contract/protocol changes
- **MINOR** (`vX.Y.0`): backward-compatible features or new protocol sections
- **PATCH** (`vX.Y.Z`): fixes, clarifications, non-breaking adjustments

If a threshold changes experimental interpretation, bump at least **MINOR** and include rationale.

---

## [Unreleased]

### Added
- _None yet_

### Changed
- _None yet_

### Fixed
- _None yet_

### Deprecated
- _None yet_

### Removed
- _None yet_

---

## [v2.0.0] - 2026-07-09

### Added
- [DOCS] Introduced v2 documentation suite and hub references.
- [CONTRACT] Established contract-first flow:
  - `docs/schema_v2.md`
  - `docs/summary_contract_v2.md`
  - `docs/template_interface_v2.md`
  - `docs/renderer_validation_v2.md`
- [CODE] Deterministic summary extraction workflow centered on `src/auto_fill_physics_summary.py`.

### Changed
- [DOCS] README reorganized around:
  - implemented deterministic pipeline
  - experimental research track
  - explicit scientific status note
- [DOCS] Added canonical status system:
  - ✅ Implemented
  - 🧪 Experimental
  - 🚧 In Progress
  - 📋 Planned

### Notes
- v2.0.0 is the baseline for future protocol and threshold deltas.

---

## Protocol Revision Log

> Record experiment workflow changes here, even if code has not yet changed.

| Date (UTC) | Protocol Version | Status | Change Summary | Rationale | Related Files | Author |
|---|---|---|---|---|---|---|
| 2026-07-09 | p2.0.0 | 🧪 Experimental | Established baseline Floquet/subharmonic protocol framing in docs. | Normalize experiment language and expected metrics. | `docs/experiments/subharmonic_validation_protocol.md` | maintainer |

---

## Threshold Change Log

> Every threshold update must include justification and expected impact.

| Date (UTC) | Parameter | Old Value | New Value | Scope | Reason | Validation Plan | Status |
|---|---|---:|---:|---|---|---|---|
| 2026-07-09 | `SNR_pass` | — | `8 dB` | Subharmonic pass criteria | Initial baseline definition | Validate across baseline + sweep runs | 🧪 Experimental |
| 2026-07-09 | `sigma_phi_pass` | — | `0.3` | Phase stability pass criteria | Initial baseline definition | Compare variance stability over repeated segments | 🧪 Experimental |
| 2026-07-09 | `sigma_phi_abort` | — | `0.5` | Abort logic | Initial safety guardrail | Confirm abort behavior under induced instability | 🧪 Experimental |
| 2026-07-09 | `lifetime_abort` | — | `0.8 × baseline` | Abort logic | Prevent operation during Q/lifetime collapse | Validate with controlled degradation scenarios | 🧪 Experimental |

---

## Contract Change Log

> Track schema/interface compatibility here.

| Date (UTC) | Contract | Change Type | Backward Compatible | Summary | Migration Required | Status |
|---|---|---|---|---|---|---|
| 2026-07-09 | `schema_v2` | Initial | Yes | Baseline input contract for run ingestion. | No | ✅ Implemented |
| 2026-07-09 | `summary_contract_v2` | Initial | Yes | Baseline output summary payload contract. | No | ✅ Implemented |
| 2026-07-09 | `template_interface_v2` | Initial | Yes | Template rendering interface contract. | No | ✅ Implemented |
| 2026-07-09 | `renderer_validation_v2` | Initial | Yes | Renderer and drift-gate validation rules. | No | ✅ Implemented |

---

## Safety/SOP Change Log

| Date (UTC) | Area | Change | Trigger Conditions Affected | Operational Impact | Status |
|---|---|---|---|---|---|
| 2026-07-09 | Abort/SOP | Baseline emergency SOP documented (abort → shutdown → cooldown → resume checks). | `sigma_phi_abort`, `lifetime_abort`, leakage thresholds | Defines minimum safe response path for unstable runs. | 🧪 Experimental |

---

## CI Change Log

| Date (UTC) | Workflow/File | Change Summary | Breaking | Status |
|---|---|---|---|---|
| 2026-07-09 | `ci.yml` (badge-linked workflow) | CI framing aligned to schema → summary → template → renderer validation path. | No | ✅ Implemented |

---

## Entry Template (Copy/Paste)

Use this template for new release entries:

```markdown
## [vX.Y.Z] - YYYY-MM-DD

### Added
- [TYPE] ...

### Changed
- [TYPE] ...

### Fixed
- [TYPE] ...

### Deprecated
- [TYPE] ...

### Removed
- [TYPE] ...

### Migration Notes
- Required actions (if any)
```

Use this template for threshold updates:

```markdown
| YYYY-MM-DD | `parameter_name` | old | new | scope | reason | validation plan | status |
```

Use this template for protocol updates:

```markdown
| YYYY-MM-DD | pX.Y.Z | status | what changed | why | related files | author |
```

---

## Governance Rules

1. **No silent threshold changes**: any threshold adjustment must appear in this file before/with merge.
2. **Contract edits require compatibility note**: explicitly mark migration need.
3. **Protocol edits must include rationale**: why the change improves reliability/validity/safety.
4. **Release tags should map to this file**: each release must have a dated entry.

---

## Links

- README: [`README.md`](../README.md)
- Roadmap: [`docs/roadmap.md`](roadmap.md)
- v2 docs hub: [`docs/v2_index.md`](v2_index.md)
