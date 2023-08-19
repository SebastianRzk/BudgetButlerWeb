#!/bin/bash

pushd .
pushd ../../

docker build -t budget-butler-fpm -f Dockerfile.fpm .
docker build -t budget-butler-static -f Dockerfile.static .

popd

docker-compose up -d
