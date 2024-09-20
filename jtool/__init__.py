import json
from typing import Union

import simplekml as sk


class Node:
    def __init__(self, node_id: int, properties: Union[dict, str]):
        self.node_id = node_id
        self.properties = properties
        if type(self.properties) is str:
            self.properties = json.loads(self.properties)

    def add_to_kml(self, kml=None) -> sk.Kml:
        if kml is None:
            kml = sk.Kml()
        kml.newpoint(
            name=self.properties.get("name"),
            description=self.properties.get('type'),
            coords=[(self.properties.get("long"), self.properties.get("lat"))]
        )
        return kml

    def __repr__(self):
        return f'<Node {self.node_id}>'


class Edge:
    def __init__(
            self,
            edge_id: int,
            source_id: int,
            target_id: int,
            properties: Union[dict, str]):
        self.edge_id = edge_id
        self.source_id = source_id
        self.target_id = target_id
        self.properties = properties
        if type(self.properties) is str:
            self.properties = json.loads(self.properties)

    def __repr__(self):
        return f'<Edge: {self.source_id} -> {self.target_id}>'
