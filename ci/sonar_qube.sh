#!/usr/bin/env bash

set -e
pytest butler_offline --cov=butler_offline --cov-report xml:coverage/cov.xml
sonar-scanner -Dsonar.login=$SONAR
