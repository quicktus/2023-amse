> **:information_source:** _This repository is a student project focused on data engineering and data science using open data. It is part of the AMSE/SAKI course, conducted by the [FAU](https://fau.eu/) [Chair for Open-Source Software](https://oss.cs.fau.de/) during the summer semester of 2023._

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
1. Install [python 3.11](https://www.python.org/downloads/release/python-3110/) and [pip](https://pypi.org/project/pip/).
2. Clone this repository.
```bash
git clone https://github.com/quicktus/2023-amse.git
```
3. Go to the project directory.
```bash
cd 2023-amse
```
4. Download and install the required python packages.
```bash
pip install -r requirements.txt
```
5. Create an account with [kaggle](https://www.kaggle.com/account/login?phase=startRegisterTab) and [set up your API Token](https://www.kaggle.com/docs/api).
6. Create an account with [spotify](https://www.spotify.com/signup) and [set up your API Token](https://developer.spotify.com/documentation/web-api#getting-started).
7. Edit `data/spotify_credentials.txt` to insert your spotify API Token, e.g.
```bash
nano data/spotify_credentials.txt
```
8. Go to the `data` directory.
```bash
cd data
```
8. Run `pull-data-py`.
 ```bash
 python pull-data-py 
 ```
10. Run, explore and modify the `report_source.ipynb` notebook in the IDE of your choice. I recommend [VS Code](https://code.visualstudio.com/). Note: you might have to install an extension for Jupyter notebooks first. 
11. Enjoy!

## Disclaimer

> **:warning:** _This project does not aim to establish a causal relationship between weather conditions and music preferences and should not be construed as such._
