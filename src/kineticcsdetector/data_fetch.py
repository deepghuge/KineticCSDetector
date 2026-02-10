# --- add at bottom of data_fetch.py ---

def run_data_fetch(
    trange,
    probe=1,
    data_rate="brst",
    interp_policy="edge_hold",
    drop_nan_rows=True,
    print_resolutions=True,
    make_plot=True,
    save_npz=True,
    npz_path="mms_lmn_outputs_clean.npz",
    save_resolution_report=True,
    resolution_report_path="resolution_report.txt",
    colors=None,
):
    """
    One-call pipeline:
      extract -> (optional) save npz -> (optional) save resolution report -> (optional) plot
    Returns:
      rs, resolutions
    """
    rs, resolutions = extract_lmn_for_trange(
        trange=trange,
        probe=probe,
        data_rate=data_rate,
        interp_policy=interp_policy,
        drop_nan_rows=drop_nan_rows,
        print_resolutions=print_resolutions,
    )

    if save_npz:
        np.savez(npz_path, **rs)
        print(f"✅ Saved: {npz_path}")

    if save_resolution_report:
        _write_resolution_report(resolutions, out_path=resolution_report_path)

    if make_plot:
        plot_stack(rs, trange, probe=probe, colors=colors)

    return rs, resolutions


def _main():
    import argparse

    parser = argparse.ArgumentParser(description="Run MMS data fetch + LMN feature extraction.")
    parser.add_argument("--start", required=True, help="Start time, e.g. 2017-01-28/09:09:00.1888")
    parser.add_argument("--end", required=True, help="End time, e.g. 2017-01-28/09:09:02.4419")
    parser.add_argument("--probe", type=int, default=1, choices=[1, 2, 3, 4])
    parser.add_argument("--data-rate", default="brst")
    parser.add_argument("--interp-policy", default="edge_hold", choices=["strict", "edge_hold", "linear_extrap"])
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--no-save", action="store_true")
    parser.add_argument("--npz-path", default="mms_lmn_outputs_clean.npz")
    parser.add_argument("--res-path", default="resolution_report.txt")

    args = parser.parse_args()

    run_data_fetch(
        trange=[args.start, args.end],
        probe=args.probe,
        data_rate=args.data_rate,
        interp_policy=args.interp_policy,
        make_plot=not args.no_plot,
        save_npz=not args.no_save,
        npz_path=args.npz_path,
        save_resolution_report=True,
        resolution_report_path=args.res_path,
    )


if __name__ == "__main__":
    _main()
