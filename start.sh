#!/bin/bash

# Create and activate a temporary virtual environment
python3 -m venv env
source env/bin/activate

# Upgrade pip and install required packages
python3 -m pip install --upgrade pip
export CMAKE_ARGS="-DLLAMA_CUBLAS=on"
export FORCE_CMAKE=1
python3 -m pip install pandas pytrends matplotlib pillow openai Flask scikit-learn llama-cpp-python transformers torch

# Run the Python script
python3 app.py

# Deactivate and delete the temporary virtual environment
deactivate
rm -r env
