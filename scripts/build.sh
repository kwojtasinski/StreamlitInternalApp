#!/bin/bash
set -xe
VERSION=${1:-`poetry version -s`}
poetry version $VERSION
poetry build

if command -v docker &> /dev/null
then
    docker build . -t streamlit_internal_app:$VERSION-development -f dev.Dockerfile
    docker build . --build-arg PACKAGE_VERSION=$VERSION -t streamlit_internal_app:$VERSION-latest
fi
