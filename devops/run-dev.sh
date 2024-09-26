#!/usr/bin/env bash

DEPLOY_ENV="dev"
ENV_FILE=.env
EXTRA_FILES_ARR=(
	templates/index.html
	static/style.css
	static/leaflet.filelayer.js
	static/togeojson.js
) 
EXTRA_FILES=$(IFS=: ; echo "${EXTRA_FILES_ARR[*]}")
HOST="localhost"
PORT=5000
RUN_DIR=/root/jraph

FLASK_DEBUG=1

cd $RUN_DIR

flask --env-file $ENV_FILE run \
	--extra-files $EXTRA_FILES \
	--port $PORT \
	--host $HOST
