import json
from typing import Optional, Union


class Node:
    def __init__(
        self,
        node_id: int,
        properties: Optional[Union[dict, str]] = None,
        **kwargs
    ):
        self.node_id = node_id

        self.properties = dict()
        if type(properties) is dict:
            self.properties = properties
        elif type(properties) is str:
            self.properties = json.loads(properties)

        self.properties.update(**kwargs)

    def __repr__(self):
        return f'<Node {self.node_id}>'


class Edge:
    def __init__(
        self,
        edge_id: int,
        source_id: int,
        target_id: int,
        properties: Optional[Union[dict, str]] = None,
        **kwargs
    ):
        self.edge_id = edge_id
        self.source_id = source_id
        self.target_id = target_id

        self.properties = dict()
        if type(properties) is dict:
            self.properties = properties
        elif type(properties) is str:
            self.properties = json.loads(properties)

        self.properties.update(**kwargs)

    def __repr__(self):
        return f'<Edge {self.edge_id}>'
