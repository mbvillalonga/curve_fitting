import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from curve_functions import MODEL_FUNCTIONS  # Import models

def plot_curve_fits(raw_df, res_df, x_var, dep_var, output_dir, plot_curves=False):
    """
    Generate 6-panel plots of fitted curves over raw data points for each subject and model.

    Parameters:
    - raw_df: Trial-level data for all subjects, all conditions, used for fit_curve()
    - res_df: DataFrame with fitted model paramters (output from fit_curve())
    - x_var: Independent variable name
    - dep_var: Dependent variable name
    - output_dir: Directory where figures will be saved
    - plot_curves: Boolean flag to enable plotting
    """
    if not plot_curves:
        return
    
    subjects = res_df['subj_idx'].unique()

    # Identify parameter columns dynamically
    param_columns = [col for col in res_df.columns if col.startswith("param_")]
    if not param_columns:
        raise KeyError("Could not find any parameter columns (e.g., 'param_0', 'param_1') in res_df")
    
    for subj_idx in subjects:
        for model_name, model_func in MODEL_FUNCTIONS.items():

            if not res_df['model'].str.lower().str.contains(model_name.lower()).any():
                continue

            subj_data = res_df[(res_df['subj_idx'] == subj_idx) & (res_df['model'].str.lower() == model_name.lower())]

            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 12), sharey=True)
            axes = axes.flatten()

            col_titles = ['Bed', 'Chair']
            row_titles = ['0G', '1G', '1.8G']

            for i, (g_level_corrected, bed_chair) in enumerate(
                [(0.0, 'V'), (0.0, 'R'),
                (1.0, 'V'), (1.0, 'R'),
                (1.8, 'V'), (1.8, 'R')]):
                ax = axes[i]
                group_data = raw_df[(raw_df['g_level_corrected'] == g_level_corrected) &
                                    (raw_df['bed_chair'] == bed_chair) &
                                    (raw_df['subj_idx'] == subj_idx)]
                
                if group_data.empty:
                    ax.set_title(f"No Data ({g_level_corrected}G, {bed_chair})")
                    continue

                x = group_data[x_var]
                y = group_data[dep_var]

                curve_data = subj_data[(subj_data['g_level_corrected'] == g_level_corrected) &
                                        (subj_data['bed_chair'] == bed_chair)]
                
                if not curve_data.empty:
                    params = curve_data[param_columns].dropna(axis=1).values.flatten()

                    ax.scatter(x, y, label='Data', alpha=0.7)
                    x_smooth = np.linspace(x.min(), x.max(), 500)
                    ax.plot(x_smooth, model_func(x_smooth, *params), label=f'{model_name.capitalize()} Fit')
                    ax.legend()
                
                if i % 2 == 1:
                    ax_right = ax.twinx()
                    ax_right.set_ylabel(f"{row_titles[i // 2]}", rotation=270, labelpad=20, fontsize=14, fontweight='bold')
                    ax_right.set_yticks([])
                if i < 2:
                    ax.set_title(col_titles[i % 2], fontsize=14, fontweight='bold')
                
                ax.set_xlabel('Tilt Amplitude (deg)')
                ax.set_ylabel(f"{dep_var} (deg)")

            fig.tight_layout()
            filename = f"{dep_var}_subj_{subj_idx}_{model_name}_fits.pdf"
            plt.suptitle(f"{dep_var} - Subject {subj_idx}\n{model_name.capitalize()} Fits", fontsize=16, fontweight='bold')
            plt.subplots_adjust(top=0.9)
            plt.savefig(os.path.join(output_dir, filename))
            plt.close(fig)

if __name__ == "__main__":

    # Load data and arguments for testing function
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot-curves", action="store_true", help="Enable curve fitting visualization")
    parser.add_argument("--data-file", type=str, required=True, help="Path to the raw data file")
    parser.add_argument("--results-file", type=str, required=True, help="Path to the curve fitting results file")
    parser.add_argument("--x-var", type=str, required=True, help="Independent variable name")
    parser.add_argument("--dep-var", type=str, required=True, help="Dependent variable name")
    parser.add_argument("--output-dir", type=str, required=True, help="Directory where figures will be saved")
    args = parser.parse_args()
    
    # Convert output dir str to Path and ensure it exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data files
    df = pd.read_csv(args.data_file)
    res_df = pd.read_csv(args.results_file)
    

    plot_curve_fits(df, res_df, args.x_var, args.dep_var, args.output_dir, plot_curves=args.plot_curves)