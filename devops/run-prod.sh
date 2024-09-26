#!/usr/bin/env bash

DEPLOY_ENV="prod"
ENV_FILE=.env
EXTRA_FILES_ARR=(
	templates/index.html
	static/style.css
	static/leaflet.filelayer.js
	static/togeojson.js
) 
EXTRA_FILES=$(IFS=: ; echo "${EXTRA_FILES_ARR[*]}")
HOST="0.0.0.0"
PORT=80
RUN_DIR=/root/jraph

cd $RUN_DIR

flask --env-file $ENV_FILE run \
	--debug \
	--extra-files $EXTRA_FILES \
	--port $PORT \
	--host $HOST
