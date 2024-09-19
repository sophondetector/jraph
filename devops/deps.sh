#!/usr/bin/env sh

SERVICE_NAME="jraph"
DEPS="mssql-server mssql-tools18 unixODBC-devel python3.12"

echo "installing dependencies for $SERVICE_NAME"

curl -o /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/9/mssql-server-2022.repo
curl -o /etc/yum.repos.d/mssql-release.repo https://packages.microsoft.com/config/rhel/9/prod.repo
dnf check-update
dnf install -y $DEPS
dnf update --all

# TODO configgify the interactive answers
echo "configuring mssql-server service"
/opt/mssql/bin/mssql-conf setup

# add sqlcmd to PATH
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc

# python deps
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

pip3 install pyodbc
pip3 install simplekml
pip3 install python-dotenv
pip3 install flask
pip3 install ipython
pip3 install lxml
pip3 install pandas
