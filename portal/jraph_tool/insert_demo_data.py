import os
import json
import pyodbc


_CONN = None


def _get_nodes_edges():
    with open('/root/portal/jraph_tool/lib/nodes.json') as fh:
        nodes = json.load(fh)
    with open('/root/portal/jraph_tool/lib/edges.json') as fh:
        edges = json.load(fh)
    return nodes, edges


def _get_pass():
    raw = os.getenv("JRAPH_SA_PASSWORD")
    if raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1]
    return raw


def init_conn(server, username, password, database) -> pyodbc.Connection:
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


if __name__ == '__main__':
    msg = "WARNING! This script deletes EVERYTHING in node and edge tables!"
    msg += "\nDo you wish to continue? y/n "
    if input(msg).lower()[0] != "y":
        print("Aborting...")
        exit(0)

    nodes, edges = _get_nodes_edges()
    # done with two separate sessions bc only
    # one table can have IDENTITY_INSERT set
    # to ON per session

    # clear previous data
    with init_conn('localhost', 'sa', _get_pass(), 'jraph') as conn:
        cur = conn.cursor()

        # initting data, so no other data should be in there
        cur.execute("""
            DELETE FROM node;
            DELETE FROM edge;
        """)

        cur.commit()

        cur.execute("""
            SET IDENTITY_INSERT node ON;
        """)

        cur.commit()

        for node in nodes:
            insert_sql = """
            INSERT INTO node(node_id, properties)
            VALUES (?, ?)
            """
            cur.execute(
                insert_sql,
                node['node_id'],
                json.dumps(node['properties'])
            )

        cur.commit()

    # insert edges
    with init_conn('localhost', 'sa', _get_pass(), 'jraph') as conn:
        cur = conn.cursor()

        cur.execute("""
            SET IDENTITY_INSERT edge ON;
        """)

        for edge in edges:
            insert_sql = """
            INSERT INTO edge(
                    edge_id,
                    source_id,
                    target_id,
                    properties)
            VALUES ( ?, ?, ?, ? )
            """
            cur.execute(
                insert_sql,
                edge['edge_id'],
                edge['source_id'],
                edge['target_id'],
                json.dumps(edge['properties']))

        cur.commit()

    print("all done")
    exit(0)
