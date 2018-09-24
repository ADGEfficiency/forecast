# forecasting energy time series 

This project is in the initial stages of development.  I'm currently working on time series problems at Tempus Energy - as I build tools for my work at Tempus I try to port them over to this library. 

## goals for the repo

The aim of this repo is to provide a set of tools and examples of time series forecasting for energy problems.

Reusable tools exist in `forecast/forecast` - project specific code exists in `projects/project_name`.  The structure of a project folder is flexible.

### data

Tools for scraping publically available energy datasets and tools for cleaning & processing data for use in training models.

Scraping
- Elexon (UK grid data)

Processing
- Elexon
- wind farm data

```
Makridakis_2018_statistical_ml_concerns.pdf

Original data: No pre-processing is applied.
• Transforming the data: The log or the Box-Cox [66] power transformation is applied to the
original data in order to achieve stationarity in the variance.
• Deseasonalizing the data: The data is considered seasonal if a significant autocorrelation
coefficient at lag 12 exists. In such case the data is deseasonalized using the classical, multiplicative
decomposition approach [39]. The training of the ML weights, or the optimization of
statistical methods, is subsequently done on the seasonally adjusted data. The forecasts
obtained are then reseasonalized to determine the final predictions. This is not done in the
case of ETS and ARIMA methods since they include seasonal models, selected using relative
tests and information criteria that take care of seasonality and model complexity directly.
• Detrending the data: A Cox-Stuart test [67] is performed to establish whether a deterministic
linear trend should be used, or alternatively first differencing, to eliminate the trend
from the data and achieve stationarity in the mean.
• Combination of the above three: The benefits of individual preprocessing techniques are
applied simultaneously to adjust the original data.
```

### feature engineering

Toolkit for engineering features using sklearn pipelines.  Fully developed test suite for each individual pipeline.

Transformations
- boxcox

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

A toolkit for common plots used for time series analysis

Completed
- time series plots
- grouping of variables by month/day/hour
- distributions of data
- autocorrelation & partial autocorrelation
- lagged scatter matrix

Todo
- box plots
- (https://github.com/sebaheg/GEFCom2014-wind)
- fig 8 from 2017_Ullah_energy_cons_markov_models.pdf (box plot for every hour of the day)
- https://otexts.org/fpp2/ - plots and methods from Hyndman
- mixed density networks - http://blog.otoro.net/2015/11/24/mixture-density-networks-with-tensorflow/
- http://euanmearns.com/el-hierro-portal/ - a data source
- http://www.netzdaten-berlin.de/#

why is seasonality a problem:
* If the dependent variable has seasonality, then the variance of the total will be larger on days with greater business activity (this is a consequence of the central limit theorem)
* Transformations such as logging or seasonal adjustment can be used to deal with this problem
what is central limit theorem
* central limit theorem - sum or avg of a large number of independent random variables (whatever their distributions) reaches a normal distribution
autocorrelation
* If autocorrelation is a problem, probably include lagged variables.  Stationarize dependent or dependent by differencing, or add lags of the dependent/independent variable regression, or include autoregressive error correction (which is better, differencing or including the vars?)
