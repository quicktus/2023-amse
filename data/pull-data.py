# Required Data:

# * Datasource1: Spotify daily charts per country (kaggle)
#    -> https://www.kaggle.com/datasets/pepepython/spotify-huge-database-daily-charts-over-3-years

# * Datasource2: Climate Data (DWD)
#   - Rain           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/more_precip/
#   - Sun / Cloud    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/
#   - Temperature    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/
#   - Wind           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/wind/

# NOTE: If you suspect any issues with the local data, you can try running this script with the "--clean" flag. This will
#       clean it by deleting and re-downloading all data files and re-building the SQLite db.

from ftplib import FTP
from rich.progress import track
from rich import print
import pandas as pd
import os
import sys
import zipfile
import shutil
import sqlalchemy as sa
from kaggle.api.kaggle_api_extended import KaggleApi
from logger import log

# globals
raw_dir: str = "raw"
db_connection_uri = "sqlite:///../data.sqlite"
engine = sa.create_engine(db_connection_uri)

def main():

    spotify: str = "spotify_data"
    spotify_uri: str = "pepepython/spotify-huge-database-daily-charts-over-3-years"
    spotify_path: str = os.path.join(raw_dir, spotify)
    spotify_zip_name: str = "spotify-huge-database-daily-charts-over-3-years.zip"
    spotify_member_name: str = "Database to calculate popularity.csv"

    ftp_uri: str = "opendata.dwd.de"
    data_sources = [
        {
            "name": "station_data",
            "path": "climate_environment/CDC/help/RR_Tageswerte_Beschreibung_Stationen.txt",
            "columns": ["column1", "column2", "column3"]
        },
        {
            "name": "rain_data",
            "path": "climate_environment/CDC/observations_germany/climate/daily/more_precip/historical/",
            "columns": ["STATIONS_ID", "MESS_DATUM", "  RS", " RSF"]
        },
        {
            "name": "cloud_data",
            "path": "climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/historical/",
            "columns": ["STATIONS_ID", "MESS_DATUM", "N_TER", "CD_TER"]
        },
        {
            "name": "temperature_data",
            "path": "climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/historical/",
            "columns": ["STATIONS_ID", "MESS_DATUM", "TT_TER", "RF_TER"]
        },
        {
            "name": "wind_data",
            "path": "climate_environment/CDC/observations_germany/climate/subdaily/wind/historical/",
            "columns": ["STATIONS_ID", "MESS_DATUM", "DK_TER", "FK_TER"]
        }
    ]
    # list of weather acronyms:
    # https://www.noaa.gov/jetstream/appendix/weather-acronyms

    if "--clean" in sys.argv:
        clean_data()
        log("Cleaned raw data directory and SQLite database", "success")

    log(f"Pipeline started", timestamp=True)

    # Working with the kaggle API requires an API Token, see:
    # https://www.kaggle.com/docs/api
    # https://github.com/Kaggle/kaggle-api

    api = KaggleApi()
    api.authenticate()

    if(os.path.exists(spotify_path)):
            log(f"Found {spotify} files", "success")
    else:
        # Download all files of the kaggle spotify dataset
        print(log(f"Downloading {spotify} from server", "status", ret_str=True), end= "\r")
        api.dataset_download_files(spotify_uri, path=spotify_path)
        log(f"Downloaded {spotify}" + " "*42, "success")

    if sa.inspect(engine).has_table(spotify):
            log(f"Found {spotify} table", "success")
    else:
        print(log(f"Extracting {spotify} into database", "status", ret_str=True), end= "\r")
        kaggle_extract_to_db(spotify, spotify_zip_name, spotify_member_name)
        log((f"Extracted {spotify}" + " "*15), "success")

    for data_src in data_sources:
        if(os.path.exists(os.path.join(raw_dir, data_src['name']))):
            log(f"Found {data_src['name']} files", "success")
        else:
            dwd_download(ftp_uri, data_src['name'], data_src['path'])
            log(f"Downloaded {data_src['name']}", "success")

        if sa.inspect(engine).has_table(data_src["name"]):
            log(f"Found {data_src['name']} table", "success")
        else:
            dwd_extract_to_db(data_src['name'], data_src['columns'])
            log(f"Extracted {data_src['name']}", "success")

    log(f"Pipeline completed", timestamp=True)


def dwd_download(ftp_uri: str, data_src_name: str, path: str):
    # Connect to FTP server and navigate to the target directory
    ftp = FTP(ftp_uri)
    ftp.login()
    directory_path, file_name = os.path.split(path)
    ftp.cwd(directory_path)

    # Get a list of all files
    files: list[str] = None
    if file_name is None or file_name == "":
        files = ftp.nlst()
    else:
        files = [file_name]
    raw_data_directory: str = os.path.join(raw_dir, data_src_name)
    os.makedirs(raw_data_directory, exist_ok=True)

    # Download each file
    desc = log(f"Downloading {data_src_name} from server ", "status", ret_str=True)
    progress = track(files, description=desc, transient=True)
    for file in progress:
        local_filename: str = os.path.join(raw_data_directory, file)
        with open(local_filename, "wb") as f:
            def callback(chunk):
                f.write(chunk)
            ftp.retrbinary("RETR " + file, callback)

    # Close FTP connection
    ftp.quit()


def dwd_extract_to_db(data_src_name: str, filter_items: str):
    directory: str = os.path.join(raw_dir, data_src_name)
    # Get a list of all zip files in the directory
    zip_files = [file for file in os.listdir(directory) if file.endswith(".zip")]
    # Iterate over the zips with a progress bar
    desc = log(f"Extracting {data_src_name} into database ", "status", ret_str=True)
    for zip_file in track(zip_files, description=desc, transient=True):
        zip_path: str = os.path.join(directory, zip_file)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Get a list of member files contained in the zip file (excluding metadata files)
            member_files = [member for member in zip_ref.namelist() if not member.startswith("Metadaten_")]
            for member in member_files:
                # Read each member file into a pandas DataFrame
                with zip_ref.open(name=member, mode="r") as tmpfile:
                    df = pd.read_csv(tmpfile, sep=";")
                    # Remove unnecessary columns from the DataFrame
                    df = df.filter(items=filter_items)
                    # Store the data into the SQLiteDB
                    df.to_sql(data_src_name, engine, if_exists="append", index=False)


def kaggle_extract_to_db(data_src_name: str, zip_name: str, member_file_name: str):
    data_src_path: str = os.path.join(raw_dir, data_src_name, zip_name)
    with zipfile.ZipFile(data_src_path, "r") as zip_ref:
        with zip_ref.open(name=member_file_name, mode="r") as tmpfile:
            df = pd.read_csv(tmpfile)
            # Store the data into the SQLiteDB
            df.to_sql(data_src_name, engine, if_exists="replace", index=False)


def clean_data():
    # Remove all subdirectories in the raw data directory
    desc = log("Removing raw data files ", "status", ret_str=True)
    progress = track(os.listdir(raw_dir), description=desc, transient=True)
    for sub_dir in progress:
        sub_dir_path = os.path.join(raw_dir, sub_dir)
        shutil.rmtree(sub_dir_path)

    # Delete all tables in the SQLite db
    with engine.begin() as connection:
        tables = connection.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
        desc = log("Droping all tables in db ", "status", ret_str=True)
        progress = track(tables, description=desc, transient=True)
        for table in tables:
            connection.execute(sa.text(f"DROP TABLE {table[0]}"))


if __name__ == "__main__":
    main()
