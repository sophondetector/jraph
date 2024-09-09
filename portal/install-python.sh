#!/usr/bin/env bash

dnf install -y python3.12

python3 -m ensurepip --upgrade

pip3 install pyodbc
