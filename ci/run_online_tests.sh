set -e

# Installation
cd online_install

sudo apt update
sudo apt install apache2

echo "Change online folder permissions"
pwd
ls -l "$TRAVIS_BUILD_DIR/online/"
chmod -R +rx "$TRAVIS_BUILD_DIR/online/" 
ls -l "$TRAVIS_BUILD_DIR/online/"


echo "Create virtualhost file"
python create_virtualhost.py
echo "move virtualhost file"
sudo cp budget.online.conf /etc/apache2/sites-available/
echo "installed confs:"
ls -l  /etc/apache2/sites-available/

echo "Enable site"
sudo a2ensite budget.online.conf
echo "Copy apache configuration"
sudo cp apache.conf /etc/apache2/

echo "reload apache"
sudo service apache2 reload

echo "install database"
pip install -r requirements.txt

python install_database.py
cd ..
echo "database installed"

echo "teste webseite"
curl 'localhost/login.php'

echo "error log:"
sudo cat /var/log/apache2/error.log

echo "DONE"

