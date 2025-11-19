#!/bin/bash
# Startup script for Databricks App

# Install dependencies
pip install -r requirements.txt

# Start the Flask application
python app.py

