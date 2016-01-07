#/bin/bash

mongo<<EOF
  use xmodule
  db.modulestore.remove({"_id.org":"$1","_id.course":"$2"})
EOF



