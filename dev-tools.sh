#!/usr/bin/env bash

if [[ "$@" =~ "*help" ]]; then
	echo "hello! help"
fi

confirm () {
    # call with a prompt string or use a default
    read -r -p "${1:-Are you sure? [y/N]} " response
    case "$response" in
        [yY][eE][sS]|[yY])
            true
        ;;
        *)
            false
        ;;
    esac
}

create_jraph_image () {
	# TODO use an env file instead
	source config.sh 

	CONTAINER_NAME="jraph_container"
	IMAGE_NAME="jraph"
	WORKDIR="/root"
	COMMAND="/bin/bash -x entrypoint.sh"

	# TODO get systemd to be the init instead of a bash process
	# TODO remove publish-all
	podman create \
		--memory="2g" \
		--name="$CONTAINER_NAME" \
		--workdir="$WORKDIR" \
		--interactive \
		--tty \
		--publish-all \
		--replace \
		--init \
		"fedora:latest" \
		$COMMAND

	podman cp devops/FILESYSTEM_ROOT/. $CONTAINER_NAME:/
	
	podman start --attach --interactive $CONTAINER_NAME
	
	# podman commit $CONTAINER_NAME $IMAGE_NAME:latest
}

test_jraph_image () {
	# TODO get systemd to be the init instead of a bash process
	podman run -it --rm jraph:latest /bin/bash
}


# jraph client command 
jraph_service_request () {
	echo "this command not implemented"	
	# JRAPH_HOST=$1
	# SERVER_COMMAND="$@"
	# ssh $JRAPH_HOST $SERVER_COMMAND
}

"$@"
