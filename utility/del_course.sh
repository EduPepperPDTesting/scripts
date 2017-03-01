#/bin/bash

mongo<<EOF
  use xmodule
  db.modulestore.remove({"_id.org":"$1","_id.course":"$2"})
  use xcontent
  db.fs.files.remove({"_id.org":"$1","_id.course":"$2"})
  db.fs.files.remove({"files_id.org": "$1", "files_id.course": "$2"})
EOF



