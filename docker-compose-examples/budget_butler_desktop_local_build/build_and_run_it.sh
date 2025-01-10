#!/bin/bash
set -ue

pushd .
pushd ../../

docker build -t local-budgetbutler-desktopapp -f Dockerfile.desktopapp . --no-cache

popd

docker-compose up -d
