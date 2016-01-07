#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/setting.sh"
source $IMPORT_VIRTUALENVWRAPPER
source $IMPORT_RVM

fuser -k $PORT_LMS/tcp
# kill -9 $(ps -ef|grep -E '$PORT_LMS_PREVIEW'|grep -v grep|awk '{print $2}')

workon $ENV_PYTHON
rvm use $RVM_EDX_PLATFORM

cd "$PROJECT_HOME/edx-platform"

./manage.py lms runserver 127.0.0.1:8002 --settings=cms.preview_dev --pythonpath=. --nothreading


