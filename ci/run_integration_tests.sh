#!/usr/bin/env bash

set -e
flask --app butler_offline run&


cd butler_offline_selenium_tests
pytest -v
cd ..
