#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~Images Edition~~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

mkdir -p butler_online_distribution/docker_images_edition/budget_butler/images/src/api

cp -r butler_online_install/docker_images_edition/* butler_online_distribution/docker_images_edition/budget_butler
cp -r butler_online_api/api/* butler_online_distribution/docker_images_edition/budget_butler/images/src/api
cp -r butler_online/budgetbutler/dist/* butler_online_distribution/docker_images_edition/budget_butler/images/src/
cp butler_online_distribution/docker_images_edition/budget_butler/images/src/api/robots.txt butler_online_distribution/docker_images_edition/budget_butler/images/src/
rm butler_online_distribution/docker_images_edition/budget_butler/images/src/3rdpartylicenses.txt


cp -r butler_online_distribution/docker_images_edition/budget_butler/images/src/  butler_online_distribution/docker_images_edition/budget_butler/images/budget-butler-fpm
cp -r butler_online_distribution/docker_images_edition/budget_butler/images/src/  butler_online_distribution/docker_images_edition/budget_butler/images/budget-butler-static


