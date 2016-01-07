PROJECT_HOME=/home/tahoe/edx_all
ENV_PYTHON=edx-platform

IMPORT_VIRTUALENVWRAPPER=/usr/bin/virtualenvwrapper.sh
IMPORT_RVM=/home/tahoe/.rvm/scripts/rvm

PORT_LMS=8000
PORT_CMS=8001
PORT_LMS_PREVIEW=8002
PORT_XQUEUE=8003
PORT_ORA=8004
PORT_DISCUSS=8005

RVM_EDX_PLATFORM="ruby-1.9.3-p448"
RVM_DISCUSS="ruby-1.9.3-p448@cs_comments_service"

export XQUEUE_DB_NAME="xqueue"
export XQUEUE_DB_USER="pepper"
export XQUEUE_DB_PASSWORD="lebbeb"
export XQUEUE_DB_HOST="mysql"
export XQUEUE_DB_PORT="3306"

export ESSAY_DB_NAME="xqueue"
export ESSAY_DB_USER="pepper"
export ESSAY_DB_PASSWORD="lebbeb"
export ESSAY_DB_HOST="mysql"
export ESSAY_DB_PORT="3306"

export XQUEUE_URL="http://127.0.0.1:$PORT_XQUEUE"
export GRADING_CONTROLLER_INTERFACE_URL="http://127.0.0.1:$PORT_ORA"
