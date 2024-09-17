import json
import pandas as pd
# import jraph_tool.dbc as dbc

_EDGE_CSV = 'lib/data/init_offshore_edges.csv'
_DF = pd.read_csv(_EDGE_CSV, index_col=None)
