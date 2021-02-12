#!/usr/bin/env bash
set -e
sudo apt update

sudo apt-get install curl php-cli git
curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer

# Installation
echo "create butler_online"
cd butler_online_api/api
composer install
cd -


echo "create app"
cd butler_online/budgetbutler

npm install -g @angular/cli


npm install
ng build --prod

ng test --watch=false --progress=false --browsers=ChromeHeadlessCI

cd ..
cd ..
sh butler_online_install/clean_compose.sh
