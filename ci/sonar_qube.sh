set -e
pytest --cov=src --cov-report xml:coverage/cov.xml
sonar-scanner -Dsonar.login=$SONAR
