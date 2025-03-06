import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from curve_functions import MODEL_FUNCTIONS  # Import models

def compute_gof(data, x_col, y_col, model_name, func, fitted_params):
    """
    Computes goodness of fit (GOF) statistics R^2 and RMSE for each fitted model.

    Parameters:
    - data (Path, str, or pd.DataFrame): Data with original x and y values.
    - x_col (str): Column name for x values (independent variable)
    - y_col (str): Column name for y values (dependent variable)
    - model_name (str): Name of the model being evaluated
    - func (callable): The function used for fitting
    - fitted_params (pd.DataFrame): Fitted parameters DataFrame

    Returns:
    - pd.DataFrame: DataFrame with R^2 and RMSE for each model, subject, and condition
    """
    results = []

    for _, row in fitted_params.iterrows():
        subj, g_level, posture, model = row["subj_idx"], row["g_level_corrected"], row["bed_chair"], row["model"]
        params = row.iloc[4:].values # Extract model parameters; make this adaptive in case of custom functions

        # Get subject-specific  data
        subj_df = df[(df["subj_idx"] == subj) & 
                    (df["g_level_corrected"] == g_level) & 
                    (df["bed_chair"] == posture)]
        x_data = subj_df[x_col].values
        y_true = subj_df[y_col].values
        y_pred = func(x_data, *params[:func.__code__.co_argcount - 1])

        # Compute R^2
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # Compute RMSE
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

        results.append([subj, g_level, posture, model, r_squared, rmse])

    return pd.DataFrame(results, columns=["subj_idx", "g_level_corrected", "bed_chair", "model", "R_squared", "RMSE"])

def plot_goodness_of_fit(df, dep_var, output_dir):
    """
    Generates comparison plots for goodness-of-fit statistics, considering different conditions.

    Parameters:
    - df (pd.DataFrame): Data containing R^2 and RMSE values for all models.
    - dep_var (str): Name of dependent variable
    - output_dir (Path): Directory to save plots.
    """

    output_dir.mkdir(exist_ok=True)  # Ensure output directory exists

    # Boxplot for R^2 across models, grouped by gravity level and posture
    plt.figure(figsize=(12, 6))
    sns.catplot(
        data=df, x="model", y="R_squared", hue="g_level_corrected", col="bed_chair",
        kind="box", palette="viridis", height=6, aspect=1.2
    )
    plt.xlabel("Model")
    plt.ylabel("R^2")
    plt.suptitle("Comparison of R^2 Across Models, Grouped by Condition")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "r_squared_comparison_by_condition.png")
    plt.close()

    # Boxplot for RMSE across models, grouped by gravity level and posture
    plt.figure(figsize=(12, 6))
    sns.catplot(
        data=df, x="model", y="RMSE", hue="g_level_corrected", col="bed_chair",
        kind="box", palette="magma", height=6, aspect=1.2
    )
    plt.xlabel("Model")
    plt.ylabel("RMSE")
    plt.suptitle("Comparison of RMSE Across Models, Grouped by Condition")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / f"rmse_comparison_by_condition_{dep_var}.png")
    plt.close()

    print("Model comparison plots saved to:", {output_dir})

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / "data" / "for_analysis" / "d_ml_trials_cleaned_allsubj.csv"
    params_path = Path(__file__).resolve().parent.parent / "data" / "curve_fitting_output" / "fitted_parameters_all_models.csv"
    output_dir = Path(__file__).resolve().parent.parent / "data" / "curve_fitting_output"
    output_dir.mkdir(exist_ok=True)

    df = pd.read_csv(data_path)
    fitted_params = pd.read_csv(params_path)

    all_goodness_of_fit = []

    for model_name, func in MODEL_FUNCTIONS.items():
        print(f"Evaluating {model_name} model goodness of fit...")
        model_params = fitted_params[fitted_params["model"] == model_name]
        model_fit_df = compute_gof(df, "turn_displacement", "indicated_displacement", model_name, func, model_params)
        all_goodness_of_fit.append(model_fit_df)

    all_goodness_df = pd.concat(all_goodness_of_fit, ignore_index=True)
    all_goodness_df.to_csv(output_dir / "goodness_of_fit_all_models.csv", index=False)
    print("Goodness-of-fit results saved to: ", output_dir / "goodness_of_fit_all_models.csv")

    # Generate visualization
    plot_goodness_of_fit(all_goodness_df, output_dir)
