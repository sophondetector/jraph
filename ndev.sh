#!/usr/bin/env bash

STAGE_ONE="jraph_build"
STAGE_TWO="jraph"
IMAGE_NAME="$STAGE_TWO:latest"

build () {

	# TODO configgify msql setup options
	# TODO SECURITY remove publish-all
	echo "creating"
	podman create \
		--env-file="config.env" \
		--memory="2g" \
		--name="$STAGE_ONE" \
		--workdir="/root" \
		--interactive \
		--tty \
		--publish-all \
		--replace \
		"fedora:latest" \
		"./entrypoint.sh"

	echo "copying"
	podman cp JROOT/. $STAGE_ONE:/
	
	echo "starting"
	podman start --attach --interactive $STAGE_ONE
	
	echo "committing"
	podman commit \
		--change CMD=/opt/mssql/bin/sqlservr \
		$STAGE_ONE \
		$IMAGE_NAME
	
	echo "creating local jraph container $STAGE_TWO"
	podman create \
		--env-file="config.env" \
		--interactive \
		--tty \
		--publish-all \
		--name $STAGE_TWO \
		--replace $IMAGE_NAME
}

start () {
	podman start --attach --interactive \
		$STAGE_TWO
}

shell () {
	podman exec --interactive --tty \
		$STAGE_TWO /bin/bash
}

test () {
	podman exec --interactive --tty \
		$STAGE_TWO \
		/opt/mssql-tools18/bin/sqlcmd \
			-C -U sa -P $JRAPH_SA_PASSWORD -i /root/test.sql
}

jraph_client () {
	echo "this command not implemented"	
}

"$@"
