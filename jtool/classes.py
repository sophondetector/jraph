from typing import Optional, Tuple, Union


class Node:
    def __init__(
        self,
        node_id: int,
        long: Optional[Union[float, int, str]] = None,
        lat: Optional[Union[float, int, str]] = None,
        properties: Optional[dict] = None
    ):
        self.node_id: int = node_id

        self.long = long
        if self.long is not None:
            self.long = float(self.long)

        self.lat = lat
        if self.lat is not None:
            self.lat = float(self.lat)

        self.properties = dict()
        if type(properties) is dict:
            self.properties = properties

    def get_coords(self) -> Optional[Tuple[float, float]]:
        """
        return Tuple[long: float, lat: float]
        """
        if self.long is None or self.lat is None:
            print(f'warning: {self} has no coordinates')
            return None
        return (self.long, self.lat)

    def __repr__(self) -> str:
        return f'<Node {self.node_id}>'


class Edge:
    def __init__(
        self,
        edge_id: int,
        source_id: int,
        target_id: int,
        properties: Optional[dict] = None
    ):
        self.edge_id = edge_id
        self.source_id = source_id
        self.target_id = target_id

        self.properties = dict()
        if type(properties) is dict:
            self.properties = properties

        self.properties['edgeId'] = self.edge_id
        self.properties['targetId'] = self.target_id
        self.properties['sourceId'] = self.source_id

    def __repr__(self):
        return f'<Edge {self.edge_id}: {self.source_id} -> {self.target_id}>'
