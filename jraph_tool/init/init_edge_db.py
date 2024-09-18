import json
import pandas as pd
import jraph_tool.dbc as dbc
import jraph_tool.init.init_utils as ut

_EDGE_CSV = 'lib/data/init_offshore_edges.csv'
_DF = pd.read_csv(_EDGE_CSV)

_STOP = 10


def insert_node(nid, props, cur=None):
    if cur is None:
        cur = dbc.get_cur()

    if type(props) is dict:
        props = json.dumps(props)
        props = ut.nan2none(props)

    with cur:
        cur.execute('SET IDENTITY_INSERT node ON;')
        cur.execute("INSERT node (node_id, properties) VALUES (?, ?)",
                    nid, props)
        cur.commit()
        return cur.fetchone()


def insert_edge(source_id, target_id, props=None, cur=None):
    if cur is None:
        cur = dbc.get_cur()

    if props is None:
        props = '{}'

    if type(props) is dict:
        props = json.dumps(props)
        props = ut.nan2none(props)

    with cur:
        cur.execute(
            "INSERT edge (source_id, target_id, properties) VALUES (?, ?, ?)",
            row._start, row._end, props)
        cur.commit()
        return cur.fetchone()


try:
    for idx, row in _DF.iterrows():
        print('DOING ', idx)
        print(row)
        props_only = row.drop(['_start', '_end', '_type'])
        props_string = props_only.to_json()
        insert_edge(row._start, row._end, props_string)

        if idx == _STOP:
            break

except Exception as e:
    print(e)

finally:
    dbc.get_conn().close()
