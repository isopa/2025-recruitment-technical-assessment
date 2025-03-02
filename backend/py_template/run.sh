#!/usr/bin/env bash

function cleanup {
    echo
    echo "Deactivating virtual environment..."
    echo "If still stuck with (.venv) type 'deactivate'!"
    deactivate
}

# Creates and activates a virtual env
python -m venv venv
venv/Scripts/activate

# Install dependencies and runs
pip install -r requirements.txt
python devdonalds.py

trap cleanup EXIT



