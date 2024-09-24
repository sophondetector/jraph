import io
from flask import Flask, request, render_template, send_file

from jtool.jraph import Jraph
from jtool.dbc import query_node, query_node_edges, query_node_prop


app = Flask("jraph")

DEFAULT_OUTPUT = "No output yet"
LAST_OUTPUT = DEFAULT_OUTPUT


@app.route("/download", methods=["GET"])
def download():
    global LAST_OUTPUT
    fh = io.BytesIO(LAST_OUTPUT.encode())
    return send_file(
        fh,
        as_attachment=True,
        download_name="output.kml")


@app.route("/", methods=["GET"])
def index():
    global LAST_OUTPUT
    arg_list = list(request.args.items())
    print('ARGS ', arg_list)
    if len(arg_list) < 1:
        return render_template("index.html", output=LAST_OUTPUT)

    nodes = []
    for k, v in arg_list:
        if k == "node_id":
            node_row = [query_node(v)]
        elif len(v) > 0:
            node_row = query_node_prop(k, v)
        else:
            node_row = []
        nodes.extend(node_row)

    jr = Jraph()
    seen = set()
    for n in nodes:
        # TODO track this down
        if n is None:
            continue
        if n.node_id in seen:
            continue
        seen.add(n.node_id)
        jr.add(n)

    LAST_OUTPUT = jr.j2k().kml()
    return render_template("index.html", output=LAST_OUTPUT)
