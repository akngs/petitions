#!/usr/bin/env bash
python petition.py
aws s3 sync data s3://data10902/petition
