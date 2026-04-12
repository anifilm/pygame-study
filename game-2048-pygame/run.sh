#!/bin/bash

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH"
    exit 1
fi

# Check if pygame environment is active
# Redirect stderr to /dev/null to suppress conda warnings
CURRENT_ENV=$(conda info --envs 2>/dev/null | grep "*" | awk '{print $1}')

if [ "$CURRENT_ENV" != "pygame" ]; then
    echo "Activating pygame environment..."
    # Source the conda.sh script to enable conda activate in the script
    source "$(conda info --base 2>/dev/null)/etc/profile.d/conda.sh"
    conda activate pygame 2>/dev/null

    # Check if activation was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to activate pygame environment"
        exit 1
    fi
fi

# Run the Python script
python ./scripts/main.py
