#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

echo "Löschen von alten ergebnissen"
rm -rfv butler_online_distribution

echo "build php api"
cd butler_online_api/api/
composer install
cd -

echo "build ng frontend"
cd butler_online/budgetbutler
#npm install
#ng build --prod
cd -

echo "create webspace edition"
mkdir butler_online_distribution
mkdir butler_online_distribution/webspace_edition
mkdir butler_online_distribution/webspace_edition/api
cp -r butler_online_api/api/* butler_online_distribution/webspace_edition/api
cp -r butler_online/budgetbutler/dist/* butler_online_distribution/webspace_edition/
cp butler_online_distribution/webspace_edition/api/robots.txt butler_online_distribution/webspace_edition/
cp butler_online_install/.htaccess butler_online_distribution/webspace_edition/
rm butler_online_distribution/webspace_edition/3rdpartylicenses.txt

echo "create docker edition"
mkdir butler_online_distribution/docker_edition
mkdir butler_online_distribution/docker_edition/src/
mkdir butler_online_distribution/docker_edition/src/api
cp -rv butler_online_install/docker_edition/* butler_online_distribution/docker_edition/
cp -rv butler_online_api/api/* butler_online_distribution/docker_edition/src/api
cp -rv butler_online/budgetbutler/dist/* butler_online_distribution/docker_edition/src/
cp butler_online_distribution/docker_edition/src/api/robots.txt butler_online_distribution/docker_edition/src/
rm butler_online_distribution/docker_edition/src/3rdpartylicenses.txt


echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~~Done Building~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

