import io
import simplekml as sk
from flask import Flask, request, render_template, send_file

from jtool import query_node, query_node_edges


app = Flask("jraph")


@app.route("/query", methods=["GET"])
def query():
    node_ids = request.args.get("node_id", '').split(',')
    kml = sk.Kml()
    for nid in node_ids:
        node = query_node(nid)
        node.add_to_kml(kml)

    seen = set()
    for nid in node_ids:
        edges = query_node_edges(nid)
        for edge in edges:
            if edge.edge_id in seen:
                continue
            seen.add(edge.edge_id)
            if str(edge.source_id) in node_ids and str(edge.target_id) in node_ids:
                print('ADDING', edge)
                edge.add_to_kml(kml)

    fh = io.BytesIO(kml.kml().encode())
    return send_file(
        fh,
        as_attachment=True,
        download_name="output.kml")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
