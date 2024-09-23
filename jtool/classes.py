from typing import Optional


class Node:
    def __init__(
        self,
        node_id: int,
        properties: Optional[dict] = None,
        **kwargs
    ):
        self.node_id = node_id
        self.properties = properties if properties is not None else dict()
        self.properties.update(**kwargs)

    def __repr__(self):
        return f'<Node {self.node_id}>'


class Edge:
    def __init__(
        self,
        edge_id: int,
        source_id: int,
        target_id: int,
        properties: Optional[dict] = None,
        **kwargs
    ):
        self.edge_id = edge_id
        self.source_id = source_id
        self.target_id = target_id
        self.properties = properties if properties is not None else dict()
        self.properties.update(**kwargs)

    def __repr__(self):
        return f'<Edge {self.edge_id}>'
