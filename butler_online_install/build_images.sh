#!/bin/bash
set -e

docker build -t budget-butler-fpm -f Dockerfile.fpm .
docker build -t budget-butler-static -f Dockerfile.static .
