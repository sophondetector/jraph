import io
import time

from typing import Optional

from flask import Flask, request, render_template, send_file, abort, jsonify

from jtool.jraph import Jraph
from jtool.dbc import query_many_node_edges, query_node_prop


app = Flask("jraph")

# TODO change so there are session objects
LAST_JRAPH: Optional[Jraph] = None
PREVIOUS_QUERIES = []


@app.route("/download-gpkg", methods=["GET"])
def download_gpkg():
    global LAST_JRAPH
    if LAST_JRAPH is None:
        return abort(500, 'something went wrong with the gpkg')
    return send_file(
        LAST_JRAPH.j2q(),
        as_attachment=True,
        download_name="output.gpkg")


@app.route("/download", methods=["GET"])
def download_kml():
    global LAST_JRAPH
    if LAST_JRAPH is None:
        return abort(500, 'something went wrong with the kml')
    encoded_kml = LAST_JRAPH.j2k().kml().encode()
    fh = io.BytesIO(encoded_kml)
    return send_file(
        fh,
        as_attachment=True,
        download_name="output.kml")


@app.route("/", methods=["GET", "POST"])
def index():
    global LAST_JRAPH
    if request.method == "GET":
        return render_template(
            "index.html", output="none", previous_queries=[])

    start_time = time.time()

    search = request.form.get("search")
    PREVIOUS_QUERIES.append(search)
    if search is None or len(search) == 0:
        return jsonify({
            "previousQuery": PREVIOUS_QUERIES[-1],
            "kml": None
        })

    nodes = query_node_prop(search)
    edges = query_many_node_edges([n.node_id for n in nodes])
    jr = Jraph(nodes=nodes, edges=edges)
    kml = jr.j2k().kml()
    LAST_JRAPH = jr

    time_taken = time.time() - start_time
    print('QUERY TIME: ', time_taken, ' seconds')

    return jsonify({
        "previousQuery": PREVIOUS_QUERIES[-1],
        "kml": kml
    })
