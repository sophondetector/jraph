from typing import Iterable, Optional, List, Union
from io import BytesIO

from shapely.geometry import Point
import geopandas as gpd
import simplekml as sk
import pandas as pd

from .dbc import query_n_nearest_nodes, query_node, query_node_edges
from .classes import Node, Edge


_DEFAULT_NAME = 'JRAPH NODE'


class Jraph:
    def __init__(
        self,
        nodes: Optional[List[Node]] = None,
        edges: Optional[List[Edge]] = None
    ):
        self.nodes = nodes if nodes is not None else []
        self.edges = edges if edges is not None else []
        self.name_inc = 0

    def j2q(self) -> BytesIO:
        """
        Export geographic points with attributes to a GeoPackage file for QGIS.
        """

        # Prepare data for GeoDataFrame
        records = []
        geometries = []

        for node in self.nodes:
            lon, lat = node.get_coords()
            point = Point(lon, lat)
            geometries.append(point)
            record = {'node_id': node.node_id}
            features = node.properties['features'][0]
            geocoding = features['properties']['geocoding']
            for key, value in geocoding.items():
                record[key] = value
            records.append(record)

        # Create DataFrame from records
        df = pd.DataFrame(records)

        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=geometries, crs="EPSG:4326")

        # Export to GeoPackage
        res = BytesIO()
        gdf.to_file(res, driver="GPKG")

        return res

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
            desc = edge.properties.get("description")
            if desc is not None:
                ls.description = desc
            ls.coords = [self.get_coords(source), self.get_coords(target)]

        return kml

    def get_jraph_node(self, node_id: int) -> Optional[Node]:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def get_jraph_edge(self, edge_id: int) -> Optional[Edge]:
        for edge in self.edges:
            if edge.edge_id == edge_id:
                return edge
        return None

    def clear(self) -> None:
        self.nodes = []
        self.edges = []

    def get_coords(self, node: Node) -> Optional[tuple[float, float]]:
        return node.get_coords()

    def get_name(self, node: Node) -> str:
        name = node.properties.get("name")
        if name is None:
            name = node.properties.get("label")
            if name is None:
                name = _DEFAULT_NAME + ' ' + str(self.name_inc)
                self.name_inc += 1
        return name

    def add_node(self, node: Node) -> None:
        check = self.get_jraph_node(node.node_id)
        if check is not None:
            return
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        check = self.get_jraph_edge(edge.edge_id)
        if check is not None:
            return
        self.edges.append(edge)

    def add_edges(self, edges: List[Edge]) -> None:
        for ed in edges:
            self.add_edge(ed)

    def add(
        self,
        nodes: Optional[Union[Node, Iterable[Node]]] = None,
        edges: Optional[Union[Edge, Iterable[Edge]]] = None,
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
    lat = -118.423581
    long = 34.0573375
    print('query_n_nearest_nodes test')
    res = query_n_nearest_nodes(lat, long, 20)
    print(res)

    outpath = 'jraph-test-output.kml'
    jraph = Jraph()
    for nid in [262892, 262897, 262988]:
        node = query_node(nid)
        edges = query_node_edges(nid)
        jraph.add(node, edges)
    kml = jraph.j2k()
    print('saving kml to {}...'.format(outpath), end='')
    kml.save(outpath)
    print('success')
