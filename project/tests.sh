#!/bin/bash

cd data
python pull-data.py --clean
pytest -k test_db test-pipeline.py
