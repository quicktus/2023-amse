# Project Plan

## Summary

This project aims to analyze correlations between the popularity of music and the weather conditions at the time. The project will attempt to identify possible relationships. Based on these, it will use the current weather conditions to suggest a "weather appropriate" song to the user.

## Rationale

The analysis will provide insights into the possible relationship between music and weather conditions. While the project is primarily intended as an entertaining exploration of these, it could also lead to users discovering new music.

## Datasources

### Datasource1: Spotify daily charts per country

* Metadata URL: https://www.kaggle.com/datasets/pepepython/spotify-huge-database-daily-charts-over-3-years
* Data Type: CSV

This dataset contains all songs in Spotify's daily top 200 charts over a 3-year period (2017-2020) for 35+1 (global) countries. It includes various metadata such as genre or audio features like acousticness or danceability.

### Datasource2: DWD Climate Data

* Metadata URL: https://mobilithek.info/offers/-4979349128225020802
* Data URL: https://opendata.dwd.de/climate_environment/
* Data Type: various

The data set is used for weather monitoring and forecasting purposes. It contains standardized meteorological measurement and observation data from various locations in Germany.

## Work Packages

1. [Automated data pipeline](https://github.com/quicktus/2023-amse/issues/1)
2. [Automated tests](https://github.com/quicktus/2023-amse/issues/2)
3. [Continuous Integration](https://github.com/quicktus/2023-amse/issues/3)
4. [Data visualization](https://github.com/quicktus/2023-amse/issues/5)
5. [Implement song recommendation](https://github.com/quicktus/2023-amse/issues/6)
6. ~~[Deployment](https://github.com/quicktus/2023-amse/issues/4)~~

___

**:warning: Disclaimer:** This project is intended as an amusing exercise in finding correlations and does not aim to prove a causal relationship between weather conditions and the popularity of particular songs or genres. The analysis is not intended to be scientifically rigorous and should not be construed as such.
