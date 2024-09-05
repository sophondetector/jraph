#!/usr/bin/env bash

echo "$0 starting..."

if ([[ ! -v USERNAME ]] || [[ ! -v PASSWORD ]]); then 
	echo "$0 requires \$USERNAME and \$PASSWORD in env"
	exit 1
fi

echo "creating user $USERNAME"
useradd "$USERNAME"

echo "adding user $USERNAME to wheel group"
groupmod --append -U "$USERNAME" wheel

echo "$PASSWORD" | passwd --stdin "$USERNAME"

echo "$0 finito"

