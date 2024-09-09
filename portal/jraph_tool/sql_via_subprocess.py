import subprocess


def sql_via_subprocess(sql):
    comm = """/opt/mssql-tools18/bin/sqlcmd -C -U sa -P $JRAPH_SA_PASSWORD -d testdb -Q"""
    comm.append(sql)
    res = subprocess.run(comm, capture_output=True)
    return res
