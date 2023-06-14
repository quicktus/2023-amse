import os
from sqlalchemy import create_engine, inspect
import pytest  # noqa: F401


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
