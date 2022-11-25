#!/usr/bin/env bash

set -e
cd butler_offline &&  FLASK_APP=start_as_flask.py flask run > build.log&


cd butler_offline_selenium_tests
pytest -v
cd ..
