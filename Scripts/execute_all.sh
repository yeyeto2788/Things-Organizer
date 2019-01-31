echo off

echo "Running pylint"
pylint -f parseable --rcfile=.pylintrc things_organizer | tee .\pylint.txt

echo "Running tests"
py.test -v --junitxml unittests.xml --cov=things_organizer --cov-config .coveragerc --cov-report xml --cov-report term