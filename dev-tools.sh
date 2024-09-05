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
	BASE_IMAGE="fedora:latest"
	IMAGE_NAME="jraph"
	IMAGE_TAG="latest"
	WORKDIR="/root"
	COMMAND="/bin/bash"
	MEMORY="2g"

	# TODO get systemd to be the init instead of a bash process
	podman create \
		--memory=$MEMORY \
		--name="$IMAGE_NAME" \
		--workdir="$WORKDIR" \
		--interactive \
		--tty \
		--publish-all \
		--replace \
		$BASE_IMAGE 
		$COMMAND

	podman cp devops/install-basic-deps.sh $IMAGE_NAME:/root/
	podman cp devops/create-admin.sh $IMAGE_NAME:/root/
	podman cp devops/install-msql-server.sh $IMAGE_NAME:/root/

	podman start $IMAGE_NAME
	
	# TODO package these three scripts into one command
	# and then set that command as the starting command 
	# in the podman create command above
	# then just need to do podman run and then podman commit
	podman exec -t $IMAGE_NAME /bin/bash -x /root/install-basic-deps.sh
	podman exec -it $IMAGE_NAME /bin/bash -x /root/create-admin.sh
	podman exec -it $IMAGE_NAME /bin/bash -x /root/install-msql-server.sh

	podman commit $IMAGE_NAME $IMAGE_NAME:$IMAGE_TAG
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
