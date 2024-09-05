#!/usr/bin/env sh

DEPS='locate jq vim'

echo "installing ${DEPS}"
dnf check-update
dnf upgrade -y
dnf install -y $DEPS
dnf update --all
