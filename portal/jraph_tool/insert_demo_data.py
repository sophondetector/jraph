import json
from dbc import init_jraph_conn

msg = "WARNING! This script deletes EVERYTHING in node and edge tables!"
msg += "\nDo you wish to continue? y/n "
if input(msg).lower()[0] != "y":
    print("Aborting...")
    exit(0)

with open('/root/portal/jraph_tool/lib/nodes.json') as fh:
    nodes = json.load(fh)
with open('/root/portal/jraph_tool/lib/edges.json') as fh:
    edges = json.load(fh)

# done with two separate sessions bc only
# one table can have IDENTITY_INSERT=ON
# per session

# session 1: clear previous data and insert nodes
with init_jraph_conn() as conn:
    cur = conn.cursor()

    # initting data, so no other data should be in there
    cur.execute("""
        DELETE FROM edge;
        DELETE FROM node;
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

# session 2: insert edges
with init_jraph_conn() as conn:
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
