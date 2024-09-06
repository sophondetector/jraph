#!/usr/bin/env bash

DEPS="mssql-server mssql-tools18 unixODBC-devel"

echo "installing following SQL Server deps: $DEPS"

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

echo "creating jongraph database and test table dbo.Products"
/opt/mssql-tools18/bin/sqlcmd \
	-C -U sa -P $JRAPH_SA_PASSWORD -i test-db-init.sh -o test-init-output.log
