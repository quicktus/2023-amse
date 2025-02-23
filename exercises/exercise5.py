# use Python 3.11
import os
import pandas as pd
import sqlalchemy as sa
import time
import urllib.request
import zipfile

# Automated data pipeline for the following source:
# https://mobilithek.info/offers/110000000002933000

SOURCE_URI: str = "https://gtfs.rhoenenergie-bus.de/GTFS.zip"
ZIP_FILE_NAME: str = "GTFS.zip"


def main():
    # download the ZIP file from SOURCE_URI
    for attempts in range(10):
        try:
            urllib.request.urlretrieve(SOURCE_URI, ZIP_FILE_NAME)
        except:
            time.sleep(0.25 * attempts)  # backoff icreasingly
            continue
        else:
            break

    assert os.path.isfile(ZIP_FILE_NAME), f"{ZIP_FILE_NAME} not found - download failed"

    df: pd.DataFrame = None

    # pick out stops.txt from the ZIP file
    with zipfile.ZipFile(ZIP_FILE_NAME, "r") as zip_ref:
        with zip_ref.open(name="stops.txt", mode="r") as tmpfile:
            df = pd.read_csv(tmpfile)

    assert df is not None, f"stops.txt not found in {ZIP_FILE_NAME}"

    # Only keep the columns stop_id, stop_name, stop_lat, stop_lon, zone_id
    df = df[["stop_id", "stop_name", "stop_lat", "stop_lon", "zone_id"]]

    # Adapt data types
    df["stop_id"] = df["stop_id"].astype(int)
    df["stop_name"] = df["stop_name"].astype(str)
    df["stop_lat"] = df["stop_lat"].astype(float)
    df["stop_lon"] = df["stop_lon"].astype(float)
    df["zone_id"] = df["zone_id"].astype(int)

    # Only keep stops from zone 2001
    df = df[df["zone_id"] == 2001]
    print(df)

    # stop_lat/stop_lon must be a geographic coordinates between -90 and 90, including upper/lower bounds
    df = df[(df["stop_lat"] >= -90) & (df["stop_lat"] <= 90)]
    df = df[(df["stop_lon"] >= -90) & (df["stop_lon"] <= 90)]

    # assign fitting SQLite types
    dtypes = {"stop_id": sa.types.BIGINT,
              "stop_name": sa.types.TEXT,
              "stop_lat": sa.types.FLOAT,
              "stop_lon": sa.types.FLOAT,
              "zone_id": sa.types.BIGINT}

    # Write the data into the SQLite database using pandas
    engine = sa.create_engine("sqlite:///gtfs.sqlite")
    df.to_sql("stops", engine, if_exists="replace", index=False, dtype=dtypes)

    # delete the ZIP file
    os.remove(ZIP_FILE_NAME)


if __name__ == "__main__":
    main()
