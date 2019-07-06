#!/usr/bin/env bash
set -e
sudo apt update

sudo apt-get install curl php5-cli git
curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer


sudo apt install npm chromium-browser


# Installation
echo "create butler_online"
pushd butler_all_online_api/api
composer install
popd ..


echo "create app"
pushd butler_all_online/budgetbutler

npm install -g @angular/cli


ng install
ng build --prod

export CHROME_BIN=/usr/bin/chromium-browser
ng test --watch=false
