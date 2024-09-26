#!/usr/bin/env sh

# assumes this script is in $jraph_root/devops
# and we want to be in $jraph_root
rundir=$(dirname $0)/..
cd $rundir

flask --env-file secrets.env run \
	--debug \
	--extra-files "templates/index.html:static/style.css:static/leaflet.filelayer.js:static/togeojson.js" \
	--port 5000 \
