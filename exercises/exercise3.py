# use Python 3.11
import pandas as pd
import sqlalchemy as sa

# Automated data pipeline for the following source:
# https://mobilithek.info/offers/-655945265921899037

# encoding: chardetect 46251-0021_00.csv {'encoding': 'ISO-8859-1', 'confidence': 0.7283978470743464, 'language': ''}
# CIN: https://en.wikipedia.org/wiki/Community_Identification_Number

SOURCE_URI: str = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv"


def main():
    excel_cols = ["A", "B", "C", "M", "W", "AG", "AQ", "BA", "BK", "BU"]
    col_indices = [excel_col_to_idx(col) for col in excel_cols]
    col_names = ["date", "CIN", "name", "petrol", "diesel", "gas", "electro", "hybrid", "plugInHybrid", "others"]
    col_sqlite_types = [sa.types.TEXT, sa.types.TEXT, sa.types.TEXT, sa.types.INTEGER, sa.types.INTEGER, sa.types.INTEGER,
                        sa.types.INTEGER, sa.types.INTEGER, sa.types.INTEGER, sa.types.INTEGER]

    # Download CSV file and reshape df
    df = pd.read_csv(SOURCE_URI, sep=";", encoding="ISO-8859-1", skiprows=7, skipfooter=4, engine="python", usecols=col_indices,
                     names=col_names, dtype={"CIN": str}, na_values="-")

    # Validate data and drop invalid rows
    # CINs are strings with 5 characters all of which are digits (and can have a leading 0)
    df = df[df["CIN"].str.match(r"\d{5}$")]

    # All other cols should be positive integers > 0
    df = df.dropna()

    mask = df.iloc[:, 3:].gt(0).any(axis=1)
    df = df[mask]

    # Write the data into the SQLite database and assign fitting types
    engine = sa.create_engine("sqlite:///cars.sqlite")
    df.to_sql("cars", engine, if_exists="replace", index=False, dtype=dict(zip(col_names, col_sqlite_types)))


def excel_col_to_idx(column):
    return sum((ord(char) - 64) * (26 ** i) for i, char in enumerate(reversed(column))) - 1


if __name__ == "__main__":
    main()
