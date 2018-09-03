set -e
cd online_install
sudo pip install requirements.txt
python install_database.py
cd ..
