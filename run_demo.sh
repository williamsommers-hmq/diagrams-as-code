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

if [ -f "demo_architecture.png" ]; then
    echo "Success! Diagram created at $(pwd)/demo_architecture.png"
else
    echo "Error: Diagram file not found."
    exit 1
fi
