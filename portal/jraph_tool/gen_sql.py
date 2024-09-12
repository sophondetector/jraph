import json

# this for generating sql value rows for jraph-*-init.sql

with open('portal/jraph_tool/lib/data/edges.json') as fh:
    edges = json.load(fh)

for edge in edges:
    print('''({}, {}, {}, \'{}\'),'''.format(
        edge['edge_id'],
        edge['source_id'],
        edge['target_id'],
        json.dumps(edge['properties']))
    )
