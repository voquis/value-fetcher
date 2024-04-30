#!/bin/bash
set -euo pipefail

# Assumes the src contains a single package to be built
PACKAGE_PATH=$(find src/* -type d | head -n 1)
PACKAGE_NAME=${PACKAGE_PATH#src/}
echo "Using package name: $PACKAGE_NAME"

# Install development dependencies with pip
pip install .[dev]

# Run formatting checks
flake8

# Run linting checks
black --check --diff .
pylint src tests

# Run tests and generate coverage reports
pytest --cov="$PACKAGE_NAME" \
  --cov-report term \
  --cov-report html \
  --cov-fail-under=100.00

# Check the build
python -m build
twine check --strict dist/*
