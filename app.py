import io
import json
import logging

from flask import Flask, request, render_template, send_file, abort, jsonify

from jtool.jraph import Jraph
from jtool.dbc import (
    query_many_node_edges,
    query_node_prop,
    query_nodes_within_radius,
    query_connected_nodes,
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


@app.route("/related-nodes", methods=["POST"])
def related_nodes():
    node_id = request.form.get("nodeId", type=int)
    if node_id is None:
        return abort(500, "missing param: nodeId")

    jr = Jraph()
    for edge, node in query_connected_nodes(node_id):
        jr.add_edge(edge)
        jr.add_node(node)

    geojson = jr.j2gj()
    pq = f'Connections to {node_id}'
    return jsonify({
        "previousQuery": pq,
        "geoJson": geojson
    })


@app.route("/nodes-within-radius", methods=["POST"])
def nodes_within_radius():
    lat = request.form.get("lat", type=float)
    lng = request.form.get("lng", type=float)
    r_meters = request.form.get("rad", type=float)

    if lat is None or lng is None or r_meters is None:
        return abort(500, 'nodes-within-radius: missing parameters')

    nodes = query_nodes_within_radius(lat, lng, r_meters)
    pq = f"lat: {lat}\tlong: {lng}\trad_meters:{r_meters}"
    if nodes is None:
        return jsonify({
            "previousQuery": pq,
            "geoJson": None
        })

    edges = query_many_node_edges([n.node_id for n in nodes])

    jr = Jraph(nodes=nodes, edges=edges)
    geojson = jr.j2gj()
    return jsonify({
        "previousQuery": pq,
        "geoJson": geojson
    })


@app.route("/download-gpkg", methods=["POST"])
def download_gpkg():
    input_geojson = request.form.get("geojson")
    if input_geojson is None:
        return abort(500, 'could not make file')
    as_dict = json.loads(input_geojson)
    jr = Jraph(input_geojson=as_dict)
    return send_file(
        jr.j2q(),
        as_attachment=True,
        download_name="output.gpkg")


@app.route("/download-kml", methods=["POST"])
def download_kml():
    input_geojson = request.form.get("geojson")
    if input_geojson is None:
        return abort(500, 'could not make file')
    jr = Jraph(input_geojson=json.loads(input_geojson))
    encoded_kml = jr.j2k().kml().encode()
    fh = io.BytesIO(encoded_kml)
    return send_file(
        fh,
        as_attachment=True,
        download_name="output.kml")


# TODO make search its own endpoint
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    search = request.form.get("search")
    if search is None or len(search) == 0:
        return jsonify({
            "previousQuery": search,
            "geoJson": None
        })

    if check_for_sql_injection(search):
        app.logger.warning("SQL INJECTION DETECTED: {}".format(search))
        app.logger.warning("SQL INJECTION IP: {}".format(request.remote_addr))
        return abort(500, 'something went wrong')

    nodes = query_node_prop(search)
    edges = query_many_node_edges([n.node_id for n in nodes])
    jr = Jraph(nodes=nodes, edges=edges)
    geo_json = jr.j2gj()

    return jsonify({
        "previousQuery": search,
        "geoJson": geo_json
    })
