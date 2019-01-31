@ECHO off

ECHO "--------------------------------------------"
ECHO "---------------Running PyLint---------------"
ECHO "--------------------------------------------"
pylint -f parseable --rcfile=.pylintrc things_organizer > .\pylint.txt
@type .\pylint.txt


IF %ERRORLEVEL% NEQ 0 (
   ECHO
   ECHO "--------------------------------------------"
   ECHO "Trying to install PyLint"
   ECHO "--------------------------------------------"
   GOTO install_pylint
)

ECHO "--------------------------------------------"
ECHO "---------------Running tests----------------"
ECHO "--------------------------------------------"
py.test -v --junitxml unittests.xml --cov=things_organizer --cov-config .coveragerc --cov-report xml --cov-report term

IF %ERRORLEVEL% NEQ 0 (
   ECHO
   ECHO "--------------------------------------------"
   ECHO "Trying to install PyTest"
   ECHO "--------------------------------------------"
   GOTO install_pytest
)

ECHO "--------------------------------------------"
ECHO "-------Generating Documentation-------------"
ECHO "--------------------------------------------"
CD venv\Scripts\
ECHO "Activate the virtual environment"
activate.bat
CD ..\..\
ECHO "Running the script."
python ./generate_doc.py > .\doculog.txt

:install_pylint
pip install pylint
EXIT /B 0

:install_pytest
pip install -U --trusted-host 10.201.236.14 -i http://10.201.236.14:8000/simple pytest pytest-cov mock
EXIT /B 0
