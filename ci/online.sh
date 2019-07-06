#!/usr/bin/env bash
set -e
sudo apt update

sudo apt-get install curl php7.0-cli git
curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer

# Installation
echo "create butler_online"
cd butler_all_online_api/api
composer install
cd -


echo "create app"
cd butler_all_online/budgetbutler

npm install -g @angular/cli


npm install
ng build --prod

ng test --watch=false --progress=false --browsers=ChromeHeadlessCI
