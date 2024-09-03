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
	confirm "clear all podman containers?" \
		&& podman container rm --volumes "$@" \
		|| echo "didn't do anything"
}

# create jraph-service container
# TODO add options
podmake () {
	podman run -it fedora:latest /bin/bash
}

# ssh into container
podssh () {
	podman exec -it $1 /bin/bash
}

# jraph service status
podcheck () {
	podman container inspect $1
}

