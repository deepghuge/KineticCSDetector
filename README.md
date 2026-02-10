# KineticCSDetector
CNN pipeline trained on SheetGen synthetic current-sheet events to scan space-plasma time series and flag candidate small kinetic-scale current-sheet intervals. Outputs ranked time windows for targeted physics follow-up, reducing manual search across large datasets.
## data-fetch

This module handles data ingestion and preprocessing for **KineticCSDetector**.

### What it does
- Downloads/loads MMS burst-mode plasma and field data (FPI, FGM, EDP)
- Cleans and validates time-series streams
- Interpolates multi-cadence signals with configurable edge policy
- Builds LMN coordinates (MVA/HMVA)
- Computes physics features:
  - current density `J = e(ni*Vi - ne*Ve)`
  - `|J|`
  - electron-frame `E·J` proxy
- Exports clean arrays for downstream detection and ML workflows

### Inputs
- Time range (`trange`)
- Probe ID
- Data rate / interpolation policy

### Outputs
- LMN magnetic components
- LMN ion/electron velocity
- LMN current components + `|J|`
- `E·J`
- Resolution/cadence report
