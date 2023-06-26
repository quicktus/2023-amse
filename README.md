**:information_source:** _This repository is a student project focused on data engineering and data science using open data. It is part of the AMSE/SAKI course, conducted by the [FAU](https://fau.eu/) [Chair for Open-Source Software](https://oss.cs.fau.de/) during the summer semester of 2023._

<h1 align="center">
  <img alt="Logo" src="media/logo_light.png" width="256" height="256">
</h1>

# Weather Conditions and Music Preferences

[![Project Pipeline](https://github.com/quicktus/2023-amse/actions/workflows/action.yml/badge.svg?branch=main)](https://github.com/quicktus/2023-amse/actions/workflows/action.yml)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Summary
This project explores the potential connection between music preferences and weather conditions. The analysis indicates that although some associations between music and weather were observed, they were not found to be statistically significant. I speculate that music preferences are influenced by various factors, with the impact of weather being minor.  
Additionally, I use the current weather conditions to attempt to suggest a "weather appropriate" song to the user.  
</br>
:point_right: [**Read the Project Report!**](project/report.html)

## Methods and Data
The project is implemented in Python and primarily uses [pandas](https://pandas.pydata.org/) for data processing and [matplotlib](https://matplotlib.org/) for data visualization.  
The analysis is based on data from the [Open Data Server](https://opendata.dwd.de/) of the [German Meteorological Service](https://www.dwd.de/EN/Home/home_node.html) and a [kaggle](https://www.kaggle.com/) dataset of [Daily Song Rankings](https://www.kaggle.com/datasets/pepepython/spotify-huge-database-daily-charts-over-3-years) scraped from [Spotify](https://developer.spotify.com/documentation/web-api/) as well as additional data points taken directly from Spotify.  

## Set up
1. install [python 3.11](https://www.python.org/downloads/release/python-3110/) and the packages detailed in `requirements.txt`.
2. clone this repository.
3. create an account with kaggle and [set up your API Token](https://www.kaggle.com/docs/api).
4. create an account with spotify and [set up your API Token](https://developer.spotify.com/documentation/web-api#getting-started) and place it in `data/spotify_credentials.txt`.
5. run `pull-data-py` from the `data` directory.
6. execute the `report_source.ipynb` notebook.
7. enjoy!
___

**:warning:** _This project does not aim to establish a causal relationship between weather conditions and music preferences and should not be construed as such._

