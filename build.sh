#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt

python src/cleaning.py
python src/feature_engineering.py
python src/location_normalization.py