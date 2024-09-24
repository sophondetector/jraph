import io
from typing import List, Tuple
from urllib.parse import unquote

from flask import Flask, request, render_template, send_file

from jtool.jraph import Jraph
from jtool.dbc import query_node, query_node_edges, query_node_prop


app = Flask("jraph")

DEFAULT_OUTPUT = "No output yet"
LAST_OUTPUT = DEFAULT_OUTPUT
PREVIOUS_QUERIES = []


def _parse_args(arg_string) -> List[Tuple[str, str]]:
    res = []
    for tup in map(lambda x: x.split('='), arg_string.split('&')):
        if len(tup[1]) > 0:
            res.append(tup)
    return res


def _decode_args(request) -> str:
    _bytes = request.get_data()
    raw_str = _bytes.decode()
    unquoted = unquote(raw_str)
    final = unquoted.replace('+', ' ')
    return final


@app.route("/download", methods=["GET"])
def download():
    global LAST_OUTPUT
    fh = io.BytesIO(LAST_OUTPUT.encode())
    return send_file(
        fh,
        as_attachment=True,
        download_name="output.kml")


@app.route("/", methods=["GET", "POST"])
def index():
    global LAST_OUTPUT, PREVIOUS_QUERIES, app
    if request.method == "GET":
        return render_template(
            "index.html", output="none", previous_queries=[])

    decoded = _decode_args(request)
    arg_list = _parse_args(decoded)

    if len(arg_list) < 1:
        LAST_OUTPUT = ''
        PREVIOUS_QUERIES.append("NO QUERY")
        return render_template(
            "index.html",
            output=LAST_OUTPUT,
            previous_queries=PREVIOUS_QUERIES
        )

    nodes = []
    this_query = ''
    for k, v in arg_list:
        if not v:
            continue
        this_query += '{}: {}|'.format(k.strip(), v.strip())
        if k == "node_id":
            node_set = map(lambda nid: query_node(nid), v.split(','))
        else:
            node_sets = map(lambda val: query_node_prop(k, val), v.split(','))
            node_set = [node for node_set in node_sets for node in node_set]
        nodes.extend(node_set)
    this_query = this_query[:-1]

    jr = Jraph()
    seen_nodes = set()
    seen_edges = set()
    for n in nodes:
        # TODO why there are Nones here sometimes?
        if n is None:
            continue
        if n.node_id in seen_nodes:
            continue
        seen_nodes.add(n.node_id)
        edges = query_node_edges(n.node_id)
        edges = filter(lambda e: e.edge_id not in seen_edges, edges)
        map(lambda ed: seen_edges.add(ed.edge_id), edges)
        jr.add(nodes=n, edges=edges)

    PREVIOUS_QUERIES.append(this_query)
    LAST_OUTPUT = jr.j2k().kml()
    return render_template(
        "index.html",
        output=LAST_OUTPUT,
        previous_queries=PREVIOUS_QUERIES
    )
