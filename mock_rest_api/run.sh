#!/bin/bash


args="$@ -p 80"

# file=/data/db.json
# if [ -f $file ]; then
#     echo "Found db.json, trying to open"
#     args="$args db.json"
# fi


args="$args --watch /data/db.json"
#args="$args --static /data/static/"

json-server $args
