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

    # Compute per-subject and grand mean statistics

    # Output summary tables

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
