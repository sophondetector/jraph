#!/usr/bin/env bash

CONTAINER_NAME="jraph_container"
IMAGE_NAME="jraph"

build () {

	# TODO configgify msql setup options
	# TODO SECURITY remove publish-all
	podman create \
		--env-file="config.env" \
		--memory="2g" \
		--name="$CONTAINER_NAME" \
		--workdir="/root" \
		--interactive \
		--tty \
		--publish-all \
		--replace \
		"fedora:latest" \
		"/bin/bash -x entrypoint.sh"

	podman cp JROOT/. $CONTAINER_NAME:/
	
	podman start --attach --interactive $CONTAINER_NAME
	
	podman commit $CONTAINER_NAME $IMAGE_NAME:latest
}

start () {
	podman run --rm -it $IMAGE_NAME:latest /opt/mssql/bin/sqlservr
}

# jraph client command
jraph_client () {
	echo "this command not implemented"	
}

"$@"
