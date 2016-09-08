# Modify these variables to fit the instance!
INSTANCE_NAME=""
PORT_PREFIX=80

export PROJECT_HOME="${HOME}/pepper/${INSTANCE_NAME}"
export DEBUG=1

if [[ $INSTANCE_NAME = "" ]]; then
    DB_SUFFIX=""
    VIRTUALEVN_SUFFIX=""
else
    DB_SUFFIX="_${INSTANCE_NAME}"
    VIRTUALEVN_SUFFIX="-${INSTANCE_NAME}"
fi

export LMS_BASE="http://www.pepperpd.com"
export PREVIEW_LMS_BASE="http://preview.pepperpd.com"

# virtualevn
ENV_PYTHON="edx-platform${VIRTUALEVN_SUFFIX}"

if [[ -f /usr/bin/virtualenvwrapper.sh ]]; then
    IMPORT_VIRTUALENVWRAPPER=/usr/bin/virtualenvwrapper.sh
elif [[ -f /usr/local/bin/virtualenvwrapper.sh ]]; then
    IMPORT_VIRTUALENVWRAPPER=/usr/local/bin/virtualenvwrapper.sh
fi    

# ports
PORT_LMS="${PORT_PREFIX}00"
PORT_CMS="${PORT_PREFIX}01"
PORT_LMS_PREVIEW="${PORT_PREFIX}02"
PORT_XQUEUE="${PORT_PREFIX}03"
PORT_ORA="${PORT_PREFIX}04"
PORT_DISCUSS="${PORT_PREFIX}05"

# rvm
IMPORT_RVM="${HOME}/.rvm/scripts/rvm"
RVM_EDX_PLATFORM="ruby-1.9.3-p448@${INSTANCE_NAME}"

# elasticsearch
export SEARCH_SERVER=""

# ora
export XQUEUE_DB_NAME="xqueue${DB_SUFFIX}"

export XQUEUE_DB_USER="pepper"
export XQUEUE_DB_PASSWORD="lebbeb"
export XQUEUE_DB_HOST="mysql"
export XQUEUE_DB_PORT="3306"

export ESSAY_DB_NAME="essay${DB_SUFFIX}"
export ESSAY_DB_USER="pepper"
export ESSAY_DB_PASSWORD="lebbeb"
export ESSAY_DB_HOST="mysql"
export ESSAY_DB_PORT="3306"

export XQUEUE_URL="http://127.0.0.1:$PORT_XQUEUE"
export GRADING_CONTROLLER_INTERFACE_URL="http://127.0.0.1:$PORT_ORA"

# discuss
RVM_DISCUSS="ruby-1.9.3-p448@discuss${DB_SUFFIX}"
export ES_INDEX_COMMENT_THREAD="comment_thread${DB_SUFFIX}"
export ES_INDEX_COMMENT="comment${DB_SUFFIX}"
export DISSCUSS_MONGODB_HOST="mongo"
export DISSCUSS_MONGODB_PORT="27017"

export COMMENTS_SERVICE_URL="http://127.0.0.1:$PORT_DISCUSS"

# edx-platform
export EDX_PLATFORM_MONGO3_HOST="mongo3"
export EDX_PLATFORM_MONGO3_PORT=27018
export EDX_PLATFORM_MONGO3_USER="pepper"
export EDX_PLATFORM_MONGO3_PASSWORD="lebbeb"
export EDX_PLATFORM_MONGO3_DB_REPORTING="reporting${DB_SUFFIX}"

export EDX_PLATFORM_MONGO_HOST="mongo"
export EDX_PLATFORM_MONGO_PORT=27017
export EDX_PLATFORM_MONGO_USER="pepper"
export EDX_PLATFORM_MONGO_PASSWORD="lebbeb"
export EDX_PLATFORM_MONGO_DB_XMODULE="xmodule${DB_SUFFIX}"
export EDX_PLATFORM_MONGO_DB_XCONTENT="xcontent${DB_SUFFIX}"
export EDX_PLATFORM_MONGO_DB_USERSTORE="userstore${DB_SUFFIX}"
export EDX_PLATFORM_MONGO_DB_REMIND="remind${DB_SUFFIX}"
export EDX_PLATFORM_MONGO_DB_ASSIST="assist${DB_SUFFIX}"

export EDX_PLATFORM_MYSQL_DB_R="pepper${DB_SUFFIX}"
export EDX_PLATFORM_MYSQL_HOST_R="mysql_read"
export EDX_PLATFORM_MYSQL_PORT_R="3306"
export EDX_PLATFORM_MYSQL_USER_R="pepper"
export EDX_PLATFORM_MYSQL_PASSWORD_R="lebbeb"

export EDX_PLATFORM_MYSQL_DB_W="$EDX_PLATFORM_MYSQL_DB_R"
export EDX_PLATFORM_MYSQL_HOST_W="mysql_write"
export EDX_PLATFORM_MYSQL_PORT_W="$EDX_PLATFORM_MYSQL_PORT_R"
export EDX_PLATFORM_MYSQL_USER_W="$EDX_PLATFORM_MYSQL_USER_R"
export EDX_PLATFORM_MYSQL_PASSWORD_W="$EDX_PLATFORM_MYSQL_PASSWORD_R"

# people elasticsearch
export PEOPLE_ES_HOST1="elasticsearch"
export PEOPLE_ES_PORT1=9200
export PEOPLE_ES_HOST2="ashpepdr01p"
export PEOPLE_ES_PORT2=9200
export PEOPLE_ES_INDEX="people${DB_SUFFIX}"
export PEOPLE_ES_DOCTYPE="user"
