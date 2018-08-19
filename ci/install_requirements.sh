set -e
pip install -r ci/integration-requirements.txt
pip install coveralls
pip install codecov
sudo apt-get update
sudo apt-get install firefox
