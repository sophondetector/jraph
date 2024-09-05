#!/usr/bin/env bash

SERVICE_NAME='jraph'
DEPS="mssql-server mssql-tools18 unixODBC-devel"

echo "installing the following deps for $SERVICE_NAME"
echo "$DEPS"

curl -o /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/9/mssql-server-2022.repo
curl -o /etc/yum.repos.d/mssql-release.repo https://packages.microsoft.com/config/rhel/9/prod.repo
dnf check-update
dnf install -y $DEPS
dnf update --all

# TODO configgify the interactive answers
echo "configuring mssql-server service"
/opt/mssql/bin/mssql-conf setup

echo "making sqlcmd avail in PATH"
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc

