set -e

# Installation
cd online_install

sudo apt update
sudo apt install apache2

python create_virtualhost.py
sudo cp budget.online.conf /etc/apache2/sites-available/

sudo a2ensite budget.online.conf
#sudo rm /etc/apache2/apache.conf 
sudo cp apache.conf /etc/apache2/

sudo service apache2 reload

pip install -r requirements.txt

python install_database.py


cd ..
cp -r online/* ./
curl 'localhost/login.php'
echo "DONE"

