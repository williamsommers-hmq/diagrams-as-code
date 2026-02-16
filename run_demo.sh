#!/bin/bash
set -e

echo "Setting up environment..."

# Check for virtual environment
if [ -d ".venv" ]; then
    echo "Using virtual environment at .venv"
    source .venv/bin/activate
else
    echo "No virtual environment found. Please create one with 'python3 -m venv .venv'"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import diagrams" &> /dev/null; then
    echo "Installing diagrams library..."
    pip install diagrams
fi

echo "Running demo script..."
python3 demo.py

if [ -f "images/demo_architecture.png" ] || [ -f "images/demo_architecture_transparent.png" ]; then
    echo "Success! Diagram created in $(pwd)/images/"
else
    echo "Error: Diagram file not found in images/."
    exit 1
fi
