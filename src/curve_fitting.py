import pandas as pd
from scipy.optimize import curve_fit
from pathlib import Path
from curve_functions import MODEL_FUNCTIONS  # Import all polynomial functions


def fit_curve(data, subj_to_keep, x_col, y_col, model_name, func):
    """
    Fits the specified function to the data.

    Parameters:
    - data (Path, str, or pd.DataFrame): Path to the CSV file with x and y values, or the DataFrame itself
    - subj_to_keep (list): List of subject IDs to include in the analysis
    - x_col (str): Column name for x values (independent variable)
    - y_col (str): Column name for y values (dependent variable)
    - model_name (str): Name of the model (function) to fit
    - func (callable): The formula of the function

    Returns:
    - pd.DataFrame: Dataframe with fitted parameters.
    """
    fitted_params = []

    # Load relevant pd.DataFrame or CSV file
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    elif isinstance(data, (str, Path)):
        df = pd.read_csv(data)
    else:
        raise ValueError(
            f"Invalid data input type: {type(data)}. Expected a DataFrame or file path."
        )

    # Ensure subj_to_keep is not None
    if subj_to_keep is not None:
        df = df[df["subj_idx"].isin(subj_to_keep)]
    else:
        print("⚠️ Warning: subj_to_keep is None. No filtering will be applied.")

    # Debugging: Print subjects in filtered dataset
    print(f"✅ Filtered dataset for curve fitting: {df.shape[0]} rows")
    print(f"Subjects included: {df['subj_idx'].unique()}")

    # Group by subject, posture condition, and g-level
    for (subj, g_level, posture), group in df.groupby(
        ["subj_idx", "g_level_corrected", "bed_chair"]
    ):
        x_data = group[x_col].values
        y_data = group[y_col].values

        try:
            params, _ = curve_fit(func, x_data, y_data)
        except RuntimeError:
            print(
                f"Curve fitting failed for subject {subj}, g-level {g_level}, posture condition {posture}"
            )
            params = []

        fitted_params.append(
            [subj, g_level, posture, model_name] + list(params)
        )  # add column with function name, and make sure GOF stats are here

    # Convert to DataFrame
    param_columns = ["subj_idx", "g_level_corrected", "bed_chair", "model"] + [
        f"param_{i}" for i in range(len(params))
    ]
    return pd.DataFrame(fitted_params, columns=param_columns)


if __name__ == "__main__":
    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "testing"
        / "for_analysis"
        / "d_ml_trials_cleaned_allsubj.csv"
    )
    output_dir = (
        Path(__file__).resolve().parent.parent / "data" / "testing" / "analysis_output"
    )
    output_dir.mkdir(exist_ok=True)

    # Load the dataset as a DataFrame
    df = pd.read_csv(data_path)

    all_fitted_params = []
    subj_to_keep = ["S1", "S2", "S3", "S4", "S5"]  # Sample data

    ## IF FITTING ALL FUNCTIONS IN CURVE_FUNCTIONS.PY:
    for model_name, func in MODEL_FUNCTIONS.items():
        print(f"Fitting {model_name} model...")
        fitted_params_df = fit_curve(
            df,
            subj_to_keep,
            "turn_displacement",
            "indicated_displacement",
            model_name,
            func,
        )
        all_fitted_params.append(fitted_params_df)

    # Concatenate all fitted parameters and save
    all_fitted_params_df = pd.concat(all_fitted_params, ignore_index=True)
    all_fitted_params_df.to_csv(
        output_dir / "fitted_parameters_all_models.csv", index=False
    )
    print(
        "All fitted parameters saved to: ",
        output_dir / "fitted_parameters_all_models.csv",
    )

    ### IF FITTING A SINGLE FUNCTION:
    ## Fit curves (change arguments as needed, depending on your IV, DV, and function)
    ## Make sure your function is defined in curve_functions.py
    # fitted_params_df = fit_curve(data_path, subj_to_keep, "turn_displacement", "indicated_displacement", linear)

    ## Save fitted parameters
    # fitted_params_df.to_csv(output_dir / f"fitted_parameters_{func_to_fit}.csv", index=False)
    # print("Fitted parameters saved to:", output_dir / "fitted_parameters.csv")
