from kineticcsdetector import run_data_fetch

TRANGE = ["2017-01-28/09:09:00.1888", "2017-01-28/09:09:02.4419"]

rs, res = run_data_fetch(
    trange=TRANGE,
    probe=1,
    data_rate="brst",
    interp_policy="edge_hold",
    make_plot=True,
    save_npz=True,
    npz_path="mms_lmn_outputs_clean.npz",
    save_resolution_report=True,
    resolution_report_path="resolution_report.txt",
)
