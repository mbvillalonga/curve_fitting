import pandas as pd
from pathlib import Path

# For each trial group (contained in a subdirectory of /data/processed)
# combine files from all subjects into one data frame

# %%
# Define directory paths using pathlib
script_dir = Path(__file__).resolve().parent # dir with data_cleaning.py (this file)
project_dir = script_dir.parent # main project directory
data_base_dir = project_dir / "data" # dir with all data
paths_list = [ # data subdirs with input for cleaning
    data_base_dir / "processed" / "flight_xls_midline", # acceptable trials for DVs related to SUBJECTIVE VERTICAL/REAR
    data_base_dir / "processed" / "flight_xls_pointback" # accepable trials for DVs related to DISPLACEMENT and MIDLINE
]

data_out_dir = data_base_dir / "testing" / "for_analysis" # output directory for cleaned data
data_out_dir.mkdir(parents=True, exist_ok=True)  # creates directory if missing


#%%

combined_data = {} # initialize dict that will store processed data from all subjects, all acceptable trials

# Iterate over each subdir of processed data (each subdir contains a different subset of trials)
for paths in paths_list:
    df_list = [] # initialize empty list to store combined data for this trial group
    folder_name = paths.name 
    if folder_name == "flight_xls_pointback": # store trial group for metadata
        trial_group = "d_ml_trials" # renames file correctly for DVs related to DISPLACEMENT (d) and MIDLINE (ml)
    else:
        trial_group = "v_r_trials" # renames file correctly for DVs related to SUBJECTIVE VERTICAL (v)/REAR (r)

    print(f"\nCleaning data from directory: {paths}")

    if not paths.exists():
        print(f"\n***WARNING*** Path {paths} does not exist. Skipping...")
        continue # skip if folder doesn't exist

    for flight_path in paths.iterdir():
        if flight_path.is_dir(): # ensure it's a directory and not a file
            for file_path in flight_path.glob("*"):
                if not file_path.name.startswith('.'): # ignore hidden files
                    try:
                        df_temp = pd.read_excel(file_path)
                        df_temp["source_folder"] = folder_name # add metadata listing the input folder (HP data)
                        df_temp["flight"] = flight_path.name # add flight metadata 
                        df_temp["use_for_2025"] = trial_group # this indicates whether rows should be used for d_ml or v_r analyses
                        df_list.append(df_temp) # add current file's data to data_list
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    # Concatenate all data into a single dataframe for this trial group
    if df_list:
        df_combined = pd.concat(df_list, ignore_index=True)
        combined_data[trial_group] = df_combined # store in dict for subsequent data reduction
        #out_file = os.path.join(data_out_dir, f"{trial_group}_combined.csv")
        #df_combined.to_csv(out_file, index=False)
        print(f"Stored DataFrame for {trial_group} (Rows: {df_combined.shape[0]})")
    else:
        print(f"No valid files found in {folder_name}. Skipping DataFrame creation.")

# %%
# Create new variables to use in analyses

for name, df in combined_data.items():
    print(f"\nCleaning dataset: {name}\nAdding new variables...")

    # if statements make sure the required columns exist before creating new variables
    if "csvfile" in df.columns:
        df['subj_idx'] = df['csvfile'].str.rsplit('/').str[-1].str.split('_').str[0] # subject ID
        df['bed_chair'] = df['csvfile'].str.rsplit('_').str[-2].str.split('-').str[-1] # posture condition: v=bed, r=chair
        print(f"\n✅ Added subj_idx and bed_chair to dataset: {name}")


    if "turn_displacement" in df.columns:
        df['abs_turn_displacement'] = abs(df['turn_displacement']) # absolute value of intended turn amplitude
    
    if "intended_abs_peak_velocity" in df.columns:
        df['intended_abs_peak_velocity_cat'] = round(df['intended_abs_peak_velocity'].astype('int64')) # categorical version of variable
    

# %%
# Import list of variables to keep
try:
    vars_to_keep_path = project_dir / "vars_to_keep.csv"
    vars_to_keep = pd.read_csv(vars_to_keep_path, header=None).squeeze("columns").dropna().tolist()
    print(f"\nSuccessfully loaded {len(vars_to_keep)} variables from vars_to_keep.csv")
except FileNotFoundError:
    print(f"\n***ERROR*** File not found - {vars_to_keep_path}")
    vars_to_keep = []
except pd.errors.EmptyDataError:
    print("\n***ERROR*** vars_to_keep.csv is empty.")
    vars_to_keep = []
except Exception as e:
    print(f"\n***ERROR*** Error loading vars_to_keep.csv: {e}")
    vars_to_keep = []

# %%
# Data reduction: remove variables that will not be used for analysis
for key, df in combined_data.items():
    # select columns that actually exist in the data
    cols_to_keep = [col for col in vars_to_keep if col in df.columns]

    if not cols_to_keep:
        print(f"\n***WARNING*** No valid columns found for {key}. Skipping export.")
        continue

    # keep only selected columns in a temporary dataframe
    df_reduced = df[cols_to_keep]
    
    # export reduced dataframe as csv
    out_file = data_out_dir / f"{key}_cleaned_allsubj.csv"
    try:
        df_reduced.to_csv(out_file, index=False)
        print(f"\nExported {key} file to:\n{data_out_dir}")
    except Exception as e:
        print(f"\n***ERROR*** Error saving output file: {e}")