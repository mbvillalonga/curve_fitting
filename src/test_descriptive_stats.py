import pandas as pd
from pathlib import Path
from descriptives import compute_descriptive_stats

# Define test data path
test_data_dir = Path(__file__).resolve().parent.parent / "test_data"
test_output_dir = test_data_dir / "output"

# Create test directories if they don't exist
test_output_dir.mkdir(parents=True, exist_ok=True)

# Mock DataFrames for testing
mock_d_ml_data = pd.DataFrame(
    {
        "subj_idx": ["S1", "S2", "S3", "S4"],
        "turn_displacement": [30, 30, -30, -30],
        "bed_chair": ["bed", "chair", "bed", "chair"],
        "g_level_corrected": [1.0, 1.0, 1.8, 1.8],
        "turn_bed_displacement": [32, 29, -31, -28],
        "indicated_displacement": [30, 31, -32, -29],
        "indicated_displacement_error": [2, -1, -1, 1],
        "midline_indicated_angle": [5, 4, -3, -2],
        "turn_rms_track_error": [0.5, 0.7, 0.4, 0.6],
        "turn_start_joystick_position": [0.2, -0.3, 0.1, -0.1],
    }
)

# Define test variables
test_d_ml_vars = [
    "turn_bed_displacement",
    "indicated_displacement",
    "indicated_displacement_error",
    "midline_indicated_angle",
    "turn_rms_track_error",
    "turn_start_joystick_position",
]
test_group_vars = ["turn_displacement", "bed_chair", "g_level_corrected"]


def test_compute_descriptive_stats():
    """Test that compute_descriptive_stats correctly calculates subject-level and grand mean stats."""
    subj_stats, grand_mean = compute_descriptive_stats(
        mock_d_ml_data, test_d_ml_vars, test_group_vars, test_output_dir
    )

    # Ensure returned objects are DataFrames
    assert isinstance(subj_stats, pd.DataFrame), (
        "Subject-level stats should be a DataFrame"
    )
    assert isinstance(grand_mean, pd.DataFrame), (
        "Grand mean stats should be a DataFrame"
    )

    # Ensure expected columns are present for subj_stats df
    expected_columns = test_group_vars + ["subj_idx"]
    for col in test_d_ml_vars:
        expected_columns.extend([f"{col}_count", f"{col}_mean", f"{col}_std"])

    assert all(col in subj_stats.columns for col in expected_columns), ("Missing expected columns in subject-level stats")

    # Ensure expected columns are present for grand_means df
    expected_columns = test_group_vars  # grand_mean does NOT include subj_idx
    for col in test_d_ml_vars:
        expected_columns.extend([f"{col}_mean", f"{col}_std"])
    
    assert all(col in grand_mean.columns for col in expected_columns if col != "subj_idx"), "Missing expected columns in grand mean stats"

    # Save DataFrames to CSVs in test output directory
    subj_stats.to_csv(test_output_dir / "test_subj_stats.csv", index=False)
    grand_mean.to_csv(test_output_dir / "test_grand_means.csv", index=False)

    # Verify that the output files were created in the test directory
    assert (test_output_dir / "test_subj_stats.csv").exists(), "Subject-level stats file missing!"
    assert (test_output_dir / "test_grand_means.csv").exists(), "Grand mean stats file missing!"

    print("✅ test_compute_descriptive_stats PASSED")

if __name__ == "__main__":
    test_compute_descriptive_stats()
    print("✅ All tests passed successfully!")
