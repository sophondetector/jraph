import os
import json
import pyodbc


_CONN = None


def _get_pass():
    raw = os.getenv("JRAPH_SA_PASSWORD")
    if raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1]
    return raw


def init_conn(server, username, password, database):
    global _CONN
    print(f"connecting to {database}...", end='')
    # cat /etc/odbcinst.ini to find correct val for DRIVER for Sql Server
    driver = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.4.so.1.1'
    cstring = 'DRIVER={};SERVER={};UID={};PWD={};DATABASE={}'.format(
        driver, server, username, password, database)
    cstring += ';TrustServerCertificate=yes'
    _CONN = pyodbc.connect(cstring)
    print("done")
    return _CONN


def get_conn():
    global _CONN
    return _CONN


def get_cur():
    return get_conn().cursor()


def ex(sql, *args, print_results=True) -> None:
    """
    creates a cursor, and executes the given sql WITHOUT committing
    print_results=True dumps return to stdout
    """
    with get_cur() as cur:
        cur.execute(sql, *args)
        while print_results:
            row = cur.fetchone()
            if not row:
                break
            print(row)


def excomm(sql, *args, print_results=True) -> None:
    """
    creates a cursor, executes and COMMITS given sql.
    print_results=True dumps return to stdout
    """
    with get_cur() as cur:
        cur.execute(sql, *args)
        cur.commit()
        while print_results:
            row = cur.fetchone()
            if not row:
                break
            print(row)


def list_conn_dbs():
    list_dbs_sql = """
    SELECT name, database_id, create_date
    FROM sys.databases;
    """
    with get_conn().execute(list_dbs_sql) as cur:
        while True:
            row = cur.fetchone()
            if not row:
                break
            print(row)


def insert_node(properties, node_id) -> None:
    insert_sql = "INSERT INTO node(properties, node_id) VALUES(?, ?);"
    excomm(insert_sql, json.dumps(properties), node_id)
    return


def insert_edge(source_id, target_id, properties, edge_id) -> None:
    insert_sql = """
    INSERT INTO edge(source_id, target_id, properties, edge_id)
    VALUES(?, ?, ?, ?);
    """
    excomm(insert_sql, source_id, target_id, properties, edge_id)
    return


if __name__ == '__main__':
    password = _get_pass()
    init_conn('localhost', 'sa', password, "jraph")

    with open('nodes.json') as fh:
        nodes = json.load(fh)

    for node in nodes:
        insert_node(node['properties'], node['node_id'])

    with open('edges.json') as fh:
        edges = json.load(fh)

    for edge in edges:
        insert_edge(edge['properties'], edge['edge_id'])
