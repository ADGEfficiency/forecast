# wind_forecasting

This dataset comes from [Intelligent Embedded Systems - the EuropeWindFarm data set](https://www.ies.uni-kassel.de/Software).

## Data Description

The data set containing the day-ahead forecasts of 45 wind farms (off- and onshore) scattered over the European continent as shown in Fig. 6. The data set contains hourly averaged wind power generation time series for two consecutive years and the corresponding day-ahead meteorological forecasts using the European Centre for Medium-Range Weather Forecasts (ECMWF) weather model. 

## Data Items

* Time Stamp of the measurement
* Forecasting Time Step - time between the creation of the forecast to the forecasted point in time
* Wind Speed in 100m height
* Wind Speed in 10m height
* Wind Direction (zonal) in 100m height
* Wind Direction (meridional) in 100m height
* Air Pressure Forecast of the measurement
* Air Temperature Forecast of the measurement
* Wind Power Generation of the wind farm

## Data Processing

* The power generation time series are normalized with the respective nominal capacity of the wind farm in order to enable a scale-free comparison. 
* All weather situations are normalized in the range [0..1]. 
* The data set is filtered to discard any period of time longer than 24h in which no energy has been produced, as this is an indicator of a wind farm malfunction.
