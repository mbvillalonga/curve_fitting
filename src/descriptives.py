import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def compute_descriptive_stats(data_path, variables, group_vars, output_dir):
    """
    Computes means and standard deviations for specified variables, grouped by given conditions.

    Parameters:
    - data_path (Path or str): Path to the CSV file with cleaned data
    - variables (list): List of variables to compute stats for
    - group_vars (list): Variables used for grouping (e.g. expected turn amplitude, posture condition, g-level)
    - output_dir (Path): Directory where descriptive summary stats will be saved.

    Returns:
    - subj_stats (pd.DataFrame): Per-subject mean and standard deviation, in each experimental condition.
    - grand_mean (pd.DataFrame): Grand mean statistics across all subjects.
    """

    # Load relevant CSV files
    df = pd.read_csv(data_path)

    missing_vars = [var for var in variables + group_vars + ["subj_idx"] if var not in df.columns]
    if missing_vars:
        raise ValueError(f"Missing columns in {data_path}: {missing_vars}")
    
    # Compute per-subject stats
    subj_stats = df.groupby(group_vars + ["subj_idx"])[variables].agg(['count','mean','std']).reset_index()

    # Compute grand mean across subjects
    subj_means = df.groupby(group_vars + ["subj_idx"])[variables].mean().reset_index()
    grand_mean = subj_stats.groupby(group_vars)[variables].agg['mean','std'].reset_index()

    # Output summary tables
    return subj_stats, grand_mean

def plot_subject_data(df, indep_vars, dep_vars, group_vars, output_dir):
    """
    Generates subject-level plots showing relationships among variables in different experimental conditions.

    Parameters:
    - df (pd.DataFrame): Data containing trial-level data for all subjects
    - indep_vars (list): List of independent variables (x-axis)
    - dep_vars (list): List of dependent variables to plot as a function of indep_var
    - group_vars (list): Grouping variables for faceting by condition
    - output_dir (Path): Directory where plots will be saved
    """

    # Load relevant CSV files 

    # Output summary plots
