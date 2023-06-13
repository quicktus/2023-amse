# built using python v3.11.3

# * Datasource1: Spotify daily charts per country (kaggle)
#    -> https://www.kaggle.com/datasets/pepepython/spotify-huge-database-daily-charts-over-3-years
#   with additional metadata from Spotify API
#    -> https://developer.spotify.com/documentation/web-api/

# * Datasource2: Climate Data (DWD)
#   - Rain           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/more_precip/
#   - Sun / Cloud    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/
#   - Temperature    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/
#   - Wind           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/wind/

# NOTE: If you suspect any issues with the local data, you can try running this script with the "--clean" flag. This will
#       clean it by deleting and re-downloading all data files and re-building the SQLite db.

import os
import time
import pandas as pd
import re
import shutil
import spotipy
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
is_test = "--test" in sys.argv

# observation period of the spotify data set
start_date = pd.to_datetime('2017-01-25')
end_date = pd.to_datetime('2020-11-30')

def main():
    # Clean data if "--clean" flag is present
    if "--clean" in sys.argv:
        clean_data()

    # Pull just a small subset of data to speed up test execution time - DO NOT USE FOR DATA ANALYSIS
    if is_test:
        log("The test flag is set. Only use this flag for testing, the resulting data will be incomplete. DO NOT USE FOR DATA ANALYSIS!", "warning")
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
        get_spotify_metadata(spotify)

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
                file_start_date, file_end_date = match.group(1), match.group(2)
                if file_start_date <= "20170125" and file_end_date >= "20201130":
                    filtered_files.append(file)

        if is_test:
            filtered_files = filtered_files[:3]

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
                        # Convert mess_datum column to datetime format
                        try:
                            df["mess_datum"] = pd.to_datetime(df["mess_datum"], format="%Y%m%d%H")
                        except:
                            df["mess_datum"] = pd.to_datetime(df["mess_datum"], format="%Y%m%d")
                        # Filter dates between 2017.01.25 and 2020.11.30 (inclusive)
                        df = df[(df['mess_datum'] >= start_date) & (df['mess_datum'] <= end_date)]
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
        df = df[df["country"] == "Germany"]
        # Drop the unnecessary columns
        df.drop(["Unnamed: 0", "country"], axis=1, inplace=True)
        # Convert the "date" column to pd.datetime
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
        # Change the "position" column to integer
        df["position"] = df["position"].astype(int)
        # convert uri to track id
        df["uri"] = df["uri"].str.strip()
        df["uri"] = df["uri"].apply(lambda uri: uri.split("/")[-1])
        df.rename(columns={"uri": "track_id"}, inplace=True)
        # Store the data into the SQLiteDB
        df.to_sql(spotify, engine, if_exists="replace", index=False)
    except:
        log((f"Could not extract {spotify}" + " "*7), "error")

    log((f"Extracted {spotify}" + " "*15), "success")


def get_spotify_metadata(spotify: str):
    """Gets the metadata for each track through the Spotify API."""

    print(log(f"Getting {spotify} track metadata", "status", ret_str=True), end= "\r")

    # get a list of all tracks in the database
    tracks = None
    try:
        connection = engine.connect()
        if is_test:
            tracks = connection.execute(sa.text(f"SELECT DISTINCT track_id FROM {spotify} LIMIT 10;")).fetchall()
        else:
            tracks = connection.execute(sa.text(f"SELECT DISTINCT track_id FROM {spotify};")).fetchall()
        assert tracks is not None
    except:
        log(f"Could not get {spotify} from database", "error")
        return None

    tracks = [track_row[0].strip() for track_row in tracks]
    try:
        tracks.remove("N\A")
        tracks.remove("#")
    except:
        pass # ignore

    tracks_100 = [tracks[i:i + 100] for i in range(0, len(tracks), 100)]

    # Read the Spotify credentials from a file
    sp, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET = None, None, None

    try:
        lines = open("./spotify_credentials.txt", "r").readlines()
        SPOTIFY_CLIENT_ID = lines[0].strip()
        SPOTIFY_CLIENT_SECRET = lines[1].strip()
    except:
        log("Could not read Spotify credentials file", "error")
        return None

    # Authenticate with the Spotify API
    try:
        auth_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=auth_manager)
    except:
        log("Could not authenticate with Spotify API", "error")
        return None

    # Get the metadata for each track
    audio_features = pd.DataFrame(columns = ["uri", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms"])
    try:
        desc = log(f"Getting {spotify} track metadata from server ", "status", ret_str=True)
        progress = track(tracks_100, description=desc, transient=True)
        for spotify_track in progress:
            while True:
                try:
                    new_features = sp.audio_features(spotify_track)
                    new_features = pd.DataFrame.from_dict(new_features)
                    audio_features = pd.concat([audio_features, new_features], join="inner", sort=True)
                    break
                except:
                    # The Spotify API rate limit is not publicly documented, but this seems to work
                    time.sleep(20)
    except:
        log(f"Could not get {spotify} track metadata from server", "error")
        return None

    try:
        # create common column "track_id"
        audio_features["uri"] = audio_features["uri"].apply(lambda uri: uri.split(":")[-1])
        audio_features.rename(columns={"uri": "track_id"}, inplace=True)
        # Store metadata in the database
        audio_features.to_sql("audio_features", engine, if_exists="replace", index=False)
    except:
        log(f"Could not store {spotify} track metadata in database", "error")
        return None

    log(f"Extracted {spotify} track metadata", "success")

    # brief summary of spotify's audio features:
    # "acousticness": A measure from 0.0 to 1.0 indicating the confidence of whether a track is acoustic, with 1.0 representing high confidence in its acoustic nature.
    # "analysis_url": A URL providing access to the full audio analysis of a track.
    # "danceability": A number from 0.0 to 1.0 describing how suitable a track is for dancing based on tempo, rhythm stability, beat strength, and regularity.
    # "duration_ms": The duration of the track in milliseconds.
    # "energy": A measure from 0.0 to 1.0 representing the intensity and activity level of a track, with higher values indicating greater energy.
    # "id": The unique Spotify ID assigned to a track.
    # "instrumentalness": A measure from 0.0 to 1.0 predicting the likelihood of a track containing no vocal content, with higher values suggesting instrumental tracks.
    # "key": The key in which the track is performed, mapped to standard Pitch Class notation.
    # "liveness": A number from 0.0 to 1.0 indicating the probability of a track being performed live, with higher values suggesting a live recording.
    # "loudness": The overall loudness of a track in decibels (dB), ranging from -60 to 0 dB.
    # "mode": An integer representing the modality (major or minor) of a track, with 1 for major and 0 for minor.
    # "speechiness": A number from 0.0 to 1.0 indicating the presence of spoken words in a track, with higher values suggesting more speech-like recordings.
    # "tempo": The estimated tempo of a track in beats per minute (BPM).
    # "time_signature": An estimated time signature specifying the number of beats in each bar, ranging from 3 to 7.
    # "track_href": A link to the Web API endpoint providing detailed information about the track.
    # "type": The object type, which is "audio_features" for audio feature objects.
    # "uri": The Spotify URI for the track.
    # "valence": A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track, with higher values indicating more positive emotions.
    # for a full description of the audio features, see https://developer.spotify.com/documentation/web-api/reference/get-audio-features


if __name__ == "__main__":
    main()
