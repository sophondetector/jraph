#!/usr/bin/env bash

HOST="localhost"
PORT=4000

flask run \
	--debug \
	--port $PORT \
	--host $HOST
