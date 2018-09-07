set -e

# Installation
echo "create online"
sh ci/install_online.sh

echo "create app"
cd online_install

sudo apt update
sudo apt install apache2 libapache2-mod-fastcgi 
sudo cp ~/.phpenv/versions/$(phpenv version-name)/etc/php-fpm.conf.default ~/.phpenv/versions/$(phpenv version-name)/etc/php-fpm.conf
sudo a2enmod rewrite actions fastcgi alias
echo "cgi.fix_pathinfo = 1" >> ~/.phpenv/versions/$(phpenv version-name)/etc/php.ini
sudo sed -i -e "s,www-data,travis,g" /etc/apache2/envvars
sudo chown -R travis:travis /var/lib/apache2/fastcgi
~/.phpenv/versions/$(phpenv version-name)/sbin/php-fpm
sudo chmod -R 777 /var/lib/apache2/fastcgi

echo "move virtualhost file"
sudo cp budget.online.conf /etc/apache2/sites-available/
echo "installed confs:"

echo "Enable site"
sudo a2ensite budget.online.conf

echo "reload apache"
sudo service apache2 reload

echo "install database"
pip install -r requirements.txt

python install_database.py
cd ..
echo "database installed"

echo "install online app"
sudo cp -rv ./online /var/www/budgetbutler


echo "apache error log before:"
sudo cat /var/log/apache2/error.log

echo "teste webseite"
curl 'localhost/login.php'

echo "error log:"
sudo cat /var/log/apache2/error.log

# tests
echo "start tests"
#pytest selenium_online
echo "tests deactivated"
echo "DONE"

