# KineticCSDetector
CNN pipeline trained on SheetGen synthetic current-sheet events to scan space-plasma time series and flag candidate small kinetic-scale current-sheet intervals. Outputs ranked time windows for targeted physics follow-up, reducing manual search across large datasets.

# data-fetch 

`data-fetch` is the ingestion and preprocessing engine for **KineticCSDetector**.  
It pulls burst-mode MMS measurements, cleans and aligns multi-cadence streams, transforms vectors to LMN, and generates physics-informed features used downstream for kinetic current-sheet detection.

## What this module does

- Fetches MMS burst data for a user-specified time range:
  - **FPI** (density, ion/electron bulk velocity)
  - **FGM** (magnetic field)
  - **EDP** (electric field)
- Cleans time series (NaNs, duplicate timestamps, sorting)
- Handles multi-rate alignment with configurable interpolation policy:
  - `strict` (NaN outside range)
  - `edge_hold` (hold edge values outside range)
  - `linear_extrap` (full extrapolation)
- Computes LMN coordinates (HMVA/MVA fallback)
- Computes core physics features:
  - \(\mathbf{J}=e(n_i\mathbf{V}_i-n_e\mathbf{V}_e)\)
  - \(|\mathbf{J}|\)
  - \(E\cdot J\) using electron-frame corrected field
- Prints and saves cadence/resolution diagnostics

---

## Inputs

- `trange`: start/end timestamps (MMS format), e.g.
  `["2017-01-28/09:09:00.1888", "2017-01-28/09:09:02.4419"]`
- `probe`: MMS spacecraft ID (`1..4`)
- `data_rate`: typically `brst`
- `interp_policy`: `strict`, `edge_hold`, or `linear_extrap`

---

## Outputs

The extraction returns arrays ready for analysis/ML:

- `time_B` (FGM/native B timeline)
- `time_ref` (reference timeline, usually electron velocity cadence)
- `BL, BM, BN`
- `VeL, VeM, VeN`
- `ViL, ViM, ViN`
- `JL, JM, JN, J_mag`
- `E_dot_J`

Saved artifacts:
- `mms_lmn_outputs_clean.npz`
- `resolution_report.txt`

---

## Quick start

```python
TRANGE = ["2017-01-28/09:09:00.1888", "2017-01-28/09:09:02.4419"]
PROBE = 1

rs, res = extract_lmn_for_trange(
    trange=TRANGE,
    probe=PROBE,
    data_rate="brst",
    interp_policy="edge_hold",
    drop_nan_rows=True,
    print_resolutions=True
)

np.savez("mms_lmn_outputs_clean.npz", **rs)
_write_resolution_report(res, out_path="resolution_report.txt")
plot_stack(rs, TRANGE, probe=PROBE)
