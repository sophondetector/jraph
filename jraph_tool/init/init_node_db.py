#!/usr/bin/env python
import json
import pandas as pd
import jraph_tool.dbc as dbc

_INIT_CSV_FP = 'lib/data/init_offshore_data.csv'


def generate_nodes(idf):
    to_drop = ["_id", "state_full", "node_id"]
    cols = [c for c in idf.columns if c not in to_drop]
    yield from zip(
        idf.node_id,
        idf[cols].to_dict(orient="records"))


def nan2none(d):
    for k in d.keys():
        if pd.isna(d[k]):
            d[k] = None
        if type(d[k]) is dict:
            d[k] = nan2none(d[k])
    return d


def main():
    print('preparing to insert offshore leaks nodes into jraph.node')
    df = pd.read_csv(_INIT_CSV_FP)
    row_gen = generate_nodes(df)
    with dbc.get_conn() as conn:
        for idx, (nid, props) in enumerate(row_gen):
            props = nan2none(props)
            with conn.cursor() as cur:
                cur.execute('SET IDENTITY_INSERT node ON;')
                cur.execute("INSERT node (node_id, properties) VALUES (?, ?)",
                            nid, json.dumps(props))
                cur.commit()
            print('\r{} rows inserted'.format(idx), end='')
    print(f'\ninserted {idx} offshore leaks notes into jraph.node')


if __name__ == '__main__':
    main()
