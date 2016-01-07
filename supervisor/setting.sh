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

# ora
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

# discuss
export ES_INDEX_COMMENT_THREAD="comment_thread_dev"
export ES_INDEX_COMMENT="comment_thread_dev"
export DISSCUSS_MONGODB_HOST="mongo"
export DISSCUSS_MONGODB_PORT="27017"

export COMMENTS_SERVICE_URL="http://localhost:$PORT_DISCUSS"

# edx-platform
export EDX_PLATFORM_MONGO_HOST='mongo'
export EDX_PLATFORM_MONGO_PORT=27017
export EDX_PLATFORM_MONGO_USER='pepper'
export EDX_PLATFORM_MONGO_PASSWORD='lebbeb'
export EDX_PLATFORM_MONGO_DB_XMODULE="xmodule"
export EDX_PLATFORM_MONGO_DB_XCONTENT="xcontent"
export EDX_PLATFORM_MONGO_DB_USERSTORE="userstore"
export EDX_PLATFORM_MONGO_DB_REMIND="remind"
export EDX_PLATFORM_MONGO_DB_ASSIST="assist"

export EDX_PLATFORM_MYSQL_DB_R='pepper'
export EDX_PLATFORM_MYSQL_HOST_R='mysql_read'
export EDX_PLATFORM_MYSQL_PORT_R='3306'
export EDX_PLATFORM_MYSQL_USER_R='pepper'
export EDX_PLATFORM_MYSQL_PASSWORD_R='lebbeb'

export EDX_PLATFORM_MYSQL_DB_W="$EDX_PLATFORM_MYSQL_DB_R"
export EDX_PLATFORM_MYSQL_HOST_W='mysql_write'
export EDX_PLATFORM_MYSQL_PORT_W="$EDX_PLATFORM_MYSQL_PORT_R"
export EDX_PLATFORM_MYSQL_USER_W="$EDX_PLATFORM_MYSQL_USER_R"
export EDX_PLATFORM_MYSQL_PASSWORD_W="$EDX_PLATFORM_MYSQL_PASSWORD_R"

export LMS_BASE="http://lms.loc"
export PREVIEW_LMS_BASE="preview-staging.pepperpd.com"
