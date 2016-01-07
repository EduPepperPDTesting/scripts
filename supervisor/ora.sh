#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/setting.sh"
source $IMPORT_VIRTUALENVWRAPPER

fuser -k $PORT_ORA/tcp
# kill -9 $(ps -ef|grep -E "$PORT_ORA"|grep -v grep|awk '{print $2}')

workon $ENV_PYTHON
cd "$PROJECT_HOME/edx-ora"

#python manage.py runserver 127.0.0.1:8004 --settings=edx_ora.settings --pythonpath=.
gunicorn edx_ora.wsgi:application --workers=8 -b localhost:$PORT_ORA
