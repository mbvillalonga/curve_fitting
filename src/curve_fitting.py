import pandas as pd
from scipy.optimize import curve_fit
from pathlib import Path
from curve_functions import linear, quadratic, cubic, quartic  # Import polynomial functions

def fit_curve(data_path, x_col, y_col, func):
    """
    Fits the specified function to the data.

    Parameters:
    - data_path (Path or str or pd.DataFrame): Path to the CSV file (or DataFrame) with x and y values
    - x_col (str): Column name for x values
    - y_col (str): Column name for y values
    - func (callable): The function to fit

    Returns:
    - pd.DataFrame: Dataframe with fitted parameters.
    """
    fitted_params = []

    # Load relevant pd.DataFrame or CSV file
    if isinstance(data_path, pd.DataFrame):
        df = data_path.copy()
    elif isinstance(data_path, (str, Path)):
        df = pd.read_csv(data_path)
    else:
        raise ValueError(f"Invalid data input type: {type(data_path)}. Expected a DataFrame or file path.")

    # Group by subject, posture condition, and g-level
    for (subj, g_level, posture), group in df.groupby(["subj_idx", "g_level_corrected", "bed_chair"]):
        x_data = group[x_col].values
        y_data = group[y_col].values

        try:
            params, _ = curve_fit(func, x_data, y_data)
            fitted_params.append([subj, g_level, posture] + list(params)) # add column with function name, and make sure GOF stats are here
        except RuntimeError:
            print(f"Curve fitting failed for subject {subj}, g-level {g_level}, posture condition {posture}")
    
    # Convert to DataFrame
    param_columns = ["subj_idx", "g_level_corrected", "bed_chair"] + [f"param_{i}" for i in range(len(params))]
    return pd.DataFrame(fitted_params, columns=param_columns)

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / "data" / "for_analysis" / "d_ml_trials_cleaned_allsubj.csv"
    output_dir = Path(__file__).resolve().parent.parent / "data" / "curve_fitting_output"
    output_dir.mkdir(exist_ok=True)

    func_to_fit = "linear"

    # Fit curves (change arguments as needed, depending on your IV, DV, and function)
    # Make sure your function is defined in curve_functions.py
    fitted_params_df = fit_curve(data_path, "turn_displacement", "indicated_displacement", linear)

    # Save fitted parameters
    fitted_params_df.to_csv(output_dir / f"fitted_parameters_{func_to_fit}.csv", index=False)
    print("Fitted parameters saved to:", output_dir / "fitted_parameters.csv")