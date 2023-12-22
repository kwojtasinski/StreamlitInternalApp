#!/bin/bash
set -xe
if command -v poetry &> /dev/null
then
    VERSION=${1:-`poetry version -s`}
else
    VERSION=${1:-ci}
fi

if command -v docker &> /dev/null
then
    docker build . -t streamlit_internal_app:$VERSION-development -f dev.Dockerfile
    docker build . --build-arg PACKAGE_VERSION=$VERSION -t streamlit_internal_app:$VERSION-latest
fi
