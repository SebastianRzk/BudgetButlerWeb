set -e
pytest --cov=mysite --cov-report xml:coverage/cov.xml
sonar-scanner -Dsonar.login=$SONAR
