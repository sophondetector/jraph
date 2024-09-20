import simplekml as sk
from flask import Flask, request, render_template

import jtool.dbc as dbc


app = Flask("jraph")


@app.route("/query", methods=["GET"])
def query():
    node_ids = request.args.get("node_id", '').split(',') or [3]
    kml = sk.Kml()
    for node in (dbc.query_node(nid) for nid in node_ids):
        node.as_kml_point(kml)
    return kml.kml()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
