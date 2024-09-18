import pandas as pd

print('making csv of nodes connected to us nodes')

_UBER_CSV = '~/Public/Datasets/offshore-leaks-db/nodes-entities.csv'
_INIT_EDGES_CSV = 'lib/data/init_offshore_edges.csv'
_US_ENTITY_CSV = 'lib/data/init_offshore_data.csv'
_OUTPUT_FP = 'lib/data/us_connected_nodes.csv'

udf = pd.read_csv(_UBER_CSV)
edf = pd.read_csv(_INIT_EDGES_CSV)
usdf = pd.read_csv(_US_ENTITY_CSV)

node_ids = set()
for v in edf._start.values:
    node_ids.add(v)

for v in edf._end.values:
    node_ids.add(v)

udf.set_index('node_id', inplace=True, drop=False)
node_index = pd.Index(node_ids)
out = udf.filter(node_index, axis=0)
# out = out[out.country_codes.apply(lambda cc: 'USA' not in cc)]

out.to_csv(_OUTPUT_FP, index=False)

print(f'save to {_OUTPUT_FP} done')
