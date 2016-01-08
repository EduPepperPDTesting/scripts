#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/setting.sh"
source $IMPORT_VIRTUALENVWRAPPER
source $IMPORT_RVM

fuser -k $PORT_LMS/tcp
# kill -9 $(ps -ef|grep -E "$PORT_LMS"|grep -v grep|awk '{print $2}')

workon $ENV_PYTHON
rvm use $RVM_EDX_PLATFORM

cd "$PROJECT_HOME/edx-platform"

# ./manage.py lms runserver 127.0.0.1:8000 --settings=cms.staging --pythonpath=. --nothreading
gunicorn lms.wsgi:application --workers=8 -b localhost:$PORT_LMS
