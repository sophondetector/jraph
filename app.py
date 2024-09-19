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


@app.route("/", methods=["GET", "POST"])
def index():
    output = "no queries yet"
    input_query = None
    if request.method == "POST":
        kml = sk.Kml()
        input_query = request.form.to_dict().get("node_id")
        nids = input_query.split(',')
        for node_id in nids:
            node = dbc.query_node(node_id)
            node.as_kml_point(kml)
        output = kml.kml()
    return render_template(
        "index.html",
        output=output,
        previous_query=input_query)
