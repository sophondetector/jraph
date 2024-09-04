#!/usr/bin/env bash

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

# list containers
podlist () {
	podman container list --all "$@"
}

# clear containers
podclear () {
	confirm "clear following containers and associated volumes $@" \
		&& podman container rm --volumes "$@" \
		|| echo "podclear aborted"
}

# create jraph-service container
podnew () {
	# TODO remove publish-all
	podman run --memory=2g --name="jraph-base" --workdir=/root --volume=./devops/:/root/devops/:z,ro --rmi --publish-all --tty --interactive --rm fedora:latest /bin/bash
}

# jraph client command 
jraph () {
	JRAPH_HOST=$1
	SERVER_COMMAND="$@"
	echo "jraph not implemented"	
	# ssh $JRAPH_HOST $SERVER_COMMAND
}
