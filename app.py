import json
import simplekml
from flask import Flask, request, render_template

import jraph_tool.dbc as dbc


app = Flask("jraph")


def get_single_node(node_id) -> (int, dict):
    with dbc.get_conn().cursor() as cur:
        cur.execute("SELECT * FROM node WHERE node_id=?;", node_id)
        node_id, properties_raw = cur.fetchone()
        return node_id, json.loads(properties_raw)


@app.route("/query", methods=["GET"])
def query():
    node_ids = request.args.get("node_id", '').split(',') or [3]

    kml = simplekml.Kml()
    for row in (get_single_node(nid) for nid in node_ids):
        node_id, properties = row
        kml.newpoint(
            name=properties.get("name"),
            description=properties.get('type'),
            coords=[(properties.get("lat"), properties.get("long"))]
        )
    return kml.kml()


@app.route("/", methods=["GET", "POST"])
def index():
    value = "default value"
    if request.method == "POST":
        value = "hello"
    return render_template("index.html", value=value)
