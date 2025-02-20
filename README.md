# curve_fitting

_This README is a work in progress and is updated in an ongoing fashion._

This repository contains Python scripts for performing curve fitting on experimental data. These scripts facilitate data analysis by fitting mathematical models to observed data points, estimating parameters, and visualizing fitted curves.

## Features

- **Flexible model fitting**: Supports linear, polynomial, and nonlinear curve fitting.
- **Customizable models**: Define custom mathematical functions to fit a variety of experimental data.
- **Goodness-of-fit metrics**: Includes R<sup>2</sup>, RMSE, and residual analysis to evaluate model performance.
- **Visualization tools**: Plots raw data alongside fitted curves for easy interpretations.

## Project Directory

```
curve_fitting/
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- data/
|   |-- cleaned/                # Store copy of cleaned data files for each subject; input for data_processing.py
|   |-- for_analysis/           # Store reduced and combined data; output from data_processing.py
|-- src/                # Python modules
|   |-- data_processing.py      # Prepare data for analysis
|   |-- descriptives.py         # Generate descriptive stats and visualizations for different dependent variables
|   |-- curve_fitting.py        # Fit curves to subject-level data and export model results
|   |-- statistical_tests.py    # Run ANOVAs on estimated model parameters
|   |-- visualization.py        # Visualize model fits
|   |-- main.py                 # 
```

## Dependencies

- Python 3.x
- NumPy
- SciPy
- Matplotlib
- Pandas

## Usage

(Coming soon)

## To do

1. Modularize scripts
2. Add file structure
3. Write setup.py / pyproject.toml
