import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from descriptives import compute_descriptive_stats
from curve_fitting import fit_curve
from curve_fit_goodness import compute_gof, plot_goodness_of_fit
from anova_fitted_params import run_anova, plot_anova_results
from curve_functions import MODEL_FUNCTIONS

# Load .env 
load_dotenv("analysis_config.env")

# Fixed cleaned data directory and files (users should not change these)
data_dir_cleaned = Path(os.getenv("DATA_DIR_CLEANED")).resolve()
d_ml_file = data_dir_cleaned / "d_ml_trials_cleaned_allsubj.csv"
v_r_file = data_dir_cleaned / "v_r_trials_cleaned_allsubj.csv"

# Validate above directories and files
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

# Run data processing only if enabled
if run_data_processing:
    print("\n- Running data processing step...")
    os.system("python data_processing.py") # runs src/data_processing.py as subprocess
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

    # Create a subfolder for this DV inside results_dir
    dep_var_res_dir = results_dir / dep_var
    dep_var_res_dir.mkdir(parents=True, exist_ok=True)

    # Load dataset
    #df = pd.read_csv(dataset_file)
    print(f"This is when the script would read in the csv: {dataset_file}") # for testing

    # Compute descriptive statistics
    print(f"- Computing descriptive statistics for {dep_var}...")