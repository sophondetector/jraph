import io
import logging

from typing import Optional

from flask import Flask, request, render_template, send_file, abort, jsonify

from jtool.jraph import Jraph
from jtool.dbc import (
    query_many_node_edges,
    query_node_prop,
    query_nodes_within_radius,
    check_for_sql_injection,
    get_conn
)


app = Flask("jraph")
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

app.logger.info("establishing connection to database...")

try:
    get_conn()
except Exception as e:
    app.logger.error("could not connect to database!")
    app.logger.error(e)
    quit(1)

app.logger.info("connection established")

# TODO change so there are session objects
LAST_JRAPH: Optional[Jraph] = None
PREVIOUS_QUERIES = []


@app.route("/related-nodes", methods=["POST"])
def related_nodes():
    node_id = request.form.get("node_id")
    if node_id is None:
        return abort(500, "missing param: node_id")

    # return jraph object consisting ONLY of the queried node
    # and its connected neighbors and the edges to/from the node
    # then return as geoJSON
    return abort(500, "not implemented yet!")


@app.route("/nodes-within-radius", methods=["POST"])
def nodes_within_radius():
    global LAST_JRAPH, PREVIOUS_QUERIES
    lat = request.form.get("lat", type=float)
    lng = request.form.get("lng", type=float)
    r_meters = request.form.get("rad", type=float)

    if lat is None or lng is None or r_meters is None:
        return abort(500, 'nodes-within-radius: missing parameters')

    nodes = query_nodes_within_radius(lat, lng, r_meters)
    if nodes is None:
        return jsonify({
            "previousQuery": PREVIOUS_QUERIES[-1],
            "geoJson": None
        })

    edges = query_many_node_edges([n.node_id for n in nodes])

    LAST_JRAPH = Jraph(nodes=nodes, edges=edges)
    geojson = LAST_JRAPH.j2gj()
    PREVIOUS_QUERIES.append(f"lat: {lat}\tlong: {lng}\trad_meters:{r_meters}")
    return jsonify({
        "previousQuery": PREVIOUS_QUERIES[-1],
        "geoJson": geojson
    })


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

    search = request.form.get("search")

    PREVIOUS_QUERIES.append(search)
    if search is None or len(search) == 0:
        return jsonify({
            "previousQuery": PREVIOUS_QUERIES[-1],
            "kml": None
        })

    if check_for_sql_injection(search):
        app.logger.warning("SQL INJECTION DETECTED: {}".format(search))
        app.logger.warning("SQL INJECTION IP: {}".format(request.remote_addr))
        return abort(500, 'something went wrong')

    nodes = query_node_prop(search)
    edges = query_many_node_edges([n.node_id for n in nodes])
    jr = Jraph(nodes=nodes, edges=edges)
    geo_json = jr.j2gj()
    LAST_JRAPH = jr

    return jsonify({
        "previousQuery": PREVIOUS_QUERIES[-1],
        "geoJson": geo_json
    })
