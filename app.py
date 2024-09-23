import io
from flask import Flask, request, render_template, send_file

from jtool.jraph import Jraph
from jtool.dbc import query_node, query_node_edges, query_node_prop


app = Flask("jraph")


# @app.route("/query", methods=["GET"])
# def query():
#     jr = Jraph()
#
#     node_ids = request.args.get("node_id", '').split(',')
#     for nid in node_ids:
#         node = query_node(nid)
#         edges = query_node_edges(nid)
#         jr.add(node, edges)
#
#     names = request.args.get("name", '').split(',')
#     for name in names:
#         node = query_node_prop("name", name)
#
#     kml = jr.j2k()
#     fh = io.BytesIO(kml.kml().encode())
#     return send_file(
#         fh,
#         as_attachment=True,
#         download_name="output.kml")


@app.route("/", methods=["GET", "POST"])
def index():
    s = request.get_data(as_text=True)
    l = s.split('&')
    for i in l:
        k, v = i.split('=')
        if len(v) > 0:
            res = query_node_prop(k, v)
            print(res)
    return render_template("index.html")
