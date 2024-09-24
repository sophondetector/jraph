#!/usr/bin/env sh

JRAPH_LOG=/tmp/jraph.log
RUNDIR=/root/jraph

cd $RUNDIR

flask --env-file secrets.env run \
	--debug \
	--extra-files "templates/index.html:static/style.css" \
	--port 80 \
	--host 0.0.0.0 &>> $JRAPH_LOG
