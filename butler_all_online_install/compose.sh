#!/bin/bash
set -e

echo "Löschen von alten ergebnissen"
rm -rfv butler_all_online_distribution

echo "build php api"
cd butler_all_online_api/api/
composer install
cd -

echo "build ng frontend"
npm install
cd butler_all_online/budgetbutler
ng build --prod
cd -

echo "create dist"
mkdir butler_all_online_distribution
mkdir butler_all_online_distribution/api
cp -r butler_all_online_api/api/* butler_all_online_distribution/api
cp -r butler_all_online/budgetbutler/dist/* butler_all_online_distribution
cp butler_all_online_distribution/api/robots.txt butler_all_online_distribution/
cp butler_all_online_install/.htaccess butler_all_online_distribution/
rm butler_all_online_distribution/3rdpartylicenses.txt

echo "server erstellt"
