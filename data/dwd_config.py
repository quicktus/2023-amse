data_sources = [
    {
        "name": "rain_data",
        "path": "climate_environment/CDC/observations_germany/climate/daily/more_precip/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "  RS", " RSF"],
    },
    {
        "name": "cloud_data",
        "path": "climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "N_TER", "CD_TER"],
    },
    {
        "name": "temperature_data",
        "path": "climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "TT_TER", "RF_TER"],
    },
    {
        "name": "wind_data",
        "path": "climate_environment/CDC/observations_germany/climate/subdaily/wind/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "DK_TER", "FK_TER"],
    }
]

# list of weather acronyms:
# https://www.noaa.gov/jetstream/appendix/weather-acronyms