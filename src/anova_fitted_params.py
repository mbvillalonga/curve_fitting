import pandas as pd
from statsmodels.stats.anova import AnovaRM
from pathlib import Path

# Define valid subjects (manually confirmed to have all conditions)
VALID_SUBJECTS = {"PD", "JRL", "AW", "BY", "IS"}

def run_anova(df, model_name):
    """
    Performed a repeated measures ANOVA (g_level_corrected x bed_chair)
    for all parameters in a given model.

    Parameters:
    - df (pd.Dataframe): Data containing fitted parameters
    - model_name (str): The model name to filter data for analysis

    Returns:
    - None (prints ANOVA results for each parameter)
    """

    # Filter the data for the selected model
    df_model = df[df["model"] == model_name]

    # Get all parameter columns
    param_cols = [col for col in df.columns if col.startswith("param_")]

    print(f"\n\nRunning repeated measures ANOVA for {model_name} model...")

    for param in param_cols:
        # Skip ANOVA if column contains NaN values
        if df_model[param].isna().any():
            print(f"Skipping {param} since it is not in the {model_name} model.")
            continue

        print(f"\nANOVA for {param}:")

        # Run repeated measures ANOVA
        aov = AnovaRM(df_model, depvar=param, subject="subj_idx", within=["g_level_corrected", "bed_chair"]).fit()

        # Print ANOVA results
        print(aov.summary())

if __name__ == "__main__":
    # Define paths
    params_path = Path(__file__).resolve().parent.parent / "data" / "curve_fitting_output" / "fitted_parameters_all_models.csv"

    # Load fitted parameters
    df = pd.read_csv(params_path)

    # Filter DataFrame to only analyze data from subjects with complete data
    df = df[df["subj_idx"].isin(VALID_SUBJECTS)]

    # Ask user for models to analyze
    available_models = df["model"].unique()
    print("\nAvailable models:", available_models)

    user_input = input("Enter models to analyze (comma-separated, for example: linear, quadratic): ").strip()
    selected_models = [m.strip() for m in user_input.split(",") if m.strip() in available_models]

    if not selected_models:
        print("No valid models selected. Exiting.")
    else:
        for model in selected_models:
            run_anova(df, model)