#!/usr/bin/env bash

dnf install -y python3.12

python3 -m ensurepip --upgrade

python3 -m pip install --upgrade pip

pip3 install pyodbc
pip3 install simplekml
pip3 install python-dotenv
pip3 install flask
pip3 install ipython
