#!/bin/bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/setting.sh"
source $IMPORT_VIRTUALENVWRAPPER

fuser -k $PORT_XQUEUE/tcp
# kill -9 $(ps -ef|grep -E "$PORT_XQUEUE"|grep -v grep|awk '{print $2}')

workon $ENV_PYTHON

cd "$PROJECT_HOME/xqueue"

#python manage.py runserver 127.0.0.1:8003 --settings=xqueue.settings --pythonpath=. 
gunicorn xqueue.wsgi:application --workers=8 -b localhost:$PORT_XQUEUE
