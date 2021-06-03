#!/bin/bash

echo "Split data by timestamp"
python -u group_by_timestamp.py /data/input /data/_output/csv

echo "Create PG-JSON representation"
python -u json-pg-serialize.py /data/_output/csv /data/output/json-pg

