import os
import sys
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from src.descriptives import compute_descriptive_stats
from src.curve_functions import MODEL_FUNCTIONS
from src.curve_fitting import fit_curve
from src.curve_fit_goodness import compute_gof, plot_goodness_of_fit
from src.anova_fitted_params import run_anova, plot_anova_results

# Load .env 
load_dotenv("analysis_config.env")

# Fixed cleaned data directory and files (users should not change these)
data_dir_cleaned = Path(os.getenv("DATA_DIR_CLEANED")).resolve()
d_ml_file = data_dir_cleaned / "d_ml_trials_cleaned_allsubj.csv"
v_r_file = data_dir_cleaned / "v_r_trials_cleaned_allsubj.csv"

# Validate above directories and files
print("TESTING: Validating directories and files...") # for testing
if not data_dir_cleaned.exists():
    sys.exit(f"***ERROR*** Data directory not found: {data_dir_cleaned}")

if not d_ml_file.exists():
    sys.exit(f"***ERROR*** Missing dataset: {d_ml_file}")

if not v_r_file.exists():
    sys.exit(f"***ERROR*** Missing dataset: {v_r_file}")

# Results directory (see analysis_config.env to modify)
results_dir = Path(os.getenv("RESULTS_DIR")).resolve()
results_dir.mkdir(parents=True, exist_ok=True)

# Load other settings from .env
run_data_processing = os.getenv("RUN_DATA_PROCESSING", "False").lower() == "true"
x_var = os.getenv("X_VAR").strip()
group_vars = [var.strip() for var in os.getenv("GROUP_VARS").split(",")]
dep_vars = [var.strip() for var in os.getenv("DEP_VARS").split(",")]
curve_functions = [var.strip() for var in os.getenv("CURVE_FUNCTIONS").split(",")]

# Debugging: Print loaded settings
print(f"\nTESTING: Settings Loaded from .env:")
print(f"  - X Variable: {x_var}")
print(f"  - Grouping Variables: {group_vars}")
print(f"  - Dependent Variables: {dep_vars}")
print(f"  - Curve Functions: {curve_functions}")
print(f"  - Results Directory: {results_dir}")

# Run data processing only if enabled
if run_data_processing:
    print("\n- Running data processing step...")
#REMOVE AFTER DEBUG    os.system("python src/data_processing.py") # runs src/data_processing.py as subprocess
    print("Data processing complete.")

# Define which dataset each dependent variable (DV) belongs to
v_r_vars = {"vertical_indicated_error", "tilt_indicated_error"}
d_ml_vars = {
    "turn_bed_displacement", "indicated_displacement", "indicated_displacement_error", 
    "turn_end_joystick_position", "midline_indicated_angle", "turn_rms_track_error"
}

# Run analysis for each DV
for dep_var in dep_vars:
    print(f"\n- Processing dependent variable: {dep_var}")

    # Determine which dataset to use
    if dep_var in v_r_vars:
        dataset_file = v_r_file
    elif dep_var in d_ml_vars:
        dataset_file = d_ml_file
    else:
        print(f"***WARNING*** Dependent variable {dep_var} not recognized. Skipping.")
        continue

    # Validate dataset file existence before reading
    if not dataset_file.exists():
        print(f"***ERROR*** Expected dataset file missing: {dataset_file}")
        continue

    # Create a subfolder for this DV inside results_dir
    dep_var_res_dir = results_dir / dep_var
    dep_var_res_dir.mkdir(parents=True, exist_ok=True)

    # Load dataset
    print(f"TESTING: Loading data set: {dataset_file}") # for testing
    df = pd.read_csv(dataset_file)
    print(f"TESTING: Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns.") # for testing

    # Compute descriptive statistics (src/descriptives.py)
    print(f"- Computing descriptive statistics for {dep_var}...")
#REMOVE AFTER DEBUG    subj_stats, grand_mean = compute_descriptive_stats(df, [dep_var], group_vars, dep_var_res_dir)
#REMOVE AFTER DEBUG    subj_stats.to_csv(dep_var_res_dir / f"subj_stats_{dep_var}.csv", index=False)
#REMOVE AFTER DEBUG    grand_mean.to_csv(dep_var_res_dir / f"grand_means_{dep_var}.csv", index=False)
    # TO DO: check descriptives module for success message

    # Perform curve fitting (src/curve_fitting.py)
    print(f"- Performing curve fitting for {dep_var}...")
    fitted_params_list = []
    for model_name in curve_functions:
        if model_name in MODEL_FUNCTIONS:
            print(MODEL_FUNCTIONS[model_name]) # for testing
#REMOVE AFTER DEBUG            fitted_params_df = fit_curve(df, x_var, dep_var, model_name, MODEL_FUNCTIONS[model_name])
#REMOVE AFTER DEBUG            fitted_params_list.append(fitted_params_df)
        else:
            print(f"***WARNING*** {model_name} not found in src/curve_functions.py. Skipping.")
    # TO DO: check curve fitting module for success message

    # Save curve fitting results
#REMOVE AFTER DEBUG    all_fitted_params = pd.concat(fitted_params_list, ignore_index=True)
#REMOVE AFTER DEBUG    all_fitted_params.to_csv(dep_var_res_dir / f"fitted_parameters_{dep_var}.csv", index=False)
    # TO DO: check curve fitting module for success message

    # Compute goodness-of-fit and generate figures
    print(f"- Computing goodness-of-fit for {dep_var}...")
    gof_res = []
#REMOVE AFTER DEBUG    for model_name in curve_functions:
#REMOVE AFTER DEBUG        gof_df = compute_gof(df, x_var, dep_var, model_name, curve_functions[model_name], all_fitted_params)
#REMOVE AFTER DEBUG        gof_res.append(gof_df)
    
#REMOVE AFTER DEBUG    all_gof = pd.concat(gof_res, ignore_index=True)
#REMOVE AFTER DEBUG    all_gof.to_csv(dep_var_res_dir / f"goodness_of_fit_{dep_var}.csv", index=False)
#REMOVE AFTER DEBUG    plot_goodness_of_fit(all_gof, dep_var, results_dir)
    # TO DO: check gof module for success message

    # Perform ANOVAs and generate figures showing group mean of each model parameter by condition, 
    # corresponding to ANOVA results
    print(f"- Running ANOVAs and generating figures for each model's parameters, {dep_var}...")
#REMOVE AFTER DEBUG    for model in curve_functions:
#REMOVE AFTER DEBUG        anova_res = run_anova(all_fitted_params, model)
#REMOVE AFTER DEBUG        anova_res.to_csv(dep_var_res_dir / f"anova_results_{dep_var}_{model}.csv")
#REMOVE AFTER DEBUG        plot_anova_results(df, model, anova_res, dep_var_res_dir)
    # TO DO: check anova module for success message

print("\nAnalysis complete. Results saved in: ", results_dir)
