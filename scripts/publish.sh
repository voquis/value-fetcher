#!/bin/bash

set -euo pipefail

# Install dependencies, excluding development dependencies
poetry install --no-dev --no-root

# Publish package to pypi python repository
poetry publish --build --username="${PYTHON_REPOSITORY_USERNAME}" --password="${PYTHON_REPOSITORY_PASSWORD}"
