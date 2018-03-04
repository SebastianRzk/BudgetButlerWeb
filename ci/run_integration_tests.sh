set -e
cd mysite && python manage.py runserver > build.log &

cd selenium_tests
pytest
cd ..
