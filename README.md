# KineticCSDetector ( Work In Progress)
CNN pipeline trained on SheetGen synthetic current-sheet events to scan space-plasma time series and flag candidate small kinetic-scale current-sheet intervals. Outputs ranked time windows for targeted physics follow-up, reducing manual search across large datasets.

# utils/data-fetch.ipynb (will be turned into a  module )

`utils/data-fetch.ipynb` is the current **notebook-based** data ingestion and preprocessing workflow for **KineticCSDetector**.

It pulls MMS burst-mode measurements, cleans and aligns multi-cadence streams, transforms vectors to LMN, and generates physics-informed features used for kinetic current-sheet analysis and ML-ready exports.

## What this notebook does

- Fetches MMS burst data for a user-defined time range:
  - **FPI** (electron/ion density, bulk velocity)
  - **FGM** (magnetic field)
  - **EDP** (electric field)
- Cleans time series (NaNs, duplicate timestamps, sorting)
- Aligns multi-rate signals with configurable interpolation policy:
  - `strict` (NaN outside source range)
  - `edge_hold` (hold boundary values)
  - `linear_extrap` (linear extrapolation outside range)
- Computes LMN coordinates (HMVA with MVA fallback)
- Computes key physics features:
  - `J = e (ni*Vi - ne*Ve)`
  - `|J|`
  - `E·J` using electron-frame corrected electric field
- Prints and saves cadence/resolution diagnostics
- Generates a 6-panel stack plot for quick event inspection

---

## Inputs

- `trange`: MMS-format start/end time, e.g.  
  `["2017-01-28/09:09:00.1888", "2017-01-28/09:09:02.4419"]`
- `probe`: spacecraft ID (`1..4`)
- `data_rate`: usually `brst`
- `interp_policy`: `strict`, `edge_hold`, `linear_extrap`

---

## Outputs

Notebook returns/exports arrays for downstream analysis:

- `time_B` (native magnetic timeline)
- `time_ref` (reference timeline, typically electron-velocity cadence)
- `BL, BM, BN`
- `VeL, VeM, VeN`
- `ViL, ViM, ViN`
- `JL, JM, JN, J_mag`
- `E_dot_J`

Saved artifacts:
- `mms_lmn_outputs_clean.npz`
- `resolution_report.txt`

---

## Quick start (Notebook)

1. Open `utils/data-fetch.ipynb`
2. Set:
   - `TRANGE`
   - `PROBE`
   - `interp_policy`
3. Run all cells in order
4. Inspect stack plots and exported files

Example config:

```python
TRANGE = ["2017-01-28/09:09:00.1888", "2017-01-28/09:09:02.4419"]
PROBE = 1
INTERP_POLICY = "edge_hold"  # strict / edge_hold / linear_extrap
