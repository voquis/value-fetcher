#!/bin/bash
set -euo pipefail

# Install dependencies, including development dependencies
poetry install --no-root

# Run linting checks on package, tests and app entrypoint
poetry run pylint src tests

# Run tests and generate test coverage report
poetry run coverage run -m pytest tests
poetry run coverage html --omit="tests*"
poetry run coverage xml --omit="tests/*"
poetry run coverage report --omit="tests/*" --precision=2 --fail-under=100.00
