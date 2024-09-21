from typing import Optional

import simplekml as sk

from jtool.classes import Node, Edge
from jtool.dbc import query_node, query_node_edges


class Jraph:
    nodes: list[Node] = []
    edges: list[Edge] = []

    _default_lat: float = 43.0
    _default_long: float = -122.0
    _default_alt: float = 1.0

    _default_inc: int = 1

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
            cls._default_inc += 1
            name = 'default name ' + cls._default_inc
        return name


if __name__ == '__main__':
    outpath = 'output.kml'
    for nid in [1, 2, 3]:
        node = query_node(nid)
        Jraph.nodes.append(node)
        edges = query_node_edges(nid)
        Jraph.edges.extend(edges)

    kml = Jraph.j2k()
    print('saving kml to {}...'.format(outpath), end='')
    kml.save(outpath)
    print('success')
    print('finito')
