import os
import sys
import subprocess

print(f"welcome to return_kml.py {os.getcwd()}")


def get_pass():
    raw = os.getenv("JRAPH_SA_PASSWORD")
    if raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1]
    return raw


def run_sql(sql, password):
    comm = """/opt/mssql-tools18/bin/sqlcmd -C -U sa -P {} -d jongraph -Q""" .format(
        password).split()
    comm.append(sql)
    res = subprocess.run(comm, capture_output=True)
    return res


def main():
    pw = get_pass()
    print('PASSWORD', pw)
    for idx, arg in enumerate(sys.argv):
        print('ARG', idx, arg)

    sql = "select * from dbo.Products"
    res = run_sql(sql, pw)
    print('RESULT: ', res)


main()
