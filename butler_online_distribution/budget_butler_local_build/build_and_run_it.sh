#!/bin/bash

pushd .
pushd ../../

docker build -t local-budgetbutlerweb-companion-api -f Dockerfile.api . --no-cache
docker build -t local-budgetbutlerweb-companion-static  -f Dockerfile.static . --no-cache

popd

docker-compose up -d
