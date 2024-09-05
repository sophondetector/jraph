#!/usr/bin/env bash

echo "$0 starting..."

if ([[ ! -v JRAPH_ADMIN_USERNAME ]] || [[ ! -v JRAPH_ADMIN_pASSWORD ]]); then 
	echo "$0 requires \$JRAPH_ADMIN_USERNAME and \$JRAPH_ADMIN_PASSWORD in env"
	exit 1
fi

echo "creating user $JRAPH_ADMIN_USERNAME"
useradd "$JRAPH_ADMIN_USERNAME"

echo "adding user $JRAPH_ADMIN_USERNAME to wheel group"
groupmod --append -U "$JRAPH_ADMIN_USERNAME" wheel

echo "$JRAPH_ADMIN_PASSWORD" | passwd --stdin "$JRAPH_ADMIN_USERNAME"

echo "$0 finito"

