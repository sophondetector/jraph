#!/usr/bin/env sh

SERVICE_NAME='jraph'
DEPS='locate jq vim'

echo "installing ${DEPS}"
dnf check-update
dnf upgrade -y
dnf install -y $DEPS
dnf update --all

echo "installing $SERVICE_NAME deps"
curl -o /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/9/mssql-server-2022.repo
curl -o /etc/yum.repos.d/mssql-release.repo https://packages.microsoft.com/config/rhel/9/prod.repo
dnf check-update
dnf install -y mssql-server mssql-tools18 unixODBC-devel
dnf update --all

echo "configuring mssql-server service"
/opt/mssql/bin/mssql-conf setup
systemctl status mssql-server

ehco "make sqlcmd avail in PATH"
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc

echo "finished provisioning $SERVICE_NAME"
