#!/bin/bash

echo "Cleaning output folder"
rm -rf /data/output

echo "Split data by timestamp"
python -u group_by_timestamp.py

echo "Create PG-JSON representation"
python -u json-pg-serialize.py


