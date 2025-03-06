# curve_fitting

_This README is a work in progress and will be updated in an ongoing fashion._

## About

This repository contains Python scripts for cleaning and analyzing experimental data collected by the Ashton Graybiel Spatial Orientation Laboratory at Brandeis University. These scripts were developed to facilitate data analysis by fitting mathematical models to observed data points, estimating parameters, and visualizing fitted curves.

## Directory Structure

```
curve_fitting/
|-- README.md               # Instructions for lab members - START HERE!
|
|-- src/                    # All Python scripts and modules
|   |-- data_processing.py      # Prepare data for analysis
|   |-- descriptives.py         # Generate descriptive stats for different dependent variables
|   |-- curve_functions.py      # Define polynomial and custom functions for curve fitting
|   |-- curve_fitting.py        # Fit curves to subject-level data and export model results
|   |-- curve_fit_goodness.py   # Generate goodness of fit statistics for each model
|   |-- anova_fitted_params.py # Run ANOVAs on estimated model parameters
|   |-- visualization.py        # Visualize model fits
|
|-- data/                   # Data files
|   |-- processed/              # HP's processed data from 2012
|   |-- for_analysis/           # Combined data from all Ss
|   |-- curve_fitting_output/   # Output folder with model fit and ANOVA results 
|
|-- analysis_config.env     # Configuration file (TO BE EDITED FOR CUSTOM ANALYSES)
|-- run_analysis.py         # Main script that runs everything
|-- requirements.txt        # Dependencies for the project


```

## Features

- **Flexible model fitting**: Supports linear, polynomial, and nonlinear curve fitting.
- **Customizable models**: Define custom mathematical functions to fit a variety of experimental data.
- **Goodness-of-fit metrics**: Includes R<sup>2</sup>, RMSE, and residual analysis to evaluate model performance.
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

1. Modularize scripts according to directory structure:

    - data_processing.py :yellow_circle: (Need to formalize as method)
    - descriptives.py :yellow_circle: (Have outline)
    - curve_fitting.py :x:
    - statistical_tests.py :x:
    - model_visualization.py :x:
    - main.py :x:

2. statistical_tests.py: modify to take as input a list of curve functions
3. Update individual script annotation
4. Write setup.py / pyproject.toml
5. Update README with final summary
