#!/bin/bash

# Check if config.py exists
if [ ! -f config.py ]; then
    # config.py doesn't exist, create a new one with default values
    cat <<EOF > config.py
# Configuration file

# OpenAI API key
OPENAI_API_KEY = ""

# MML model file path
MML_MODEL_FILE = ""

# Prompt file path
PROMPT_FILE = "prompt.txt"

# IP address and port
IP_ADDRESS = ""
PORT = 8081
EOF
fi

# Read the existing values from config.py
EXISTING_OPENAI_API_KEY=$(grep -oP 'OPENAI_API_KEY = "\K[^"]*' config.py)
EXISTING_MML_MODEL_FILE=$(grep -oP 'MML_MODEL_FILE = "\K[^"]*' config.py)
EXISTING_IP_ADDRESS=$(grep -oP 'IP_ADDRESS = "\K[^"]*' config.py)
EXISTING_PORT=$(grep -oP 'PORT = \K[^"]*' config.py)

# Prompt the user for new values if they don't exist or ask to use existing values
OPENAI_API_KEY=${EXISTING_OPENAI_API_KEY}
if [ -z "$OPENAI_API_KEY" ]; then
    read -p "Enter the OpenAI API key: " OPENAI_API_KEY
fi

MML_MODEL_FILE=${EXISTING_MML_MODEL_FILE}
if [ -z "$MML_MODEL_FILE" ]; then
    read -p "Enter the MML model file path: " MML_MODEL_FILE
fi

PROMPT_FILE="prompt.txt"

IP_ADDRESS=${EXISTING_IP_ADDRESS}
if [ -z "$IP_ADDRESS" ]; then
    read -p "Enter the IP address: " IP_ADDRESS
fi

PORT=${EXISTING_PORT}
if [ -z "$PORT" ]; then
    read -p "Enter the port: " PORT
fi

# Write the updated values to config.py
cat <<EOF > config.py
# Configuration file

# OpenAI API key
OPENAI_API_KEY = "$OPENAI_API_KEY"

# MML model file path
MML_MODEL_FILE = "$MML_MODEL_FILE"

# Prompt file path
PROMPT_FILE = "$PROMPT_FILE"

# IP address and port
IP_ADDRESS = "$IP_ADDRESS"
PORT = $PORT
EOF
