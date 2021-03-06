#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/setting.sh"
source $IMPORT_VIRTUALENVWRAPPER
source $IMPORT_RVM

fuser -k $PORT_LMS_PREVIEW/tcp
# kill -9 $(ps -ef|grep -E '$PORT_LMS_PREVIEW'|grep -v grep|awk '{print $2}')

workon $ENV_PYTHON
rvm use $RVM_EDX_PLATFORM

cd "$PROJECT_HOME/edx-platform"

if [ $DEBUG -eq 1 ]; then
    ./manage.py lms runserver 127.0.0.1:$PORT_LMS_PREVIEW --settings=cms.staging --pythonpath=. --nothreading
else
    gunicorn lms.wsgi:application --workers=8 -b 0.0.0.0:$PORT_LMS_PREVIEW
fi
