import os
import pyodbc

_CONN = None

# cat /etc/odbcinst.ini to find correct val for DRIVER for Sql Server
_DB_DRIVER = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.4.so.1.1'
_JRAPH_DB = 'jraph'
_JRAPH_HOST = 'localhost'
_JRAPH_USER = 'sa'


def _get_pass():
    pw = os.getenv("JRAPH_SA_PASSWORD")
    if not pw:
        print("JRAPH_SA_PASSWORD required in env!")
        exit(1)

    if pw[0] == '"' and pw[-1] == '"':
        return pw[1:-1]

    return pw


def get_conn() -> pyodbc.Connection:
    global _CONN
    if _CONN is None:
        print(f"connecting to {_JRAPH_DB}...", end='')
        cstring = 'DRIVER={};SERVER={};UID={};PWD={};DATABASE={}'.format(
            _DB_DRIVER, _JRAPH_HOST, _JRAPH_USER, _get_pass(), _JRAPH_DB)
        cstring += ';TrustServerCertificate=yes'
        _CONN = pyodbc.connect(cstring)
        print("done")
    return _CONN
