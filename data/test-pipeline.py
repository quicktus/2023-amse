import os
from sqlalchemy import create_engine, inspect
import pytest

def db_test():
    assert os.path.exists("data.sqlite")

    # Create the SQLAlchemy engine
    engine = create_engine("sqlite:///data.sqlite")

    # Create the SQLAlchemy inspector
    inspector = inspect(engine)

    # Define the expected table names
    expected_tables = [
        "cloud_data",
        "rain_data",
        "temperature_data",
        "wind_data",
        "audio_features",
        "spotify_data"
    ]

    # Get the list of table names from the database
    table_names = inspector.get_table_names()

    # Check if all expected tables exist in the database
    for table_name in expected_tables:
        assert table_name in table_names
import os
from sqlalchemy import create_engine, inspect
import pytest

def test_db():
    # Check if the database file exists
    assert os.path.exists("../data.sqlite")

    engine = create_engine("sqlite:///../data.sqlite")
    inspector = inspect(engine)

    expected_tables = [
        "cloud_data",
        "rain_data",
        "temperature_data",
        "wind_data",
        "audio_features",
        "spotify_data"
    ]

    table_names = inspector.get_table_names()

    # Check if all expected tables exist in the database
    for table_name in expected_tables:
        assert table_name in table_names
    print("Success!")