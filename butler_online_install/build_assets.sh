#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~~~~~Assets~~~~~~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
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

