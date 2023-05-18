# use Python 3.11
import pandas as pd
import sqlalchemy as sa

# Automated data pipeline for the following source:
# https://mobilithek.info/offers/-8691940611911586805
# which is derived from https://openflights.org/data.html

SOURCE_URI: str = "https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv"

def main():
    # download the CSV file from SOURCE_URI
    df = pd.read_csv(SOURCE_URI, sep=";")

    # Rename the columns
    df = df.rename(columns={
        "column_1": "airport_id",
        "column_2": "name",
        "column_3": "city",
        "column_4": "country",
        "column_5": "iata",
        "column_6": "icao",
        "column_7": "latitude",
        "column_8": "longitude",
        "column_9": "altitude",
        "column_10": "timezone",
        "column_11": "dst",
        "column_12": "tz_database_timezone",
        "geo_punkt": "geopunkt"
    })

    # Write the data into the SQLite database and assign fitting types using pandas
    engine = sa.create_engine("sqlite:///airports.sqlite")
    df.to_sql("airports", engine, if_exists="replace", index=False, dtype={
            "airport_id"            : sa.types.INTEGER, # Unique OpenFlights identifier for this airport.
            "name"                  : sa.types.TEXT,    # Name of airport. May or may not contain the City name.
            "city"                  : sa.types.TEXT,    # Main city served by airport. May be spelled differently from Name.
            "country"               : sa.types.TEXT,    # Country or territory where airport is located. See Countries to cross-reference to ISO 3166-1 codes. 
            "iata"                  : sa.types.TEXT,    # 3-letter IATA code. Null if not assigned/unknown.
            "icao"                  : sa.types.TEXT,    # 4-letter ICAO code. Null if not assigned.
            "latitude"              : sa.types.FLOAT,   # Decimal degrees, usually to six significant digits. Negative is South, positive is North.
            "longitude"             : sa.types.FLOAT,   # Decimal degrees, usually to six significant digits. Negative is West, positive is East.
            "altitude"              : sa.types.INTEGER, # In feet.
            "timezone"              : sa.types.FLOAT,   # Hours offset from UTC. Fractional hours are expressed as decimals, eg. India is 5.5.
            "dst"                   : sa.types.CHAR,    # Daylight savings time. One of E (Europe), A (US/Canada), S (South America), O (Australia), Z (New Zealand), N (None) or U (Unknown).
            "tz_database_timezone"  : sa.types.TEXT,    # Timezone in "tz" (Olson) format, eg. "America/Los_Angeles".
            "geopunkt"              : sa.types.TEXT,    # (redundant) Latitude and longitude separated by a comma
        })

if __name__ == "__main__":
    main()