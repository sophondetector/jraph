#!/usr/bin/env sh

echo "userpass.sh starting..."

USERNAME=${USERNAME:-"msqladmin"}
# PASSWORD=${PASSWORD:-"mydefaultpassword"}

echo "creating user $USERNAME"
useradd "$USERNAME"

echo "adding user $USERNAME to wheel group"
groupmod --append -U "$USERNAME" wheel

# echo "$PASSWORD" | passwd --stdin "$USERNAME"

echo "userpass.sh finito"
