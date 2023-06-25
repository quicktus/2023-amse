#!/bin/bash

cd data
python pull-data.py --test
pytest -k test_db test-pipeline.py
