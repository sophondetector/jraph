import json
import simplekml as sk
from typing import Union
from flask import Flask, request, render_template

import jraph_tool.dbc as dbc


app = Flask("jraph")


class Node:
    def __init__(self, node_id: int, properties: Union[dict, str]):
        self.node_id = node_id
        self.properties = properties
        if type(self.properties) is str:
            self.properties = json.loads(self.properties)

    def as_kml_point(self, kml=None) -> sk.Kml:
        if kml is None:
            kml = sk.Kml()
        kml.newpoint(
            name=self.properties.get("name"),
            description=self.properties.get('type'),
            coords=[(self.properties.get("lat"), self.properties.get("long"))]
        )
        return kml


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


def query_node(node_id: int) -> Node:
    with dbc.get_conn().cursor() as cur:
        cur.execute("SELECT * FROM node WHERE node_id=?;", node_id)
        node_id, properties_raw = cur.fetchone()
        return Node(node_id, properties_raw)


@app.route("/query", methods=["GET"])
def query():
    node_ids = request.args.get("node_id", '').split(',') or [3]
    kml = sk.Kml()
    for node in (query_node(nid) for nid in node_ids):
        node.as_kml_point(kml)
    return kml.kml()


@app.route("/", methods=["GET", "POST"])
def index():
    output = "no queries yet"
    input_query = None
    if request.method == "POST":
        kml = sk.Kml()
        input_query = request.form.to_dict().get("node_id")
        nids = input_query.split(',')
        for node_id in nids:
            node = query_node(node_id)
            node.as_kml_point(kml)
        output = kml.kml()
    return render_template("index.html", output=output, previous_query=input_query)
