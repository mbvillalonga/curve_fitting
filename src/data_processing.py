import pandas as pd
import os

# For each trial group (contained in a subdirectory of /data/processed)
# combine files from all subjects into one data frame

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__)) # dir with current file
data_base_dir = os.path.normpath(os.path.join(script_dir, "..", "data")) # dir with data files
paths_list = [ # data subdirs 
    os.path.join(data_base_dir, "processed", "flight_xls_midline"), # for DVs related to subjective vertical/rear
    os.path.join(data_base_dir, "processed", "flight_xls_pointback") # for DVs related to displacement and midline
]

# Output directory
data_out_dir = os.path.join(data_base_dir, "for_analysis") 
os.makedirs(data_out_dir, exist_ok=True)

# Iterate over each subdir of processed data (each subdir contains a different subset of trials)
for paths in paths_list:
    df_list = [] # Initialize empty list to store combined data for this trial group
    folder_name = os.path.basename(paths) # store trial group for metadata
    if folder_name == "flight_xls_pointback":
        trial_group = "d_ml_trials" # renames file correctly for DVs related to displacement and midline
    else:
        trial_group = "v_r_trials" # renames file correctly for DVs related to subjective vertical/rear

    print(f"Processing directory: {paths}")

    if not os.path.exists(paths):
        print(f"Warning: Path {paths} does not exist. Skipping...")
        continue # skip if folder doesn't exist

    flight_dirs = os.listdir(paths) # list all flight subdirs

    for flight in flight_dirs:
        flight_path = os.path.join(paths, flight)

        if os.path.isdir(flight_path): # ensure it's a directory and not a file
            files = os.listdir(flight_path)

            for file in files:
                if not file.startswith('.'): # ignore hidden files
                    file_path = os.path.join(flight_path, file)

                    try:
                        df_temp = pd.read_excel(file_path)
                        df_temp["source_folder"] = folder_name # add trial group metadata
                        df_temp["flight"] = flight # add flight metadata
                        df_list.append(df_temp) # add current file's data to data_list
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    # Concatenate all data into a single dataframe for this trial group
    if df_list:
        df_combined = pd.concat(df_list, ignore_index=True)
        out_file = os.path.join(data_out_dir, f"{trial_group}_combined.csv")
        df_combined.to_csv(out_file, index=False)
        print(f"Saved combined dataset to: {out_file}")
    else:
        print(f"No valid files found in {folder_name}. Skipping CSV creation.")