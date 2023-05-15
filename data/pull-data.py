# Required Data:
#  - Rain           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/more_precip/
#  - Sun / Cloud    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/
#  - Temperature    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/
#  - Wind           https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/wind/

# Weather Acronyms:
# https://www.noaa.gov/jetstream/appendix/weather-acronyms

from ftplib import FTP
from rich.progress import track
import pandas as pd
import os
import zipfile
import sqlalchemy as sa
from logger import log

# globals
raw_dir: str = "raw"
db_connection_uri = "sqlite:///../data.sqlite"
engine = sa.create_engine(db_connection_uri)

def main():
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

    log(f"Pipeline started", timestamp=True)

    for data_src in data_sources:
    # NOTE: If you suspect any issues with the downloaded files, you can delete or move the respective directory
    #       containing the downloaded files. Running the script again will re-download the contents of the directory.

        if(os.path.exists(os.path.join(raw_dir, data_src['name']))):
            log(f"Found {data_src['name']} files", "success")
        else:
            download(ftp_uri, data_src['name'], data_src['path'])
            log(f"Downloaded {data_src['name']}", "success")

        if sa.inspect(engine).has_table(data_src["name"]):
            log(f"Found {data_src['name']} table", "success")
        else:
            extract_to_db(data_src['name'], data_src['columns'])
            log(f"Extracted {data_src['name']}", "success")

    log(f"Pipeline completed", timestamp=True)


def download(ftp_uri: str, data_src_name: str, path: str):
    # Connect to FTP server and navigate to the target directory
    ftp = FTP(ftp_uri)
    ftp.login()
    folder_path, file_name = os.path.split(path)
    ftp.cwd(folder_path)

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


def extract_to_db(data_src_name: str, filter_items: str):
    folder: str = os.path.join(raw_dir, data_src_name)
    # Get a list of all zip files in the folder
    zip_files = [file for file in os.listdir(folder) if file.endswith(".zip")]
    # Iterate over the zips with a progress bar
    desc = log(f"Extracting {data_src_name} into database ", "status", ret_str=True)
    for zip_file in track(zip_files, description=desc, transient=True):
        zip_path: str = os.path.join(folder, zip_file)
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


if __name__ == "__main__":
    main()
