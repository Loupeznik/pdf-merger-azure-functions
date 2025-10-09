#!/bin/bash

set -e

VENV_DIR=".venv"

echo "Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing production dependencies..."
pip install -r requirements.txt

echo "Installing development dependencies..."
pip install -r requirements-dev.txt

echo ""
echo "Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To deactivate when done, run:"
echo "  deactivate"
