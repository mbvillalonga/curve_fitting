import pandas as pd
from statsmodels.stats.anova import AnovaRM
from pathlib import Path

def run_anova(df, model_name):
    """
    Performed a repeated measures ANOVA (g_level_corrected x bed_chair)
    for all parameters in a given model.

    Parameters:
    - df (pd.Dataframe): Data containing fitted parameters
    - model_name (str): The model name to filter data for analysis

    Returns:
    - dict: Dictionary with ANOVA results for each parameter
    """

    # Filter the data for the selected model
    df_model = df[df["model"] == model_name]

    # Get all parameter columns
    param_cols = [col for col in df.columns if col.startswith("param_")]

    print(f"\n\nRunning repeated measures ANOVA for {model_name} model...")

    anova_results = {}

    for param in param_cols:
        # Skip ANOVA if column contains NaN values
        if df_model[param].isna().any():
            print(f"Skipping {param} since it is not in the {model_name} model.")
            continue

        print(f"\nANOVA for {param}:")

        # Run repeated measures ANOVA
        aov = AnovaRM(df_model, depvar=param, subject="subj_idx", within=["g_level_corrected", "bed_chair"]).fit()

        # Store and print ANOVA results
        anova_results[param] = aov.anova_table
        print(aov.summary())

    return anova_results

def plot_anova_results(df, model_name, anova_results, output_dir):
    """
    Generates dot plots for each parameter, showing group means by condition, +/- 1SD.
    Adds annotations for significant effects (p < .05).

    Parameters:
    - df (pd.DataFrame): Data containing fitted parameters
    - model_name (str): Model name for filtering data
    - anova_results (dict): Dictionary containing ANOVA results and p-values
    - output_dir (Path): Directory where plots will be saved
    """
    import matplotlib.pyplot as plt

    plt.rcParams.update(plt.rcParamsDefault)  # ✅ Resets all settings
    plt.style.use("default")  # ✅ Ensures consistent style
    output_dir.mkdir(exist_ok=True) # Ensure output directory exists

    # Filter dataset for the selected model
    df_model = df[df["model"] == model_name]

    # Get all parameter columns
    param_cols = [col for col in df_model.columns if col.startswith("param_")]

    # Capitalize model name for title
    model_name_cap = model_name.capitalize()
    
    # Define color mapping for bed_chair conditions
    color_mapping = {"V": "orange", "R": "blue"}
    label_mapping = {"V": "Bed", "R": "Chair"}  # Renaming for legend

    for param in param_cols:
        if df_model[param].isna().any():
            continue # Skip parameters with missing values

        # Compute group means and standard deviations
        summary = df_model.groupby(["g_level_corrected", "bed_chair"])[param].agg(["mean","std"]).reset_index()
        
        # Convert g_level_corrected to categorical for proper ordering
        summary["g_level_corrected"] = summary["g_level_corrected"].astype(str)

        # Initialize plot
        plt.figure(figsize=(8, 6))

        # Create scatter plot for means with dodge effect
        dodge_offset = 0.1  # Adjust separation between bed_chair conditions
        category_order = sorted(summary["g_level_corrected"].unique())  # Ensure correct x-axis order

        x_positions = []
        legend_handles = [] 

        for i, g_level in enumerate(category_order):
            for bed_chair in ["V", "R"]:  # Ensure consistent order
                subset = summary[(summary["g_level_corrected"] == g_level) & (summary["bed_chair"] == bed_chair)]
                if not subset.empty:
                    x_actual = i + (dodge_offset if bed_chair == "V" else -dodge_offset)
                    x_positions.append((x_actual, subset["mean"].values[0], subset["std"].values[0], bed_chair))
                    # Create scatter points and store legend handles
                    scatter = plt.scatter(x_actual, subset["mean"], label=label_mapping[bed_chair],
                                        s=100, edgecolor="black", color=color_mapping[bed_chair])
                    if label_mapping[bed_chair] not in [h.get_label() for h in legend_handles]:
                        legend_handles.append(scatter)

        # Add error bars
        for x_actual, mean_val, std_val, bed_chair in x_positions:
            plt.errorbar(
                x=x_actual, y=mean_val, yerr=std_val, fmt="none",
                color="black", capsize=5, elinewidth=1
            )

        # Add annotation if there is a significant effect
        if param in anova_results:
            p_values = anova_results[param]["Pr > F"]
            significant_effects = []

            if p_values["g_level_corrected"] < 0.05:
                significant_effects.append("G-Level Effect")
            if p_values["bed_chair"] < 0.05:
                significant_effects.append("Posture Effect")
            if p_values["g_level_corrected:bed_chair"] < 0.05:
                significant_effects.append("Interaction Effect")

            if significant_effects:
                sig_text = "Significant: " + ", ".join(significant_effects)
                plt.annotate(sig_text, xy=(0.05, 0.95), xycoords="axes fraction", fontsize=10, color="red",
                            bbox=dict(facecolor="white", edgecolor="red", boxstyle="round,pad=0.3"))
                
        # Set x-axis labels
        plt.xticks(ticks=range(len(category_order)), labels=category_order)

        # Set labels and title
        plt.xlabel("G-level")
        plt.ylabel(f"Group mean {param} +/- 1SD")
        plt.title(f"{model_name_cap} - {param} by Condition")

        # Add cleaned legend
        plt.legend(handles=legend_handles, title="Posture", loc="upper right")

        # Ensure the output directory for this model exists
        plot_dir = output_dir / f"anova_plots_{model_name}_model"
        plot_dir.mkdir(parents=True, exist_ok=True)
        # Construct the full file path for the plot
        plot_name = plot_dir / f"{model_name}_{param}_anova_plot.pdf"
        # Save the plot
        plt.savefig(str(plot_name), format="pdf", bbox_inches="tight")  # Ensure this is a string path
        plt.close()

        print(f"Saved ANOVA plot for {param}: {plot_name}")

if __name__ == "__main__":
    # Define paths
    params_path = Path(__file__).resolve().parent.parent / "data" / "curve_fitting_output" / "fitted_parameters_all_models.csv"
    output_dir = Path(__file__).resolve().parent.parent / "data" / "curve_fitting_output" / "anova_plots"
    output_dir.mkdir(exist_ok=True)

    # Define valid subjects (manually confirmed to have all conditions)
    VALID_SUBJECTS = {"PD", "JRL", "AW", "BY", "IS"}

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
            anova_results = run_anova(df, model)
            plot_anova_results(df, model, anova_results, output_dir)