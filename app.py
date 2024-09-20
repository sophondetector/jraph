import io
import simplekml as sk
from flask import Flask, request, render_template, send_file

import jtool.dbc as dbc


app = Flask("jraph")


@app.route("/query", methods=["GET"])
def query():
    node_ids = request.args.get("node_id", '').split(',')
    kml = sk.Kml()
    for node in (dbc.query_node(nid) for nid in node_ids):
        node.add_to_kml(kml)
    # find edges
    fh = io.BytesIO(kml.kml().encode())
    return send_file(
        fh,
        as_attachment=True,
        download_name="output.kml")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
