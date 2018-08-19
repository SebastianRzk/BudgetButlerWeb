set -e

wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
export PATH=$PATH:$(pwd)/geckodriver

echo "PATH:"
echo $PATH

cd mysite && python manage.py runserver > build.log &

cd selenium_tests
pytest
cd ..
