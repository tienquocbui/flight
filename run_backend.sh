#!/bin/bash

# Install dependencies if not already installed
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set PYTHONPATH and run backend
echo "Starting Air Traffic Control Backend..."
export PYTHONPATH=src
cd src
uvicorn api:app --reload --host 0.0.0.0 --port 8000 