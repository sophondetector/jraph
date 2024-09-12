#!/usr/bin/env bash

cd /root/portal

/usr/bin/python3 -m flask run \
	--debug \
	--extra-files "templates/index.html:static/style.css"
