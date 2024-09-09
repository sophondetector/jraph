import os
import pyodbc

_CONN = None

_JRAPH_DATABASE = 'jraph'
_JRAPH_HOST = 'localhost'
_JRAPH_USER = 'sa'


def _get_pass():
    raw = os.getenv("JRAPH_SA_PASSWORD")
    if raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1]
    return raw


def _init_conn(server, username, database) -> pyodbc.Connection:
    global _CONN
    password = _get_pass()
    print(f"connecting to {database}...", end='')
    # cat /etc/odbcinst.ini to find correct val for DRIVER for Sql Server
    driver = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.4.so.1.1'
    cstring = 'DRIVER={};SERVER={};UID={};PWD={};DATABASE={}'.format(
        driver, server, username, password, database)
    cstring += ';TrustServerCertificate=yes'
    _CONN = pyodbc.connect(cstring)
    print("done")
    return _CONN


def init_jraph_conn() -> pyodbc.Connection:
    return _init_conn(_JRAPH_HOST, _JRAPH_USER, _JRAPH_DATABASE)


def get_conn() -> pyodbc.Connection:
    global _CONN
    return _CONN
