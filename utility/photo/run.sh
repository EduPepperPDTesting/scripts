#!/bin/bash
ROOT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mongo<<EOF
  use userstore
  db.dropDatabase()
EOF

if [ -f ~/shell/edx/env-rvm1.9.3.sh ]; then
  source ~/shell/edx/env-rvm1.9.3.sh
else
  source ~/edx_all/scripts/env-rvm1.9.3.sh
fi

cd "$ROOT_PATH"
python mongo_user_store.py

