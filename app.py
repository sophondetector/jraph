import io
from flask import Flask, request, render_template, send_file

from jtool import Jraph, query_node, query_node_edges


app = Flask("jraph")


@app.route("/query", methods=["GET"])
def query():
    node_ids = request.args.get("node_id", '').split(',')
    for nid in node_ids:
        node = query_node(nid)
        edges = query_node_edges(nid)
        Jraph.add(node, edges)

    kml = Jraph.j2k()
    Jraph.clear()
    fh = io.BytesIO(kml.kml().encode())
    return send_file(
        fh,
        as_attachment=True,
        download_name="output.kml")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
