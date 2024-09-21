class Node:
    def __init__(self, _id: int, **kwargs):
        self.id = _id
        self.properties = dict(**kwargs)


class Edge:
    def __init__(self, edge_id: int, source_id: int, target_id: int, **kwargs):
        self.id = edge_id
        self.source_id = source_id
        self.target_id = target_id
        self.properties = dict(**kwargs)
