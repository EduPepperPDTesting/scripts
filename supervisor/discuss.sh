#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/setting.sh"
source $IMPORT_RVM

fuser -k $PORT_DISCUSS/tcp
# kill -9 $(ps -ef|grep -E 'ruby app.rb'|grep -v grep|awk '{print $2}')

rvm use $RVM_DISCUSS

cd "$PROJECT_HOME/cs_comments_service"
ruby app.rb -p $PORT_DISCUSS
