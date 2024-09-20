import jtool.dbc as dbc


class TestData:
    nodes = [
        {"node_id": 1, "properties": {
            "name": "Nate Taylor", "type": "person", "age": 38}},
        {"node_id": 2, "properties": {
            "name": "Jon Miller", "type": "person", "age": 40}},
        {"node_id": 3, "properties": {"name": "MIIS", "type": "place", "address": {
            "city": "Montery", "state": "CA"}, "lat": 36.59948, "long": -121.89673}}
    ]

    edges = [
        {"source_id": 1, "target_id": 3, "properties": {
            "type": "attended", "focus": "nonproliferation"}},
        {"source_id": 2, "target_id": 3, "properties": {
            "type": "attended", "focus": "terrorism"}},
    ]


print('inserting jraph test data')

for node in TestData.nodes:
    dbc.insert_node(node['node_id'], node['properties'])

for edge in TestData.edges:
    dbc.insert_edge(edge['source_id'], edge['target_id'], edge['properties'])

print('finito')
