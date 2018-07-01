# forecasting energy time series 

This repo is in the initial stages of development.  I'm currently very busy working on timeseries problems in my day job at Tempus Energy, working on a energy focused reinforcement learning library energy_py and teaching a reinforcement learning course!

As I build tools for my work at Tempus I try to port them over to this library. 

## goals for the repo

The aim of this repo is to provide a set of tools and examples of time series forecasting for energy problems.

### data

Tools for scraping publically available energy datasets and tools for cleaning & processing data for use in training models.

Scraping
- Elexon (UK grid data)

Processing
- Elexon
- wind farm data

### feature engineering

Toolkit for engineering features using sklearn pipelines.  Fully developed test suite for each individual pipeline.

### models

A model library that wraps commonly used models
- linear regression
- SARIMA
- random forests
- feedforward nn
- convolutional nn
- lstm nn

Tools for analyzing model performance
- error metrics such as MAPE, MASE

### visualization

A toolkit for common plots
- correlations
- autocorrelations



