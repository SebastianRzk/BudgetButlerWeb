#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~~Update Images~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"
rm -rfv butler_online_distribution/docker_images_edition/budget_butler/images/
sh butler_online_install/build_assets.sh


mkdir -p butler_online_distribution/docker_images_edition/budget_butler/images/src/api

cp -r butler_online_install/docker_images_edition/images/* butler_online_distribution/docker_images_edition/budget_butler/images
cp -r butler_online_api/api/* butler_online_distribution/docker_images_edition/budget_butler/images/src/api
cp -r butler_online/budgetbutler/dist/* butler_online_distribution/docker_images_edition/budget_butler/images/src/
cp butler_online_distribution/docker_images_edition/budget_butler/images/src/api/robots.txt butler_online_distribution/docker_images_edition/budget_butler/images/src/
rm butler_online_distribution/docker_images_edition/budget_butler/images/src/3rdpartylicenses.txt


cp -r butler_online_distribution/docker_images_edition/budget_butler/images/src/  butler_online_distribution/docker_images_edition/budget_butler/images/budget-butler-fpm
cp -r butler_online_distribution/docker_images_edition/budget_butler/images/src/  butler_online_distribution/docker_images_edition/budget_butler/images/budget-butler-static


echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~~Images Updated~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"
