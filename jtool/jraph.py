from typing import Optional, List, Union

import simplekml as sk

from .classes import Node, Edge
from .dbc import query_node, query_node_edges


_DEFAULT_LAT: float = 43.0
_DEFAULT_LONG: float = -122.0
_DEFAULT_NAME = 'JRAPH NODE'


class Jraph:
    def __init__(
        self, nodes: Optional[List[Node]] = None,
        edges: Optional[List[Edge]] = None
    ):
        self.nodes = nodes if nodes is not None else []
        self.edges = edges if edges is not None else []
        self.name_inc = 0

    def j2k(self, kml: Optional[sk.Kml] = None) -> sk.Kml:
        if kml is None:
            kml = sk.Kml()

        for node in self.nodes:
            pnt = kml.newpoint()
            pnt.name = self.get_name(node)
            pnt.coords = [self.get_coords(node)]

        for edge in self.edges:
            source = self.get_jraph_node(edge.source_id)
            target = self.get_jraph_node(edge.target_id)
            if (source is None) or (target is None):
                continue
            ls = kml.newlinestring()
            ls.coords = [self.get_coords(source), self.get_coords(target)]

        return kml

    def get_jraph_node(self, node_id) -> Optional[Node]:
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_jraph_edge(self, edge_id: int) -> Optional[Edge]:
        for edge in self.edges:
            if edge.id == edge_id:
                return edge
        return None

    def clear(self) -> None:
        self.nodes = []
        self.edges = []

    def get_coords(self, node: Node) -> tuple[float, float]:
        return (
            node.properties.get('long', _DEFAULT_LONG),
            node.properties.get('lat', _DEFAULT_LAT),
        )

    def get_name(self, node: Node) -> str:
        name = node.properties.get('name')
        if name is None:
            name = _DEFAULT_NAME + ' ' + self.name_inc
            self.name_inc += 1
        return name

    def add_node(self, node: Node) -> None:
        check = self.get_jraph_node(node.id)
        if check is not None:
            return
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        check = self.get_jraph_edge(edge.id)
        if check is not None:
            return
        self.edges.append(edge)

    def add_edges(self, edges: List[Edge]) -> None:
        for ed in edges:
            self.add_edge(ed)

    def add(
        self,
        nodes: Optional[Union[Node, List[Node]]] = None,
        edges: Optional[Union[Edge, List[Edge]]] = None,
    ) -> None:
        if nodes is not None:
            if type(nodes) is Node:
                nodes = [nodes]
            for node in nodes:
                self.add_node(node)

        if edges is not None:
            if type(edges) is Edge:
                edges = [edges]
            for ed in edges:
                self.add_edge(ed)


if __name__ == '__main__':
    outpath = 'jraph-test-output.kml'
    jraph = Jraph()
    for nid in [1, 2, 3]:
        node = query_node(nid)
        edges = query_node_edges(nid)
        jraph.add(node, edges)
    kml = jraph.j2k()
    print('saving kml to {}...'.format(outpath), end='')
    kml.save(outpath)
    print('success')
    print('finito')
