#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~Webspace Edition~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"


mkdir -p butler_online_distribution/webspace_edition/api
cp -r butler_online_api/api/* butler_online_distribution/webspace_edition/api
cp -r butler_online/budgetbutler/dist/* butler_online_distribution/webspace_edition/
cp butler_online_distribution/webspace_edition/api/robots.txt butler_online_distribution/webspace_edition/
cp butler_online_install/.htaccess butler_online_distribution/webspace_edition/
rm butler_online_distribution/webspace_edition/3rdpartylicenses.txt

