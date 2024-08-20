#!/usr/bin/env sh

echo "script starting"

USERNAME=${USERNAME:-"msqladmin"}
# PASSWORD=${PASSWORD:-"mydefaultpassword"}

echo "creating user $USERNAME"
useradd "$USERNAME"

echo "adding user $USERNAME to wheel group"
groupmod --append -U "$USERNAME" wheel

# echo "$PASSWORD" | passwd --stdin "$USERNAME"

echo "script done"
