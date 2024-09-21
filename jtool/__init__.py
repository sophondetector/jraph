import json
from typing import Union, Optional, List, Tuple

import pyodbc
import simplekml as sk

import jtool.dbc as dbc
from jtool.utils import nan2none


class Coords:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long

    def as_tuple(self) -> Tuple[float, float]:
        return (self.long, self.lat)


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
        self.name = self.properties.get("name") if name is not None else name
        self.coords = coords
        if self.coords is None:
            lat = self.properties.get("lat", 0)
            long = self.properties.get("long", 0)
            self.coords = Coords(lat, long)

    def add_to_kml(self, kml=None) -> sk.Kml:
        if kml is None:
            kml = sk.Kml()
        kml.newpoint(
            name=self.name,
            description=self.properties.get('type'),
            coords=[self.coords.as_tuple()]
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

    def add_to_kml(self, kml=None) -> sk.Kml:
        if kml is None:
            kml = sk.Kml()
        ls = kml.newlinestring()
        source_node = query_node(self.source_id)
        target_node = query_node(self.target_id)
        ls.coords = [
            source_node.coords.as_tuple(),
            target_node.coords.as_tuple()
        ]
        ls.name = self.properties.get('name', 'NO NAME')
        return kml

    def __repr__(self):
        return f'<Edge: {self.source_id} -> {self.target_id}>'


def query_node(node_id: int) -> Node:
    with dbc.get_cur() as cur:
        cur.execute("SELECT * FROM node WHERE node_id=?;", node_id)
        node_id, properties_raw = cur.fetchone()
        return Node(node_id, properties_raw)


def query_edge_source(source_id) -> List[Edge]:
    with dbc.get_cur() as cur:
        cur.execute("SELECT * FROM edge WHERE source_id=?;", source_id)
        edge_rows = cur.fetchall()
    return [Edge(*row) for row in edge_rows]


def query_edge_target(target_id) -> List[Edge]:
    with dbc.get_cur() as cur:
        cur.execute("SELECT * FROM edge WHERE target_id=?;", target_id)
        edge_rows = cur.fetchall()
    return [Edge(*row) for row in edge_rows]


def query_node_edges(node_id) -> List[Edge]:
    res = query_edge_source(node_id)
    res.extend(query_edge_target(node_id))
    return res


def insert_node(
        nid,
        props: Optional[Union[dict, str]] = None,
        cur: Optional[pyodbc.Cursor] = None):

    if cur is None:
        cur = dbc.get_cur()

    if type(props) is dict:
        props = nan2none(props)
        props = json.dumps(props)
        # TODO use a better json encoder for this

    with cur:
        cur.execute('SET IDENTITY_INSERT node ON;')
        cur.execute("INSERT node (node_id, properties) VALUES (?, ?)",
                    nid, props)
        cur.commit()


def insert_edge(
        source_id: int,
        target_id: int,
        props: Optional[Union[dict, str]] = None,
        cur: Optional[pyodbc.Cursor] = None):

    if cur is None:
        cur = dbc.get_cur()

    if props is None:
        props = '{}'

    if type(props) is dict:
        props = nan2none(props)
        props = json.dumps(props)
        # TODO use a better json encoder for this

    with cur:
        cur.execute(
            "INSERT edge (source_id, target_id, properties) VALUES (?, ?, ?)",
            source_id, target_id, props)
        cur.commit()
