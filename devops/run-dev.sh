#!/usr/bin/env bash

EXTRA_FILES_ARR=(
	templates/index.html
	static/style.css
	static/leaflet.filelayer.js
	static/togeojson.js
)
EXTRA_FILES=$(
	IFS=:
	echo "${EXTRA_FILES_ARR[*]}"
)
HOST="localhost"
PORT=4000

flask run \
	--debug \
	--extra-files $EXTRA_FILES \
	--port $PORT \
	--host $HOST
