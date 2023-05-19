# built using python v3.11.3

# * Datasource1: Spotify daily charts per country (kaggle)
#    -> https://www.kaggle.com/datasets/pepepython/spotify-huge-database-daily-charts-over-3-years

# * Datasource2: Climate Data (DWD)
#   - Rain           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/more_precip/
#   - Sun / Cloud    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/
#   - Temperature    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/
#   - Wind           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/wind/

# NOTE: If you suspect any issues with the local data, you can try running this script with the "--clean" flag. This will
#       clean it by deleting and re-downloading all data files and re-building the SQLite db.

import os
import pandas as pd
import re
import shutil
import sqlalchemy as sa
import sys
import zipfile

from ftplib import FTP
from kaggle.api.kaggle_api_extended import KaggleApi
from rich import print
from rich.progress import track

from dwd_config import data_sources
from logger import log


# globals
RAW_DIR: str = "raw"
DB_CONNECTION_URI = "sqlite:///../data.sqlite"
FTP_URI: str = "opendata.dwd.de"
engine = sa.create_engine(DB_CONNECTION_URI)

def main():
    # Clean data if "--clean" flag is present
    if "--clean" in sys.argv:
        clean_data()

    log("Pipeline started", timestamp=True)

    # Download and extract spotify data
    spotify: str = "spotify_data"
    if sa.inspect(engine).has_table(spotify):
        log(f"Found {spotify} table")
    else:
        if(os.path.exists(os.path.join(RAW_DIR, spotify))):
            log(f"Found raw {spotify} files")
        else:
            download_spotify_data(spotify)
        extract_spotify_data_to_db(spotify)

    # Download and extract weather data
    for data_src in data_sources:
        if sa.inspect(engine).has_table(data_src["name"]):
            log(f"Found {data_src['name']} table")
        else:
            if(os.path.exists(os.path.join(RAW_DIR, data_src['name']))):
                log(f"Found raw {data_src['name']} files")
            else:
                download_weather_data(data_src['name'], data_src['path'])
            extract_weather_data_to_db(data_src['name'], data_src['columns'], data_src['new_columns'])

    log("Pipeline completed", timestamp=True)


def clean_data():
    """Cleans the raw data directory and SQLite database."""

    # Remove all subdirectories in the raw data directory
    try:
        desc = log("Removing raw data files ", "status", ret_str=True)
        progress_dirs = track(os.listdir(RAW_DIR), description=desc, transient=True)
        for sub_dir in progress_dirs:
            sub_dir_path = os.path.join(RAW_DIR, sub_dir)
            shutil.rmtree(sub_dir_path)
    except:
        log("Failed to remove raw data files", "error")
        return

    # Delete all tables in the SQLite db
    try:
        with engine.begin() as connection:
            tables = connection.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
            desc = log("Dropping all tables in db ", "status", ret_str=True)
            progress_tables = track(tables, description=desc, transient=True)
            for table in progress_tables:
                connection.execute(sa.text(f"DROP TABLE {table[0]}"))
    except:
        log("Failed to drop tables in db", "error")
        return

    log("Cleaned raw data directory and SQLite database", "success")


def download_weather_data(data_src_name: str, path: str):
    """Downloads DWD (German Weather Service) data from the FTP server."""

    # Connect to FTP server and navigate to the target directory
    try:
        ftp =  FTP(FTP_URI, timeout=20) # 20 second timeout
        ftp.login()
    except:
        log("Failed to connect to FTP server", "error")
        return

    directory_path, file_name = os.path.split(path)

    try:
        ftp.cwd(directory_path)

        # Get a list of all files
        files: list[str] = None
        if file_name is None or file_name == "":
            files = ftp.nlst()
        else:
            files = [file_name]

        # Filter for right timeframe (2017-2020)
        filtered_files: list[str] = []
        for file in files:
            match = re.search(r"(\d{8})_(\d{8})", file)
            if match:
                start_date, end_date = match.group(1), match.group(2)
                if start_date <= "20170125" and end_date >= "20201130":
                    filtered_files.append(file)

        # Create target directory
        raw_data_directory: str = os.path.join(RAW_DIR, data_src_name)
        os.makedirs(raw_data_directory, exist_ok=True)

        # Download each file
        desc = log(f"Downloading {data_src_name} from server ", "status", ret_str=True)
        progress = track(filtered_files, description=desc, transient=True)
        for file in progress:
            local_filename: str = os.path.join(raw_data_directory, file)
            with open(local_filename, "wb") as f:
                def callback(chunk):
                    f.write(chunk)
                ftp.retrbinary("RETR " + file, callback)
    except:
        log(f"Failed to download {data_src_name} from server", "error")
        return

    log(f"Downloaded {data_src_name}", "success")


def extract_weather_data_to_db(data_src_name: str, cols: str, new_cols: str):
    """Extracts DWD (German Weather Service) data to the database."""
    try:
        directory: str = os.path.join(RAW_DIR, data_src_name)
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
                        df = df.filter(items=cols)
                        # Rename columns to a more readable format
                        df = df.rename(columns=dict(zip(cols, new_cols)))
                        # Store the data into the SQLiteDB
                        df.to_sql(data_src_name, engine, if_exists="append", index=False)
    except:
        log(f"Failed to extract {data_src_name} into database", "error")
        return

    log(f"Extracted {data_src_name}", "success")


def download_spotify_data(spotify: str):
    """Downloads Spotify data from Kaggle."""

    # Working with the kaggle API requires an API Token, see:
    # https://www.kaggle.com/docs/api
    # https://github.com/Kaggle/kaggle-api

    spotify_uri: str = "pepepython/spotify-huge-database-daily-charts-over-3-years"

    # Authenticate with the Kaggle API
    try:
        api = KaggleApi()
        api.authenticate()
    except:
        log("Could not authenticate with Kaggle API", "error")
        return

    print(log(f"Downloading {spotify} from server", "status", ret_str=True), end= "\r")

    # Download the dataset
    try:
        api.dataset_download_files(spotify_uri, path=os.path.join(RAW_DIR, spotify))
    except:
        log(f"Could not download {spotify}", "error")
        return

    log(f"Downloaded {spotify}" + " "*42, "success")
    return


def extract_spotify_data_to_db(spotify: str):
    """Extracts Spotify data from the downloaded ZIP file and stores it in the database."""

    ZIP_NAME: str = "spotify-huge-database-daily-charts-over-3-years.zip"
    MEMBER_NAME: str = "Database to calculate popularity.csv"
    data_src_path: str = os.path.join(RAW_DIR, spotify, ZIP_NAME)

    print(log(f"Extracting {spotify} into database", "status", ret_str=True), end= "\r")

    try:
        zip_ref = zipfile.ZipFile(data_src_path, "r")
        tmpfile = zip_ref.open(name=MEMBER_NAME, mode="r")
        df = pd.read_csv(tmpfile)
        # Filter to only include rows where country is Germany
        df = df[df['country'] == 'Germany']
        # Store the data into the SQLiteDB
        df.to_sql(spotify, engine, if_exists="replace", index=False)
    except:
        log((f"Could not extract {spotify}" + " "*7), "error")

    log((f"Extracted {spotify}" + " "*15), "success")


if __name__ == "__main__":
    main()
