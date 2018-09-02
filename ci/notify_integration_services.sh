
#!/bin/sh


sh ci/run_unit_tests.sh
sh ci/sonar_qube.sh
coveralls
codecov
