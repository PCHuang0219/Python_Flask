#!/bin/bash
app="flask-app"
WORK_FOLDER=$(pwd)
cd ..
UPPER_LEVEL=$(pwd)
cd ${WORK_FOLDER}
docker run -d -p 8000:8000 --rm --name=${app} \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v ${UPPER_LEVEL}:/source \
        ${app}:latest python3 app.py