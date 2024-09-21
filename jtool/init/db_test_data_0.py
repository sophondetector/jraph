from jtool.dbc import insert_node, insert_edge


class TestData:
    nodes = [
        {
            "node_id": 1,
            "properties": {
                "name": "Nate Taylor",
                "type": "person",
                "age": 38,
                "lat": 43.2047222222,
                "long": -71.5413888889
            }
        },
        {
            "node_id": 2,
            "properties": {
                "name": "Jon Miller",
                "type": "person",
                "age": 40,
                "lat": 45.5233333333,
                "long": -122.6802777778
            }
        },
        {
            "node_id": 3,
            "properties": {
                "name": "MIIS",
                "type": "place",
                "address": {
                    "city": "Montery",
                    "state": "CA"
                },
                "lat": 36.59948,
                "long": -121.89673
            }
        }
    ]

    edges = [
        {"source_id": 1, "target_id": 3, "properties": {
            "type": "attended", "focus": "nonproliferation"}},
        {"source_id": 2, "target_id": 3, "properties": {
            "type": "attended", "focus": "terrorism"}},
    ]


print('inserting jraph test data')

for node in TestData.nodes:
    insert_node(node['node_id'], node['properties'])

for edge in TestData.edges:
    insert_edge(edge['source_id'], edge['target_id'], edge['properties'])

print('finito')
