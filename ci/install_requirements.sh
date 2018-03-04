set -e
pip install -r ci/integration-requirements.txt
pip install coveralls
pip install codecov
sudo apt-get install chromium-browser chromium-chromedriver
