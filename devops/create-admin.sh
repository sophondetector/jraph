#!/usr/bin/env bash

echo "$0 starting..."

USERNAME="jraph-admin"
PASSWORD='Intrototerror1!'

echo "creating user $USERNAME"
useradd "$USERNAME"

echo "adding user $USERNAME to wheel group"
groupmod --append -U "$USERNAME" wheel

echo "$PASSWORD" | passwd --stdin "$USERNAME"

echo "$0 finito"
