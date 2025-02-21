# curve_fitting

_This README is a work in progress and will be updated in an ongoing fashion._

## About

This repository contains Python scripts for cleaning and analyzing experimental data collected by the Ashton Graybiel Spatial Orientation Laboratory at Brandeis University. These scripts were developed to facilitate data analysis by fitting mathematical models to observed data points, estimating parameters, and visualizing fitted curves.

## Directory Structure

```
curve_fitting/
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- data/
|   |-- processed/          # Store copy of processed data files for each subject; input for data_processing.py
|   |-- for_analysis/           # Store reduced and combined data; output from data_processing.py
|-- src/                        # Python modules
|   |-- data_processing.py      # Prepare data for analysis
|   |-- descriptives.py         # Generate descriptive stats and visualizations for different dependent variables
|   |-- curve_fitting.py        # Fit curves to subject-level data and export model results
|   |-- statistical_tests.py    # Run ANOVAs on estimated model parameters
|   |-- visualization.py        # Visualize model fits
|   |-- main.py                 # 
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
