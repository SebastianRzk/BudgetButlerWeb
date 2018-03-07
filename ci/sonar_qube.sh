set -e
pytest mysite --cov=mysite --cov-report xml:coverage/cov.xml
sonar-scanner -Dsonar.login=$SONAR
