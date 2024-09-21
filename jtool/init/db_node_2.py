import pandas as pd
import jtool.dbc as dbc


print('preparing to insert us connected nodes')

US_CONNECTED_CSV = 'lib/data/us_connected_nodes.csv'
DF = pd.read_csv(US_CONNECTED_CSV)
STOP = -1
SUCCESS = 0
ERROR = 0

for idx, row in DF.iterrows():
    print('DOING ', idx)
    props_only = row.drop(['node_id'])
    props_string = props_only.to_json()

    try:
        res = dbc.insert_node(row.node_id, props_string)
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
