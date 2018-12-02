#!/bin/bash

mongod_status=`service mongod status`

if [[ "${mongod_status}" == *"running"* ]] || [[ "${mongod_status}" == *"start"* ]]
then
    echo "MongoDB is already running."
else
    sudo service mongod start
    echo "Start MongoDB."
fi

python app.py