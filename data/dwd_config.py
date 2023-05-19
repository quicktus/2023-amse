data_sources = [
    {
        "name": "rain_data",
        "path": "climate_environment/CDC/observations_germany/climate/daily/more_precip/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "  RS", " RSF", "SH_TAG", "NSH_TAG"], # NOTE: the spaces in the column names are intentional
        "new_columns": ["stations_id", "mess_datum", "niederschlagshoehe_mm", "niederschlagsform", "schneehoehe_cm", "neuschneehoehe_cm"],
    },
    {
        "name": "cloud_data",
        "path": "climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "N_TER", "CD_TER"],
        "new_columns": ["stations_id", "mess_datum", "bedeckungsgrad", "wolkendichte"],
    },
    {
        "name": "temperature_data",
        "path": "climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "TT_TER", "RF_TER"],
        "new_columns": ["stations_id", "mess_datum", "lufttemperatur", "rel_feuchte"],
    },
    {
        "name": "wind_data",
        "path": "climate_environment/CDC/observations_germany/climate/subdaily/wind/historical/",
        "columns": ["STATIONS_ID", "MESS_DATUM", "DK_TER", "FK_TER"],
        "new_columns": ["stations_id", "mess_datum", "windrichtung", "windstaerke"],
    }
]

# DWD documentation on the data types (especially the KL- and KL2000-format):
# https://opendata.dwd.de/climate_environment/CDC/Liesmich_intro_CDC-FTP.pdf
# https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/more_precip/historical/BESCHREIBUNG_obsgermany_climate_daily_more_precip_historical_de.pdf
# https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/standard_format/BESCHREIBUNG_obsgermany_climate_subdaily_standard_format_de.pdf
# https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/standard_format/download_legende_klkxformat.pdf
