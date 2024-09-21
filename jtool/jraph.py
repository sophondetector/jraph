from typing import Optional, List, Union

import simplekml as sk

from jtool.classes import Node, Edge
from jtool.dbc import query_node, query_node_edges


class Jraph:
    nodes: list[Node] = []
    edges: list[Edge] = []

    _default_lat: float = 43.0
    _default_long: float = -122.0
    _default_name = 'jraph node'
    _default_inc: int = 1

    @classmethod
    def _get_default_name(cls) -> str:
        res = f'{cls._default_name} {cls._default_inc}'
        cls._default_inc += 1
        return res

    @classmethod
    def j2k(cls, kml: Optional[sk.Kml] = None) -> sk.Kml:
        if kml is None:
            kml = sk.Kml()

        for node in cls.nodes:
            pnt = kml.newpoint()
            pnt.name = cls.get_name(node)
            pnt.coords = [cls.get_coords(node)]

        for edge in cls.edges:
            source = cls.get_jraph_node(edge.source_id)
            target = cls.get_jraph_node(edge.target_id)
            if (source is None) or (target is None):
                continue
            ls = kml.newlinestring()
            ls.coords = [cls.get_coords(source), cls.get_coords(target)]

        return kml

    @classmethod
    def get_jraph_node(cls, node_id) -> Optional[Node]:
        for node in cls.nodes:
            if node.id == node_id:
                return node
        return None

    @classmethod
    def get_jraph_edge(cls, edge_id: int) -> Optional[Edge]:
        for edge in cls.edges:
            if edge.id == edge_id:
                return edge
        return None

    @classmethod
    def clear(cls) -> None:
        cls.nodes = []
        cls.edges = []

    @classmethod
    def get_coords(cls, node: Node) -> tuple[float, float]:
        return (
            node.properties.get('long', cls._default_long),
            node.properties.get('lat', cls._default_lat),
        )

    @classmethod
    def get_name(cls, node: Node) -> str:
        name = node.properties.get('name')
        if name is None:
            return cls._default_name()
        return name

    @classmethod
    def add_node(cls, node: Node) -> None:
        check = cls.get_jraph_node(node.id)
        if check is not None:
            return
        cls.nodes.append(node)

    @classmethod
    def add_edge(cls, edge: Edge) -> None:
        check = cls.get_jraph_edge(edge.id)
        if check is not None:
            return
        cls.edges.append(edge)

    @classmethod
    def add_edges(cls, edges: List[Edge]) -> None:
        for ed in edges:
            cls.add_edge(ed)

    @classmethod
    def add(
        cls,
        nodes: Optional[Union[Node, List[Node]]] = None,
        edges: Optional[Union[Edge, List[Edge]]] = None,
    ) -> None:
        if nodes is not None:
            if type(nodes) is Node:
                nodes = [nodes]
            for node in nodes:
                cls.add_node(node)

        if edges is not None:
            if type(edges) is Edge:
                edges = [edges]
            for ed in edges:
                cls.add_edge(ed)


if __name__ == '__main__':
    outpath = 'output.kml'
    for nid in [1, 2, 3]:
        node = query_node(nid)
        Jraph.add_node(node)
        edges = query_node_edges(nid)
        Jraph.add_edges(edges)
    kml = Jraph.j2k()
    print('saving kml to {}...'.format(outpath), end='')
    kml.save(outpath)
    print('success')
    print('finito')
