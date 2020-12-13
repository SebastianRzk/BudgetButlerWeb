#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "-  ---------incremental docker build------------"
echo "------------------------------------------------"


echo "build php api"
cd butler_online_api/api/
composer install
cd -

echo "build ng frontend"
cd butler_online/budgetbutler
npm install
ng build --prod
cd -

echo "create docker edition"
rm -rfv butler_online_distribution/docker_edition/budget_butler/src
mkdir butler_online_distribution/docker_edition/budget_butler/src/
mkdir butler_online_distribution/docker_edition/budget_butler/src/api

rm -rfv butler_online_distribution/docker_edition/budget_butler/php-fpm-image
cp -r butler_online_install/docker_edition/budget_butler/php-fpm-image butler_online_distribution/docker_edition/budget_butler

rm -fv butler_online_distribution/docker_edition/budget_butler/site.conf
cp -r butler_online_install/docker_edition/budget_butler/site.conf butler_online_distribution/docker_edition/budget_butler


cp -r butler_online_api/api/* butler_online_distribution/docker_edition/budget_butler/src/api
cp -r butler_online/budgetbutler/dist/* butler_online_distribution/docker_edition/budget_butler/src/
cp butler_online_distribution/docker_edition/budget_butler/src/api/robots.txt butler_online_distribution/docker_edition/budget_butler/src/
rm butler_online_distribution/docker_edition/budget_butler/src/3rdpartylicenses.txt


echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~~Done Building~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

