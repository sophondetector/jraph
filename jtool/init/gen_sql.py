#!/usr/bin/env python
import json

with open('lib/data/edges.json') as fh:
    edges = json.load(fh)

for edge in edges:
    print('''({}, {}, {}, \'{}\'),'''.format(
        edge['edge_id'],
        edge['source_id'],
        edge['target_id'],
        json.dumps(edge['properties'], ensure_ascii=False))
    )
