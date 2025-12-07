import os
import json
from typing import Optional, Union, List, Tuple

import psycopg
import pandas as pd
from dotenv import load_dotenv

from .classes import Node, Edge

load_dotenv()

_CONN = None
_DB_HOST_VAR = "DB_HOST"
_DB_USER_VAR = "DB_USER"
_DB_PASSWORD_VAR = "DB_PASSWORD"
_DB_NAME = "offshore_leaks"
_TIMEOUT = 10


def _nan2none(d: dict) -> dict:
    """
    recurses through dict changing NaN to None
    """
    for k in d.keys():
        if pd.isna(d[k]):
            d[k] = None
        if type(d[k]) is dict:
            d[k] = _nan2none(d[k])
    return d


def check_for_sql_injection(search_str: str) -> bool:
    """
    checks for non alphanum chars in search_str
    returns True if one is found - else False
    """
    for char in search_str:
        if not char.isalnum():
            return True
    return False


def get_conn() -> psycopg.Connection:
    global _CONN, _DB_HOST_VAR, _DB_PASSWORD_VAR, _DB_NAME, _DB_USER, _TIMEOUT

    if _CONN is not None:
        return _CONN

    host = os.getenv(_DB_HOST_VAR)
    if host is None:
        raise Exception(f'{_DB_HOST_VAR} required in env!')

    password = os.getenv(_DB_PASSWORD_VAR)
    if password is None:
        raise Exception(f'{_DB_PASSWORD_VAR} required in env!')

    user = os.getenv(_DB_USER_VAR)
    if user is None:
        raise Exception(f'{_DB_USER_VAR} required in env!')

    conn_str = "host={} dbname={} user={} password={}".format(
        host,
        _DB_NAME,
        user,
        password
    )

    _CONN = psycopg.connect(conn_str, connect_timeout=_TIMEOUT)

    return _CONN


def get_cur() -> psycopg.Cursor:
    return get_conn().cursor()


def _row2node(
    row: Tuple[int, float, float, Optional[str], Optional[str]]
) -> Node:
    node_id, long, lat, name, label = row
    props = {
        "name": name,
        "label": label
    }
    return Node(node_id, long=long, lat=lat, properties=props)


def _row2edge(row: Tuple[int, int, int, str]) -> Edge:
    edge_id, source_id, target_id, link = row
    props = {"description": link}
    return Edge(edge_id, source_id, target_id, props)


def query_node(node_id: int) -> Optional[Node]:
    with get_cur() as cur:
        cur.execute(
            """
            SELECT
                node_id,
                geocoded_address->'features'->0->'geometry'->'coordinates'->>0 as long,
                geocoded_address->'features'->0->'geometry'->'coordinates'->>1 as lat,
                geocoded_address->'features'->0->'properties'->'geocoding'->>'name' as name,
                geocoded_address->'features'->0->'properties'->'geocoding'->>'label' as label
            FROM
                nodes_nom_addresses
            WHERE node_id=%s;
            """,
            (node_id,)
        )
        row = cur.fetchone()
    if row is None:
        return None
    return _row2node(row)


def query_nodes_within_radius(
    lat: float,
    long: float,
    r_meters: float = 50000
) -> Optional[List[Node]]:
    with get_cur() as cur:
        cur.execute(
            """
            SELECT
                g.node_id,
                geocoded_address->'features'->0->'geometry'->'coordinates'->>0 as long,
                geocoded_address->'features'->0->'geometry'->'coordinates'->>1 as lat,
                geocoded_address->'features'->0->'properties'->'geocoding'->>'name' as name,
                geocoded_address->'features'->0->'properties'->'geocoding'->>'label' as label
            FROM nodes_geog n
            INNER JOIN
                nodes_nom_addresses g
            ON n.node_id = g.node_id
            WHERE ST_DWithin(
                n.geog,
                ST_MakePoint(%s, %s)::geography,
                %s
            );""",
            (long, lat, r_meters)
        )
        return [_row2node(row) for row in cur.fetchall()]


