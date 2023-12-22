#!/bin/bash
set -xe
echo "Running black format"
poetry run black .
echo "Running ruff fix"
poetry run ruff --fix .
