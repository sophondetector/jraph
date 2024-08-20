#!/usr/bin/env sh

SERVICE_NAME='msql-server'
DEPS='locate'
SA_PASSWORD='Intrototerror1!'

dnf check-update
echo "updating dnf etc"
dnf upgrade -y

echo "installing ${DEPS}"
dnf install -y $DEPS

curl -o /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/9/mssql-server-2022.repo

dnf install -y mssql-server

/opt/mssql/bin/mssql-conf setup

systemctl status mssql-server

# dnf install -y mssql-server-selinux
# firewall-cmd --zone=public --add-port=1433/tcp --permanent
# firewall-cmd --reload

curl https://packages.microsoft.com/config/rhel/9/prod.repo | tee /etc/yum.repos.d/mssql-release.repo
dnf install -y mssql-tools18 unixODBC-devel
dnf check-update
dnf update mssql-tools18

# make sqlcmd avail (????)
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc

# sqlcmd -C -S localhost -U sa -P $SA_PASSWORD
# -C is for Trust Server Certificate - prevents localhost self-signed cert error
#
# CREATE DATABASE TestDB;
# SELECT Name from sys.databases;
# GO

echo "finished provisioning $SERVICE_NAME"
