#!/bin/bash
set -xe
echo "Running black check"
poetry run black --check .
echo "Running ruff check"
poetry run ruff check .
