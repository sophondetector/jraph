#!/usr/bin/env bash

ENV_FILE=.env
EXTRA_FILES="templates/index.html:static/style.css:static/leaflet.filelayer.js:static/togeojson.js" 

cd /root/jraph

flask --env-file $ENV_FILE run \
	--debug \
	--extra-files $EXTRA_FILES \
	--port 80 \
	--host 0.0.0.0
