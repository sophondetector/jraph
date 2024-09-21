import os
import json
import pyodbc
from typing import Optional, Union, List

from .utils import nan2none
from .classes import Node, Edge

_CONN = None

# cat /etc/odbcinst.ini to find correct val for DRIVER for Sql Server
_DB_DRIVER = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.4.so.1.1'
_JRAPH_DB = 'jraph'
_JRAPH_HOST = 'localhost'
_JRAPH_USER = 'sa'


def _get_pass():
    pw = os.getenv("JRAPH_SA_PASSWORD")
    if not pw:
        print("JRAPH_SA_PASSWORD required in env!")
        exit(1)

    if pw[0] == '"' and pw[-1] == '"':
        return pw[1:-1]

    return pw


def get_conn() -> pyodbc.Connection:
    global _CONN
    if _CONN is None:
        print(f"connecting to {_JRAPH_DB}...", end='')
        cstring = 'DRIVER={};SERVER={};UID={};PWD={};DATABASE={}'.format(
            _DB_DRIVER, _JRAPH_HOST, _JRAPH_USER, _get_pass(), _JRAPH_DB)
        cstring += ';TrustServerCertificate=yes'
        _CONN = pyodbc.connect(cstring)
        print("done")
    return _CONN


def get_cur() -> pyodbc.Cursor:
    return get_conn().cursor()


def query_node(node_id: int) -> Node:
    with get_cur() as cur:
        cur.execute("SELECT * FROM node WHERE node_id=?;", node_id)
        node_id, properties_raw = cur.fetchone()
        props = json.loads(properties_raw)
        return Node(node_id, **props)


def query_edge_source(source_id) -> List[Edge]:
    with get_cur() as cur:
        cur.execute("SELECT * FROM edge WHERE source_id=?;", source_id)
        res = []
        seen = set()
        for row in cur.fetchall():
            edge_id = row[0]
            if edge_id in seen:
                continue
            seen.add(edge_id)
            source_id = row[1]
            target_id = row[2]
            props = json.loads(row[3])
            res.append(Edge(edge_id, source_id, target_id, **props))
    return res


def query_edge_target(target_id) -> List[Edge]:
    with get_cur() as cur:
        cur.execute("SELECT * FROM edge WHERE target_id=?;", target_id)
        res = []
        seen = set()
        for row in cur.fetchall():
            edge_id = row[0]
            if edge_id in seen:
                continue
            seen.add(edge_id)
            source_id = row[1]
            target_id = row[2]
            props = json.loads(row[3])
            res.append(Edge(edge_id, source_id, target_id, **props))
    return res


def query_node_edges(node_id) -> List[Edge]:
    res = query_edge_source(node_id)
    res.extend(query_edge_target(node_id))
    return res


def insert_node(
        nid,
        props: Optional[Union[dict, str]] = None,
        cur: Optional[pyodbc.Cursor] = None):

    if cur is None:
        cur = get_cur()

    if type(props) is dict:
        props = nan2none(props)
        props = json.dumps(props)
        # TODO use a better json encoder for this

    with cur:
        cur.execute('SET IDENTITY_INSERT node ON;')
        cur.execute("INSERT node (node_id, properties) VALUES (?, ?)",
                    nid, props)
        cur.commit()


def insert_edge(
        source_id: int,
        target_id: int,
        props: Optional[Union[dict, str]] = None,
        cur: Optional[pyodbc.Cursor] = None):

    if cur is None:
        cur = get_cur()

    if props is None:
        props = '{}'

    if type(props) is dict:
        props = nan2none(props)
        props = json.dumps(props)
        # TODO use a better json encoder for this

    with cur:
        cur.execute(
            "INSERT edge (source_id, target_id, properties) VALUES (?, ?, ?)",
            source_id, target_id, props)
        cur.commit()
