import pandas as pd
from pathlib import Path

def compute_descriptive_stats(data_path, variables, group_vars, output_dir):
    """
    Computes means and standard deviations for specified variables, grouped by given conditions.

    Parameters:
    - data_path (Path or str or pd.DataFrame): Path to the CSV file (or DataFrame) with cleaned data
    - variables (list): List of variables to compute stats for
    - group_vars (list): Variables used for grouping (e.g. expected turn amplitude, posture condition, g-level)
    - output_dir (Path): Directory where descriptive summary stats will be saved.

    Returns:
    - subj_stats (pd.DataFrame): Per-subject mean and standard deviation, in each experimental condition.
    - grand_mean (pd.DataFrame): Grand mean statistics across all subjects.
    """

    # Make sure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load relevant DataFrame or CSV files
    if isinstance(data_path, pd.DataFrame):
        df = data_path.copy()
    elif isinstance(data_path, (str, Path)):
        df = pd.read_csv(data_path)
    else:
        raise ValueError(f"Invalid data input type: {type(data_path)}. Expected a DataFrame or file path.")

    missing_vars = [var for var in variables + group_vars + ["subj_idx"] if var not in df.columns]
    if missing_vars:
        raise ValueError(f"Missing columns in {data_path}: {missing_vars}")
    
    # Compute per-subject stats
    subj_stats = df.groupby(group_vars + ["subj_idx"])[variables].agg(['count','mean','std']).reset_index()
    subj_stats.columns = ['_'.join(col).strip('_') for col in subj_stats.columns]

    # Compute grand mean across subjects
    subj_means = df.groupby(group_vars + ["subj_idx"])[variables].mean().reset_index()
    grand_mean = subj_means.groupby(group_vars)[variables].agg(['mean','std']).reset_index()
    # Flatten MultiIndex for grand_mean
    grand_mean.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in grand_mean.columns]

    # Output summary tables
    return subj_stats, grand_mean

# Runs if script is executed directly, not when imported
if __name__ == "__main__":
    # Define dataset for paths and variables
    data_dir = Path(__file__).resolve().parent.parent / "data" / "for_analysis"

    output_dir = data_dir.parent / "summary_stats_2025"
    output_dir.mkdir(parents=True, exist_ok=True)

    d_ml_file = data_dir / "d_ml_trials_cleaned_allsubj.csv"
    v_r_file = data_dir / "v_r_trials_cleaned_allsubj.csv"

    d_ml_dvs = [
        "turn_bed_displacement", "indicated_displacement", "indicated_displacement_error",
        "turn_end_joystick_position", "midline_indicated_angle", "turn_rms_track_error"
        ]

    v_r_dvs = ["vertical_indicated_error", "tilt_indicated_error"]

    group_vars = ["turn_displacement", "bed_chair", "g_level_corrected"]

    # Compute statistics
    d_ml_stats, d_ml_grand_mean = compute_descriptive_stats(d_ml_file, d_ml_dvs, group_vars, output_dir)
    v_r_stats, v_r_grand_mean = compute_descriptive_stats(v_r_file, v_r_dvs, group_vars, output_dir)

    # Save statistics
    d_ml_stats.to_csv(output_dir / "d_ml_subj_stats.csv", index=False)
    d_ml_grand_mean.to_csv(output_dir / "d_ml_grand_means.csv", index=False)
    print("Descriptive statistics for DISPLACEMENT and MIDLINE dependent variables computed and saved.")

    v_r_stats.to_csv(output_dir / "v_r_subj_stats.csv", index=False)
    v_r_grand_mean.to_csv(output_dir / "v_r_grand_means.csv", index=False)
    print("Descriptive statistics for VERTICAL/REAR dependent variables computed and saved.")