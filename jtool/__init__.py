import json
from typing import Union, Optional

import simplekml as sk


class Coords:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long


class Node:
    def __init__(
        self,
        node_id: int,
        properties: Union[dict, str],
        name: Optional[str] = None,
        coords: Optional[Coords] = None
    ):
        self.node_id = node_id
        self.properties = properties
        if type(self.properties) is str:
            self.properties = json.loads(self.properties)
        self.name = name
        self.coords = coords

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
