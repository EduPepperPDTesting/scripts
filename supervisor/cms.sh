#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/setting.sh"
source $IMPORT_VIRTUALENVWRAPPER
source $IMPORT_RVM

fuser -k $PORT_CMS/tcp
# kill -9 $(ps -ef|grep -E "$PORT_CMS"|grep -v grep|awk '{print $2}')

workon $ENV_PYTHON
rvm use $RVM_EDX_PLATFORM

cd "$PROJECT_HOME/edx-platform"

if [ $DEBUG -eq 1 ]; then
    ./manage.py cms runserver 127.0.0.1:$PORT_CMS --settings=staging --pythonpath=. --nothreading
else
    gunicorn cms.wsgi:application --workers=8 -b localhost:$PORT_CMS
fi
