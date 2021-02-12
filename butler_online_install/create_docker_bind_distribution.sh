#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~~Bind Edition~~~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"


mkdir -p butler_online_distribution/docker_bind_edition/budget_butler/src/api
cp -r butler_online_install/docker_bind_edition/* butler_online_distribution/docker_bind_edition/
cp -r butler_online_api/api/* butler_online_distribution/docker_bind_edition/budget_butler/src/api
cp -r butler_online/budgetbutler/dist/* butler_online_distribution/docker_bind_edition/budget_butler/src/
cp butler_online_distribution/docker_bind_edition/budget_butler/src/api/robots.txt butler_online_distribution/docker_bind_edition/budget_butler/src/
rm butler_online_distribution/docker_bind_edition/budget_butler/src/3rdpartylicenses.txt

