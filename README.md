# curve_fitting

_This README is a work in progress and will be updated in an ongoing fashion._

## About

This repository contains Python scripts for cleaning and analyzing experimental
data collected by the Ashton Graybiel Spatial Orientation Laboratory at Brandeis
University. These scripts were developed to facilitate data analysis by fitting
mathematical models to observed data points, estimating parameters, and
visualizing fitted curves.

## Directory Structure

```python
curve_fitting/
|-- README.md               # Instructions for lab members - START HERE!
|
|-- src/                    # All Python scripts and modules
|   |-- data_processing.py      # Prepare data for analysis
|   |-- descriptives.py         # Generate descriptive stats for dependent variables
|   |-- curve_functions.py      # Define polynomial / custom fxns for curve fitting
|   |-- curve_fitting.py        # Fit curves to trial data, export model results
|   |-- curve_fit_goodness.py   # Generate goodness of fit statistics for each model
|   |-- curve_fit_visualization.py  # Plot fitted curves over raw data
|   |-- anova_fitted_params.py  # Run ANOVAs on estimated model parameters
|
|-- data/                   # Data files
|   |-- processed/              # HP's processed data from 2012
|   |-- for_analysis/           # Combined data from all Ss
|   |-- analysis_output/        # Output: descriptives, model fits, & ANOVA results
|
|-- analysis_config.env     # Configuration file (TO BE EDITED FOR CUSTOM ANALYSES)
|-- run_analysis.py         # Main script that runs everything
|-- requirements.txt        # Dependencies for the project


```

## Features

- **Flexible model fitting**: Supports linear, polynomial, and nonlinear curve fitting.

- **Customizable models**: Define custom mathematical functions to fit a variety
of experimental data.

- **Goodness-of-fit metrics**: Includes R<sup>2</sup>, RMSE, and residual
analysis to evaluate model performance.

- **Visualization tools**: Plots raw data alongside fitted curves for easy interpretations.

## Dependencies

- Python 3.x
- NumPy
- SciPy
- Matplotlib
- Pandas

## Usage

(Coming soon)

## To-Do

1. :white_check_mark: Scripts:

    - :white_check_mark: data_processing.py
    - :white_check_mark: curve_functions.py
    - :white_check_mark: descriptives.py
    - :white_check_mark: curve_fitting.py
    - :white_check_mark: curve_fit_goodness.py
    - :white_check_mark: curve_fit_visualization.py
    - :white_check_mark: anova_fitted_params.py
    - :white_check_mark: run_analysis.py

2. :construction_worker_woman: Update individual script annotation
3. :no_entry: Add sample data for package
4. :construction_worker_woman: Write setup.py / pyproject.toml
5. :no_entry: Update final README
