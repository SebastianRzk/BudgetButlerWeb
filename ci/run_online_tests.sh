set -e
cd online_install
sudo pip3 install requirements.txt
python3 install_database.py
cd ..
