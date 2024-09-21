import pandas as pd
import jtool.dbc as dbc


EDGE_CSV = 'lib/data/init_offshore_edges.csv'
DF = pd.read_csv(EDGE_CSV)
STOP = -1
SUCCESS = 0
ERROR = 0

for idx, row in DF.iterrows():
    print('DOING ', idx)
    props_only = row.drop(['_start', '_end', '_type'])
    props_string = props_only.to_json()

    try:
        res = dbc.insert_edge(row._start, row._end, props_string)
        SUCCESS += 1
    except Exception as e:
        ERROR += 1
        print('error at row {}'.format(idx))
        print(e)

    if idx == STOP:
        break

dbc.get_conn().close()
print('attempted {} rows'.format(idx))
print('{} successful'.format(SUCCESS))
print('{} errors'.format(ERROR))
