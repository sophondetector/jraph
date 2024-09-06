#!/usr/bin/env bash

CONTAINER_NAME="jraph_build_container"
IMAGE_NAME="jraph:latest"
SERVICE_CONTAINER_NAME="jraph_service_container"

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
	podman commit \
		--change CMD=/opt/mssql/bin/sqlservr \
		$CONTAINER_NAME \
		$IMAGE_NAME
	
	echo "creating local jraph container $SERVICE_CONTAINER_NAME"
	podman create \
		--env-file="config.env" \
		--interactive \
		--tty \
		--publish-all \
		--name $SERVICE_CONTAINER_NAME \
		--replace $IMAGE_NAME
}

start () {
	podman start --attach --interactive \
		$SERVICE_CONTAINER_NAME
}

shell () {
	podman exec --interactive --tty \
		$SERVICE_CONTAINER_NAME /bin/bash
}

run-test () {
	podman exec --interactive --tty \
		$SERVICE_CONTAINER_NAME /bin/bash +x test-sqlcmd.sh
}

jraph_client () {
	echo "this command not implemented"	
}

"$@"