def query_n_nearest_nodes(lat: float, long: float, n: int = 10) -> List[int]:
    with get_cur() as cur:
        cur.execute(
            """SELECT node_id FROM nodes_geog
            ORDER BY coord <-> POINT (%s, %s)
            LIMIT %s
            """,
            (long, lat, n)
        )
        return [nid for (nid,) in cur.fetchall()]


def query_edge_source(source_id: int) -> List[Edge]:
    with get_cur() as cur:
        cur.execute(
            """SELECT edge_id, _start, _end, link
            FROM relationships WHERE _start=%s;""",
            (source_id,)
        )
        return [_row2edge(row) for row in cur.fetchall()]


def query_edge_target(target_id: int) -> List[Edge]:
    with get_cur() as cur:
        cur.execute(
            """SELECT edge_id, _start, _end, link
            FROM relationships WHERE _end=%s;""",
            (target_id,)
        )
        return [_row2edge(row) for row in cur.fetchall()]


def query_node_edges(node_id: int) -> List[Edge]:
    with get_cur() as cur:
        cur.execute(
            """SELECT edge_id, _start, _end, link
            FROM relationships
            WHERE _start=%s OR _end=%s;""",
            (node_id, node_id)
        )
        return [_row2edge(row) for row in cur.fetchall()]


def query_many_node_edges(node_id_arr: List[int]) -> List[Edge]:
    with get_cur() as cur:
        # TODO way to ensure unique in SQL?
        cur.execute(
            """
            SELECT edge_id, _start, _end, link
            FROM relationships
            WHERE _start = ANY(%s)
            AND _end   = ANY(%s);
            """,
            (node_id_arr, node_id_arr)
        )

        return [_row2edge(row) for row in cur.fetchall()]


def query_node_prop(value: str) -> List[Node]:
    sql = """
    SELECT
        node_id,
        geocoded_address->'features'->0->'geometry'->'coordinates'->>0 as long,
        geocoded_address->'features'->0->'geometry'->'coordinates'->>1 as lat,
        geocoded_address->'features'->0->'properties'->'geocoding'->>'name' as name,
        geocoded_address->'features'->0->'properties'->'geocoding'->>'label' as label
    FROM nodes_nom_addresses
    WHERE geocoded_address->'features'->0->'properties'->>'geocoding'
    LIKE '%{}%';
    """.format(value)
    with get_cur() as cur:
        cur.execute(sql)
        return [_row2node(r) for r in cur.fetchall()]


def query_connected_nodes(node_id: int) -> List[Tuple[Edge, Node]]:
    sql = """
    SELECT
        r.edge_id,
        r._start,
        r._end,
        r.link,
        a.node_id,
        a.geocoded_address->'features'->0->'geometry'->'coordinates'->>0 as long,
        a.geocoded_address->'features'->0->'geometry'->'coordinates'->>1 as lat,
        a.geocoded_address->'features'->0->'properties'->'geocoding'->>'name' as name,
        a.geocoded_address->'features'->0->'properties'->'geocoding'->>'label' as label
    FROM relationships r
    INNER JOIN nodes_nom_addresses a
    ON r._end = a.node_id OR r._start = a.node_id
    WHERE r._end = %s OR r._start = %s;
    """
    with get_cur() as cur:
        cur.execute(sql, (node_id, node_id))
        return [
            (_row2edge(r[:4]), _row2node(r[4:]))
            for r in cur.fetchall()
        ]


if __name__ == '__main__':
    print('TESTING JRAPH CONN')
    with get_cur() as cur:
        cur.execute(
            """
            SELECT * FROM nodes_geog LIMIT 10;
            """
        )
        for res in cur.fetchall():
            print(res)
    print('DONE')

    print('TESTING query_connected_nodes')
    res = query_connected_nodes(14003462)
    for r in res:
        print(r)
