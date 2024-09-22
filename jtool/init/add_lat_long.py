import json
import jtool.dbc as dbc
import pandas as pd

df = pd.read_csv('country_information.csv')

with dbc.get_cur() as cur:
    sql = """
    select * from node
    where properties not like '%USA%';
    """
    cur.execute(sql)
    rows = cur.fetchall()

records = []
for r in rows:
    nid, prop_string = r
    rec = json.loads(prop_string)
    rec['node_id'] = nid
    records.append(rec)

ef = pd.DataFrame.from_records(data=records)
ef = ef[ef.country_codes.notna()]
ef.drop('lat', inplace=True, axis=1)
ef.drop('long', inplace=True, axis=1)
ef['alpha3'] = ef.country_codes.apply(lambda cc: cc.split(';')[0])

ff = ef.merge(df[['lat', 'long', 'alpha3']], on="alpha3", how="inner")

sql_lat = """
UPDATE node
SET properties = json_modify(properties, '$.lat', ?)
WHERE node_id = ?;
"""

sql_long = """
UPDATE node
SET properties = json_modify(properties, '$.long', ?)
WHERE node_id = ?;
"""

for idx, row in ff.iterrows():
    with dbc.get_cur() as cur:
        cur.execute(sql_lat, row.lat, row.node_id)
        cur.execute(sql_long, row.long, row.node_id)
        cur.commit()
    print('\r{} rows inserted'.format(idx), end='')

print(f'\ninserted {idx} lat longs into jraph.node')
