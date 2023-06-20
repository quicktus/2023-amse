# use Python 3.11
import pandas as pd
import sqlalchemy as sa

# Automated data pipeline for the following source:
# https://mobilithek.info/offers/-655945265921899037

# $ chardetect 46251-0021_00.csv
# 'encoding': 'ISO-8859-1', 'confidence': 0.7283978470743464, 'language': ''}

SOURCE_URI: str = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv"


def main():
    # download the CSV file from SOURCE_URI
    df = pd.read_csv(SOURCE_URI, sep=";", encoding="ISO-8859-1")
    print(df)

    # Write the data into the SQLite database and assign fitting types using pandas
    engine = sa.create_engine("sqlite:///cars.sqlite")
    df.to_sql("cars", engine, if_exists="replace", index=False)  # TODO


if __name__ == "__main__":
    main()
