#!/usr/bin/env bash

CONTAINER_NAME="jraph_container"
IMAGE_NAME="jraph"

build () {

	# TODO configgify msql setup options
	# TODO SECURITY remove publish-all
	echo "creating"
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
		"./entrypoint.sh"

	echo "copying"
	podman cp JROOT/. $CONTAINER_NAME:/
	
	echo "starting"
	podman start --attach --interactive $CONTAINER_NAME
	
	echo "committing"
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
